import logging
from typing import Literal, Optional
from warnings import warn

import numpy as np

from streamsight.matrix import InteractionMatrix
from streamsight.matrix import TimestampAttributeMissingError
from streamsight.setting import Setting
from streamsight.setting.splitters import NPastInteractionTimestampSplitter, TimestampSplitter

logger = logging.getLogger(__name__)


class SingleTimePointSetting(Setting):
    """Single time point setting for splitting data into background and
    evaluation set.

    :param background_t: Time point to split the data into background and evaluation data. Split will be from ``[0, t)``
    :type background_t: int
    :param delta_after_t:
        Defaults to maximal integer value (acting as infinity).
    :type delta_after_t: int, optional
    :param n_seq_data: Number of last sequential interactions to provide as
        unlabeled data for model to make prediction.
    :type n_seq_data: int, optional
    :param top_K: Number of interaction per user that should be selected for evaluation purposes.
    :type top_K: int, optional
    :param item_user_based: Item or User based setting.
        Defaults to "user".
    :type item_user_based: Literal['user', 'item'], optional
    :param seed: Seed for randomization parts of the scenario.
        Timed scenario is deterministic, so changing seed should not matter.
        Defaults to None, so random seed will be generated.
    :type seed: int, optional

    """

    def __init__(
        self,
        background_t: int,
        delta_after_t: int = np.iinfo(np.int32).max,
        n_seq_data: int = 1,
        top_K: int = 1,
        item_user_based: Literal["user", "item"] = "user",
        seed: Optional[int] = None,
    ):
        super().__init__(seed=seed, item_user_based=item_user_based)
        self.t = background_t
        """Seconds before `t` timestamp value to be used in `background_set`."""
        self.delta_after_t = delta_after_t
        """Seconds after `t` timestamp value to be used in `ground_truth_data`."""
        self.n_seq_data = n_seq_data
        self.top_K = top_K

        logger.info(
            f"Splitting data at time {background_t} with delta_after_t interval {delta_after_t}")
        
        self._background_splitter =  TimestampSplitter(background_t, None, delta_after_t)
        self._splitter = NPastInteractionTimestampSplitter(
            background_t, delta_after_t, n_seq_data, self._item_user_based
        )
        self._data_timestamp_limit = background_t

    def _split(self, data: InteractionMatrix):
        """Splits your dataset into a training, validation and test dataset
            based on the timestamp of the interaction.

        :param data: Interaction matrix to be split. Must contain timestamps.
        :type data: InteractionMatrix
        """
        if not data.has_timestamps:
            raise TimestampAttributeMissingError()
        if data.min_timestamp > self.t:
            warn(
                f"Splitting at time {self.t} is before the first timestamp in the data. No data will be in the training set.")
            
        self._background_data, _ = self._background_splitter.split(data)
        past_interaction, future_interaction = self._splitter.split(data)
        self._unlabeled_data_series, self._ground_truth_data_series = self.prediction_data_processor.process(past_interaction, future_interaction)
        
