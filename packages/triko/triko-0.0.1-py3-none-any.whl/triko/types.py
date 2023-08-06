import typing as t
import tensorflow as tf


class TrikoError(Exception):
    pass


TF_REC_ENCODE_FUNC_TYPE = t.Callable[[str, t.Any], t.Dict[str, tf.train.Feature]]
