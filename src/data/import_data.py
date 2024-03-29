import os
import sys
from functools import lru_cache

if os.getcwd() not in sys.path:
    sys.path.append(os.getcwd())
from src.utils import (
    import_from_S3
)
from src.configs import S3_configs


@lru_cache(maxsize=1)
def import_data():
    params = S3_configs()
    _df = import_from_S3(params)
    return _df.apply(
        lambda x: x.apply(
            lambda z: z.decode("utf-8") if isinstance(z, bytes) else z),
        axis=1)
