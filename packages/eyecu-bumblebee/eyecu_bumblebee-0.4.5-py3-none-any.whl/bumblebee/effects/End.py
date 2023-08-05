import cv2
from typing import Union
from ..sources import FileStream
from ..bases import IEffect


class End(IEffect):

    def __init__(self, src: Union[FileStream,IEffect], end: int):
        self.src = src
        self.cap = src.cap
        self.end = end

    def read(self):
        if self.cap.get(cv2.CAP_PROP_POS_FRAMES) > self.end:
            self.cap.release()

        return self.src.read()
