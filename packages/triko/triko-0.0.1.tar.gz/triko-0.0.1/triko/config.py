import tensorflow as tf
from dataclasses import dataclass

from triko.types import TF_REC_ENCODE_FUNC_TYPE
from triko.encoders import tf_rec_bytes_encoder, tf_rec_int_encoder, tf_rec_float_encoder


@dataclass
class _TfRecConfig:
    tf_type: tf.DType
    tf_rec_encoder: TF_REC_ENCODE_FUNC_TYPE

    @staticmethod
    def int_config() -> "_TfRecConfig":
        return _TfRecConfig(tf_type=tf.int64, tf_rec_encoder=tf_rec_int_encoder)

    @staticmethod
    def float_config(float_32: bool) -> "_TfRecConfig":
        return _TfRecConfig(tf_type=tf.float32 if float_32 else tf.float64, tf_rec_encoder=tf_rec_float_encoder,)

    @staticmethod
    def bytes_config() -> "_TfRecConfig":
        return _TfRecConfig(tf_type=tf.string, tf_rec_encoder=tf_rec_bytes_encoder)
