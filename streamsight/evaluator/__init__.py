"""
.. currentmodule:: streamsight.evaluator

Evaluator Builder
----------------------------

The evaluator module in streamsight contains the EvaluatorBuilder class which is
used to build an evaluator object. :class:`EvaluatorBuilder` allows the programmer
to add algorithms, metrics and settings to the evaluator object before the
:class:`Evaluator` object is built.

It is recommended to initialise the :class:`Evaluator` object with the :class:`EvaluatorBuilder`
as it provides the API for the needed configurations. Beyond the API for the configurations,
the builder checks for the validity of the configurations and raises exceptions if the
configurations are invalid. The programmer can choose to build the :class:`Evaluator` object
without the :class:`EvaluatorBuilder` as described below but might face exceptions if the
configurations are invalid.

The adding of new algorithms through :meth:`add_algorithm` and metrics through :meth:`add_metric`
are made such that it can be done through the class type via importing the class or 
thorough specifying the class name as a string.

.. autosummary::
    :toctree: generated/

    EvaluatorBuilder

Example
~~~~~~~~~

Below is a typical example of how to use the :class:`EvaluatorBuilder` to build an
:class:`Evaluator` object. This example also follows from the example in the
python notebook.

.. code-block:: python

    from streamsight.evaluator import EvaluatorBuilder
    
    builder = EvaluatorBuilder(item_user_based="item",
                        ignore_unknown_user=True,
                        ignore_unknown_item=True)
    builder.add_setting(setting)
    builder.add_algorithm("ItemKNNIncremental", {"K": 10})
    builder.add_metric("PrecisionK")
    evaluator = builder.build()

    evaluator.run()

Evaluator
----------------------------

The evaluator module in streamsight contains the Evaluator class which is
used to evaluate the performance of the algorithms on the data.

.. autosummary::
    :toctree: generated/

    Evaluator

Accumulator
----------------------------

The evaluator module in streamsight contains the Accumulator class which is
used to accumulate the metrics.

.. autosummary::
    :toctree: generated/

    MetricAccumulator
    MacroMetricAccumulator
    MicroMetricAccumulator
"""

from streamsight.evaluator.evaluator_builder import EvaluatorBuilder
from streamsight.evaluator.evaluator import Evaluator
from streamsight.evaluator.util import MetricLevelEnum
from streamsight.evaluator.accumulator import (
    MetricAccumulator,
    MacroMetricAccumulator,
    MicroMetricAccumulator,
)
