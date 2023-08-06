import os
import array
import numpy as np
from PIL import Image
from pydantic import BaseModel

from kw6 import types

N_BYTES_DOUBLE = 8
IM_HDR_SIZE = 34


class CameraHeader(BaseModel):
    camera_version: str
    camera_index: types.CAMERA_INDEX
    scale_height: str
    scale_length: str
    xMM: str
    yMM: str
    xPixC: str
    yPixC: str
    sub_sample: str
    expoMS: str
    x0: str
    y0: str
    width: int
    height: int
    _10xReserved: str
    _5xWearLeft: str
    _5xWearRight: str

    class Config:
        allow_mutation = False

    def from_stream_(stream):
        names = CameraHeader.__fields__.keys()
        return CameraHeader(**dict(zip(
            names,
            array.array('d', stream.read(N_BYTES_DOUBLE * len(names)))
        )))


class Camera(BaseModel):
    header: CameraHeader
    image: Image.Image

    class Config:
        arbitrary_types_allowed = True
        allow_mutation = False

    @staticmethod
    def from_stream_(stream):
        header = CameraHeader.from_stream_(stream)
        return Camera(
            header=header,
            image=Camera.image_(stream, header),
        )

    @staticmethod
    def image_(stream, header):
        n_rows = header.height
        n_cols = header.width
        stream.read(N_BYTES_DOUBLE * (IM_HDR_SIZE - len(header.dict())))

        image_data = np.array(
            array.array('B', stream.read(n_rows * n_cols))
        ).reshape(n_rows, n_cols)

        return Image.fromarray(image_data)
