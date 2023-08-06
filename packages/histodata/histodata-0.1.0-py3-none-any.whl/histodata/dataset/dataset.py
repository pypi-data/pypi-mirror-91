import os
import random
from enum import IntEnum

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import torch
import torch.utils


class DataLoaderMode(IntEnum):
    TRAINING = 1
    VALIDATION = 2
    TRAINING_AND_VALIDATION = 3
    TEST = 4
    ALL = 7


# EIGENE FUNKTIOn, bekommt ein DATASET und splitted diese in zwei oder drei neue Datasets
# mode: DataLoaderMode,
# cross_validation_fold: O[U[Sequence[int], int]] = None,


class Loader:
    def __init__(self):
        pass

    def __call__(self, row, path_to_image):
        pass


class LoadFromImageFileLoader(Loader):
    def __init__(self, column):
        super().__init__()

        self.column = column

    def load_from_row(self, row, path_to_image):
        if callable(self.column):
            path = self.column(row)
        else:
            path = row[self.column]
        path_to_file = os.path.join(path_to_image, path)
        img = plt.imread(path_to_file)
        img = np.swapaxes(img, 0, 2)
        img = torch.as_tensor(img)
        return img

    def __call__(self, row_or_df, path_to_image):
        if isinstance(row_or_df, pd.DataFrame):
            imgs = []
            for _, row in row_or_df.iterrows():
                imgs.append(self.load_from_row(row, path_to_image))
            return torch.stack(imgs)
        else:
            return self.load_from_row(row_or_df, path_to_image)


class ReadValueFromCSVLoader(Loader):
    def __init__(self, column):
        super().__init__()

        self.column = column

    def __call__(self, row, path_to_image):
        if isinstance(self.column, list):
            return list(row[self.column])
        else:
            return row[self.column]


class TransformerAdapter:
    def __init__(self):
        pass

    def __call__(self, img_or_imgs):
        pass


class RandomPrinterAdapter(TransformerAdapter):
    def __init__(self, message="RandomPrinterAdapter:"):
        super().__init__()
        self.message = message

    def __call__(self, img_or_imgs):
        print(self.message, np.random.random())
        return img_or_imgs


def create_list_from_variable(variable):
    if variable is None:
        return []
    elif isinstance(variable, list):
        return variable
    else:
        return [variable]


def get_random_seed():
    module_random = random.getstate()  # TODO: same name as above!
    module_numpy = np.random.get_state()
    module_torch = torch.get_rng_state()  # this generates a NEW SEED !!!
    return module_random, module_numpy, module_torch


def set_random_seed(module_random, module_numpy, module_torch):
    random.setstate(module_random)
    np.random.set_state(module_numpy)
    torch.set_rng_state(module_torch)


def set_random_seed_with_int(integer):
    random.seed(integer)
    np.random.seed(random.randint(0, 99999999))
    torch.random.manual_seed(random.randint(0, 99999999))


