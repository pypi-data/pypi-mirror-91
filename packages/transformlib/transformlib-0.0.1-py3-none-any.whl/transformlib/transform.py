"""Contains the Transform abstraction and helper methods.
"""
from transformlib import Node
from transformlib import Output
from transformlib import Input

from typing import List
from typing import Tuple
from typing import Dict

import logging

logger = logging.getLogger(__name__)


class Transform:
    """Used to organize transformations of data.

    A Transform is a many to many mapping between Inputs and Outputs. When run the Inputs are
    loaded and the calculated outputs from the function is written to the Outputs.
    """

    def __init__(self, output_args, func, input_kwargs):
        self.output_args = output_args
        self.func = func
        self.input_kwargs = input_kwargs

    @property
    def output_args(self):
        """Output arguments of the transform.
        """
        return self._output_args

    @output_args.setter
    def output_args(self, value):
        if len(set(value)) != len(value):
            raise ValueError(f"Duplicate {value}")
        self._output_args = value

    @property
    def input_kwargs(self):
        """Input key value arguments of the transform.
        """
        return self._input_kwargs

    @input_kwargs.setter
    def input_kwargs(self, value):
        if len(set(value.values())) != len(value.values()):
            raise ValueError(f"Duplicate {value}")
        self._input_kwargs = value

    @property
    def outputs(self) -> Tuple[Output]:
        """A tuple with all the Outputs of the Transform.
        """
        return tuple(self.output_args)

    @property
    def inputs(self) -> Tuple[Input]:
        """A tuple with all the Inputs of the Transform.
        """
        return tuple(self.input_kwargs.values())

    @property
    def nodes(self) -> Tuple[Node]:
        """A tuple with all the Nodes of the Transform e.g. Input and Output.
        """
        return tuple(self.outputs + self.inputs)

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)

    def __repr__(self):
        return (
            f'{self.__class__}('
            + ', '.join(map(repr, self.output_args))
            + ', '.join(map(
                lambda key: key + '=' + repr(self.input_kwargs[key]),
                self.input_kwargs
            ))
            + ')'
        )

    def __str__(self):
        return self.func.__name__

    def __eq__(self, other):
        if set(self.nodes) == set(other.nodes):
            return True
        return False

    def __hash__(self):
        return hash((self.func, *self.output_args, *self.input_kwargs.items()))

    def run(self, **param_kwargs):
        """Runs a transform, the param_kwargs is overwritten by transform kwargs.

        A parameter to a transform is an external transform input which is
        NOT a DataFrame. This could be a model or the like.

        Args:
           *param_kwargs (Dict[str, Any]): A list og keyword argument
                parameters to a transform.

        Returns:
            Tuple[Output]: A tuple with the calculated outputs.
        """
        logger.info(f'Beginning running of {self}.')
        calc_outputs = self(
            **param_kwargs,
            **{
                key: self.input_kwargs[key].load()
                for key in self.input_kwargs
            }
        )
        if len(self.outputs) == 1:
            calc_outputs = (calc_outputs, )
        else:
            calc_outputs = tuple(calc_outputs)
        for idx, output in enumerate(self.outputs):
            output.save(calc_outputs[idx])
        logger.info(f'Completed running of {self}.')
        return calc_outputs


def transform(*args: Output, **kwargs: Input):
    """Convert a function to a Transform.

    Args:
        *args (List[Input]): The outputs of the transform.
        **kwargs (Dict[str, Input]): The inputs to the transform.

    Returns:
        function: A decorator that returns a Transform object.
    """
    def decorator(func) -> Transform:
        output_args = _filter_outputs(args)
        input_kwargs = _filter_inputs(kwargs)
        return Transform(output_args, func, input_kwargs)
    return decorator


def _filter_outputs(args) -> List[Output]:
    """Filter out anything that is not an Output."""
    return [
        arg for arg in args
        if isinstance(arg, Output)
    ]


def _filter_inputs(kwargs) -> Dict[str, Input]:
    """Filter out anything that is not an Input."""
    return {
        key: kwargs[key] for key in kwargs
        if isinstance(kwargs[key], Input)
    }
