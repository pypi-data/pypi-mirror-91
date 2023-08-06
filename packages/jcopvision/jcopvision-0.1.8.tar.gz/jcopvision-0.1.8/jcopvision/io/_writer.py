from enum import Enum

import cv2
from jcopvision.exception import IncorrectExtensionError
from jcopvision.utils._denorm import denorm_pixel


class Interpolation(Enum):
    nearest, bilinear, bicubic, area = range(4)


class BaseWriter:
    def __init__(self, output_path, width, height, fps, fourcc, interpolation):
        self.width = int(width)
        self.height = int(height)
        self._writer = cv2.VideoWriter(output_path, fourcc, fps, (self.width, self.height))

        if interpolation in Interpolation.__members__:
            self.interpolation = Interpolation[interpolation]
        else:
            raise ValueError(f"Only supports ({', '.join(Interpolation.__members__)}) interpolation")

    def write(self, frame, mode="bgr"):
        frame = denorm_pixel(frame)

        if mode == "rgb":
            frame = frame[..., ::-1]

        h, w, c = frame.shape
        if (w != self.width) | (h != self.height):
            frame = cv2.resize(frame, (self.width, self.height))
        self._writer.write(frame)

    def close(self):
        self._writer.release()


class MP4Writer(BaseWriter):
    """
    A video writer with mp4 compression.

    === Example Usage ===
    media = MediaReader("example.mp4")
    writer = MP4Writer("output.mp4", media.width, media.height, media.frame_rate)

    === Input ===
    output_path: str
        path ended with .mp4 in its name

    width: int or float
        output video width

    height: int or float
        output video height

    fps: float
        output video frame rate

    interpolation: {nearest, bilinear, bicubic, area}
        interpolation when resizing. Only used when the input frame is different with the output shape
    """
    def __init__(self, output_path, width, height, fps, interpolation="area"):
        if not output_path.endswith(".mp4"):
            raise IncorrectExtensionError("output_path should have .mp4 extension")

        fourcc = cv2.VideoWriter_fourcc(*"MP4V")
        super().__init__(output_path, width, height, fps, fourcc, interpolation)


class AVIWriter(BaseWriter):
    """
    A video writer with avi compression.

    === Example Usage ===
    media = MediaReader("example.avi")
    writer = MP4Writer("output.avi", media.width, media.height, media.frame_rate)

    === Input ===
    output_path: str
        path ended with .avi in its name

    width: int or float
        output video width

    height: int or float
        output video height

    fps: float
        output video frame rate

    interpolation: {nearest, bilinear, bicubic, area}
        interpolation when resizing. Only used when the input frame is different with the output shape
    """
    def __init__(self, output_path, width, height, fps, interpolation="area"):
        if not output_path.endswith(".avi"):
            raise IncorrectExtensionError("output_path should have .avi extension")

        fourcc = cv2.VideoWriter_fourcc(*"MJPG")
        super().__init__(output_path, width, height, fps, fourcc, interpolation)