class Adapter:
    def __init__(self, transfs=None, access_orders=None, is_callable_with_batches=None, seed=None):
        # convert or create list of pre_transformation_adapters
        self.transfs = create_list_from_variable(transfs)

        # create a new access_orders list
        if access_orders is not None:
            if len(self.transfs) != len(access_orders):
                assert AssertionError(
                    "The list of transformers and the list of access_order must be have "
                    + "the same length."
                )
            self.access_orders = access_orders
            for idx, v in enumerate(self.access_orders):
                self.access_orders[idx] = create_list_from_variable(v)
        else:
            self.access_orders = [[] for _ in self.transfs]

        # create a new is_callable_with_batches list
        if is_callable_with_batches is not None:
            if len(self.transfs) != len(is_callable_with_batches):
                assert AssertionError(
                    "The list of transformers and the list of is_callable_with_batches "
                    + "must be have the same length."
                )
            self.is_callable_with_batches = is_callable_with_batches
        else:
            self.is_callable_with_batches = [True for _ in self.transfs]

        self.seed = seed

    def append(self, trans, access_order=None, is_callable_with_batches=True):
        # TODO, need to check the values
        self.transfs.append(trans)
        self.access_orders.append(access_order)
        self.is_callable_with_batches.append(is_callable_with_batches)

    def __call__(self, item_or_batch, idx):

        is_batch = isinstance(idx, list)

        if self.seed is not None:
            saved_seed_state = get_random_seed()

        for (transf, order, batch_callable) in zip(
            self.transfs, self.access_orders, self.is_callable_with_batches
        ):

            if order is None or order == [] or order[0] is None or order[0] == -1:
                order = range(len(item_or_batch))

            for i, pos in enumerate(order):

                if i == 0:
                    tmp_saved_seed_state = get_random_seed()

                if is_batch and batch_callable and self.seed is None:
                    item_or_batch[pos] = transf(item_or_batch[pos])
                elif is_batch is False:
                    if self.seed is not None:
                        set_random_seed_with_int((1 + self.seed + idx) * int(1e8) + i * int(1e6))
                    item_or_batch[pos] = transf(item_or_batch[pos])
                else:
                    for j, item in enumerate(item_or_batch[pos]):
                        if self.seed is not None:
                            set_random_seed_with_int(
                                (1 + self.seed + idx[j]) * int(1e8) + i * int(1e6)
                            )
                        item_or_batch[pos][j] = transf(item)

                if i < len(order) - 1:
                    set_random_seed(*tmp_saved_seed_state)

        if self.seed is not None:
            set_random_seed(*saved_seed_state)

        return item_or_batch


class DatasetSTD(torch.utils.data.Dataset):
    def __init__(
        self,
        path_to_csv: str,
        path_to_images: str,
        image_loaders: str = None,
        feature_loaders: str = None,
        pre_transfs=None,
        da_transfs=None,
        seed: int = None,
        return_data_rows: bool = False,
    ):
        super().__init__()

        # save variables
        self.path_to_images = path_to_images
        self.path_to_csv = path_to_csv
        self.return_data_rows = return_data_rows
        self.seed = seed
        self.seed_increment = 0

        # convert or create list of image_loaders
        self.image_loaders = create_list_from_variable(image_loaders)
        for idx, image_loader in enumerate(self.image_loaders):
            if isinstance(image_loader, str):
                self.image_loaders[idx] = LoadFromImageFileLoader(image_loader)

        # convert or create list of feature_loaders
        self.feature_loaders = create_list_from_variable(feature_loaders)
        for idx, feature_loader in enumerate(self.feature_loaders):
            if isinstance(feature_loader, str):
                self.feature_loaders[idx] = ReadValueFromCSVLoader(feature_loader)

        # convert or create list of pre_transformation_adapters
        if pre_transfs is None:
            self.pre_transfs = Adapter(seed=69)
        else:
            self.pre_transfs = pre_transfs

        # convert or create list of pre_transformation_adapters
        if da_transfs is None:
            self.da_transfs = Adapter()
        else:
            self.da_transfs = da_transfs

        # read csv file
        self.df = pd.read_csv(os.path.join(path_to_csv))

    def return_collate_fn_(self):
        raise NotImplementedError("")

    def __getitem__(self, idx):

        # get asked row
        row = self.df.iloc[idx]

        # load data
        images = [img_loader(row, self.path_to_images) for img_loader in self.image_loaders]
        features = [
            feature_loader(row, self.path_to_images) for feature_loader in self.feature_loaders
        ]

        if self.seed is not None:
            # save random state to reactivate this state after the call
            saved_seed_state = get_random_seed()
            # set seets
            set_random_seed_with_int((1 + self.seed + self.seed_increment) * int(1e9))
            # increase seed increment to use a new random seed at next call
            self.seed_increment += 1

        # pre transform
        images = self.pre_transfs(images, idx)

        # da transforms
        images = self.da_transfs(images, idx)

        if self.seed is not None:
            # reactivate random state
            set_random_seed(*saved_seed_state)

        if self.return_data_rows is False:
            return images, features
        else:
            return images, features, row
