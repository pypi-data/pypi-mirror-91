# Copyright 2020 Q-CTRL Pty Ltd & Q-CTRL Inc. All rights reserved.
#
# Licensed under the Q-CTRL Terms of service (the "License"). Unauthorized
# copying or use of this file, via any medium, is strictly prohibited.
# Proprietary and confidential. You may not use this file except in compliance
# with the License. You may obtain a copy of the License at
#
#     https://q-ctrl.com/terms
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS. See the
# License for the specific language.

"""
Controller for integration of BOULDER OPAL automated closed-loop optimizers and M-LOOP.
"""

from typing import (
    Any,
    List,
    Optional,
    Union,
)
from warnings import warn

import numpy as np
from mloop.controllers import Controller
from mloop.interfaces import Interface
from mloop.learners import (
    Learner,
    RandomLearner,
)
from qctrl import Qctrl
from qctrlcommons.preconditions import check_argument


class QctrlController(Controller):
    """
    Controller for optimizations that uses BOULDER OPAL automated
    closed-loop optimizers.

    You can use this controller to integrate an experiment managed by
    M-LOOP to a BOULDER OPAL automated closed-loop optimizer. Notice that
    you need to set up an M-LOOP Interface to your experiment, initiate a
    BOULDER OPAL session, and define your choice of BOULDER OPAL automated
    closed-loop optimizer prior to using this class.

    Arguments
    ---------
    interface : mloop.interfaces.Interface
        The M-LOOP interface from where you obtain the cost value of the
        test points.
    qctrl : qctrl.Qctrl
        The object representing the BOULDER OPAL session. You must initiate
        it before calling the controller.
    optimizer : qctrl.types.closed_loop_optimization_step.Optimizer
        The BOULDER OPAL automated closed-loop optimizer that you want to
        use. It must be a valid optimizer object (containing either an
        initializer or a state from a previous optimization run), as
        described in the BOULDER OPAL reference documentation.
    test_point_count : int, optional
        The requested number of test points that the BOULDER OPAL automated
        closed-loop optimizer generates at each step. If chosen, it must be
        greater than zero. This is a hint only. The BOULDER OPAL automated
        closed-loop optimizer might choose differently.
    learner : mloop.learners.Learner, optional
        The M-LOOP Learner that this controller uses to obtain extra test
        points, before there are enough results to run a step of the
        BOULDER OPAL automated closed-loop optimizer. Defaults to None, in
        which case this controller uses a `RandomLearner`.
    training_run_count : int, optional
        The minimum number of training points that the controller obtains
        before calling the BOULDER OPAL automated closed-loop optimizer.
        Defaults to 0, in which case the controller uses the minimum number
        of points that the BOULDER OPAL automated closed-loop optimizer
        requires.
    interleaved_run_count : int, optional
        The minimum number of test points that the controller obtains from
        the `learner` between two calls of the BOULDER OPAL automated
        closed-loop optimizer, in addition to the points that BOULDER OPAL
        requested. Defaults to 0.
    kwargs : dict
        All the extra arguments that the Controller class from M-LOOP
        accepts.
    """

    def __init__(
        self,
        interface: Interface,
        qctrl: Qctrl,
        optimizer: Any,
        test_point_count: Optional[int] = None,
        learner: Optional[Learner] = None,
        training_run_count: int = 0,
        interleaved_run_count: int = 0,
        **kwargs,
    ):
        super().__init__(interface, **kwargs)

        # Auxiliary learner, used to get the initial test points before
        # there are enough points to run BOULDER OPAL automated closed-loop
        # optimization.
        self.learner = learner
        if self.learner is None:
            self.learner = RandomLearner(**self.remaining_kwargs)
        self._update_controller_with_learner_attributes()

        if test_point_count is not None:
            check_argument(
                test_point_count > 0,
                "The value of test_point_count must be greater than zero.",
                {"test_point_count": test_point_count},
            )

        self._test_point_count = test_point_count

        self._types_namespace = qctrl.types.closed_loop_optimization_step
        self._optimization_step = (
            qctrl.functions.calculate_closed_loop_optimization_step
        )

        if optimizer.state is not None:
            minimum_training_run_count = 0
        elif optimizer.cross_entropy_initializer is not None:
            minimum_training_run_count = np.ceil(
                2 / optimizer.cross_entropy_initializer.elite_fraction
            )
        elif optimizer.gaussian_process_initializer is not None:
            minimum_training_run_count = 2
        else:
            minimum_training_run_count = 2 * self.learner.num_params
            warn(
                f"Unrecognized optimizer {optimizer}, falling back to "
                f"{minimum_training_run_count} as the minimum number of "
                "training runs."
            )

        self._training_run_count = max(training_run_count, minimum_training_run_count)

        check_argument(
            interleaved_run_count >= 0,
            "The value of interleaved_run_count must not be negative.",
            {"interleaved_run_count": interleaved_run_count},
        )

        self._interleaved_run_count = interleaved_run_count

        self._optimizer = optimizer

    def _call_boulder_opal(self, cost_function_results: List[Any]) -> List[np.ndarray]:
        """
        Manages each call to BOULDER OPAL.
        """
        result = self._optimization_step(
            optimizer=self._optimizer,
            results=cost_function_results,
            test_point_count=self._test_point_count,
        )

        self._optimizer = self._types_namespace.Optimizer(state=result.state)

        return [np.array(test_point.parameters) for test_point in result.test_points]

    def _transform_cost(self) -> Union[float, np.ndarray]:
        """
        Adapts the cost values according to the needs of each learner.
        """
        cost = self.curr_cost

        if self.curr_bad:
            cost = float("inf")

        # The RandomLearner is different from the others in that it takes
        # the best parameters instead of the cost.
        if isinstance(self.learner, RandomLearner):
            cost = self.best_params

        return cost

    def _optimization_routine(self):
        """
        The main optimization routine.

        This overrides a method from the parent class in M-LOOP.
        """
        cost_function_results: List[Any] = []
        boulder_opal_parameters: List[np.ndarray] = []

        # Number of costs obtained before this function calls the BOULDER
        # OPAL automated closed-loop optimizer.
        required_run_count = self._training_run_count

        while self.check_end_conditions():
            # Call BOULDER OPAL only if the number of required runs has
            # been reached and there is at least one result to pass.
            if (self.num_in_costs >= required_run_count) and (
                len(cost_function_results) > 0
            ):
                boulder_opal_parameters = self._call_boulder_opal(cost_function_results)
                cost_function_results = []
                # The total number of runs before the next call to BOULDER
                # OPAL, which is: the current number of runs, plus the
                # number of runs that BOULDER OPAL requested, plus the
                # number of extra interleaved runs that the auxiliary
                # learner requests.
                required_run_count = (
                    self.num_in_costs
                    + len(boulder_opal_parameters)
                    + self._interleaved_run_count
                )

            # Obtain parameters from the BOULDER OPAL automated closed-loop
            # optimizer if any are available.
            use_boulder_opal_parameters = len(boulder_opal_parameters) > 0
            if use_boulder_opal_parameters:
                parameters = boulder_opal_parameters.pop(0)
            # Use auxiliary learner if the BOULDER OPAL automated
            # closed-loop optimizer doesn't have more parameters to suggest.
            else:
                parameters = self.learner_params_queue.get()

            # Communicate parameters to the experimental interface, and
            # obtain the results of the cost function.
            self._put_params_and_out_dict(parameters)
            self._get_cost_and_in_dict()

            self.save_archive()

            # Store cost function result in the learner's queue if it was
            # requested by the auxiliary learner.
            if not use_boulder_opal_parameters:
                self.learner_costs_queue.put(self._transform_cost())

            # Store cost function result in the list to be used by BOULDER OPAL.
            if not self.curr_bad:
                cost_function_results.append(
                    self._types_namespace.CostFunctionResult(
                        parameters=self.curr_params,
                        cost=self.curr_cost,
                        cost_uncertainty=self.curr_uncer,
                    )
                )
