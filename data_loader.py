import os
import torch
import torch.utils.data as data
from PIL import Image
import numpy as np
import pandas as pd
import ast
import utils


def get_loader(transform,
               mode='train',
               batch_size=1,
               start_word="<start>",
               end_word="<end>",
               num_workers=0
               ):
    """Returns the data loader.
    Args:
      transform: Image transform.
      mode: One of 'train' or 'test'.
      batch_size: Batch size (if in testing mode, must have batch_size=1).
      start_word: Special word denoting sentence start.
      end_word: Special word denoting sentence end.
      num_workers: Number of subprocesses to use for data loading
    """

    # Based on mode (train, val, test), obtain img_folder and annotations_file.
    if mode == 'train':
        spectrogram_folder = 'train_set/spectrogram'
        annotations_file = 'train_set/annotations.csv'
    if mode == 'test':
        assert batch_size == 1, "Please change batch_size to 1 if testing your model."
        spectrogram_folder = 'test_set'
        annotations_file = None # TODO remove this but take note its fed into Dataset

    # Spectrogram-Dance dataset.
    dataset = TikTokDataset(transform=transform,
                          mode=mode,
                          batch_size=batch_size,
                          start_word=start_word,
                          end_word=end_word,
                          annotations_file=annotations_file,
                          spectrogram_folder=spectrogram_folder)

    if mode == 'train':
        # data loader for TikTok dataset.
        data_loader = data.DataLoader(dataset=dataset,
                                      num_workers=num_workers,
                                      shuffle=True)
    else:
        data_loader = data.DataLoader(dataset=dataset,
                                      batch_size=dataset.batch_size,
                                      shuffle=True,
                                      num_workers=num_workers)

    return data_loader


class TikTokDataset(data.Dataset):  # Map-style dataset

    def __init__(self, transform, mode, batch_size, start_word,
                 end_word, annotations_file, spectrogram_folder):
        self.transform = transform
        self.mode = mode
        self.batch_size = batch_size
        self.spectrogram_folder = spectrogram_folder
        if self.mode == 'train':
            self.annotations = pd.read_csv(
                annotations_file) 
            self.num_vids = len(self.annotations.index)
        else:
            spectrograms = os.listdir(self.spectrogram_folder)
            self.paths = [self.spectrogram_folder + "/" + item for item in spectrograms]

    def __getitem__(self, idx):
        # obtain image and caption if in training mode
        if self.mode == 'train':
            # remove .mp4 in index
            spectrogram_filename = os.path.basename(
                self.annotations.iloc[idx, 0])
            spectrogram_basename = os.path.splitext(spectrogram_filename)[0]
            # construct spectrogram path
            spectrogram_path = os.path.join(self.spectrogram_folder,
                                            spectrogram_basename + ".png")
            pdseries = self.annotations.iloc[idx, 1:]

            # Convert spectrogram to tensor and pre-process using transform
            spectrogram = Image.open(spectrogram_path).convert('RGB')
            spectrogram = self.transform(spectrogram)

            # If I later on decide to put coordinates for each joint under individual headers, I can process them here.
            pose_coordinates = utils.concatenate_arrays(
                pdseries)

            # return pre-processed image and caption tensors
            return spectrogram, pose_coordinates

        # obtain spectrogram if in test mode
        else:
            path = self.paths[idx]

            # Convert image to tensor and pre-process using transform
            PIL_image = Image.open(path).convert('RGB')
            orig_spectrogram = np.array(PIL_image)
            spectrogram = self.transform(PIL_image)

            # return original image and pre-processed image tensor
            return orig_spectrogram, spectrogram

    def __len__(self):
        if self.mode == 'train':
            return len(self.annotations)
        else:
            return len(self.paths)
