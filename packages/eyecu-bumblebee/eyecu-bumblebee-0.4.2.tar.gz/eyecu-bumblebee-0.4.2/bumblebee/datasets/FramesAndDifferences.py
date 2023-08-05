import numpy as np

from ..bases.IDataset import IDataset


class FramesAndDifferences(IDataset):

    def __init__(self, src, batch_size=64):

        self.src = src

        self.batch_size = batch_size
        self.frames = []
        self.differences = []
        self.current_frame = None
        self._readfirstbatch()

    def get_props(self):
        return self.batch_size, *self.src.get_props()

    def __iter__(self):
        return self

    def _readfirstbatch(self):

        for i in range(self.batch_size):
            if self.current_frame:
                self.frames.append(self.current_frame)
                self.current_frame = super().__next__()
                self.differences = self.current_frame - self.frames[-1]
            else:
                self.current_frame = super().__next__()

    def __len__(self):
        return self.batch_size

    def __next__(self):

        self.frames.append(self.current_frame)
        self.current_frame = super().__next__()
        self.differences.append(self.current_frame - self.frames[-1])

        output = np.zeros((2, self.batch_size, *self.src.get_props()))

        for i in range(self.batch_size):
            output[0, i] = self.frames[i]
            output[1, i] = self.differences[i]

        return output
