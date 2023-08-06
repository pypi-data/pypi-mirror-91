from typing import List

import torch
import torch.utils


def collate_fn_only_data(
    batch: List,
):  # Here we would need two collate function for train and validation!
    r"""
    This collate_fn function can be used with the "SamplerSimple" and "SamplerBalanced".
    The batch size should be set in the Sampler and not in the DataLoader.
    TODO: Need to iterate over the batch and not only use the first.
    """
    data = batch[0][0]
    if len(batch[0]) == 1:
        return data
    else:
        target = torch.as_tensor(batch[0][1], dtype=torch.int64)
        if len(batch[0]) == 2:
            return data, target
        else:
            features = batch[0][0]
            return data, target, features


def collate_fn_data_and_labels(
    batch: List,
):  # Here we would need two collate function for train and validation!
    r"""
    This collate_fn function can be used with the "SamplerSimple" and "SamplerBalanced".
    The batch size should be set in the Sampler and not in the DataLoader.
    TODO: Need to iterate over the batch and not only use the first.
    """
    data = batch[0][0]
    target = torch.as_tensor(batch[0][1], dtype=torch.int64)
    return data, target
