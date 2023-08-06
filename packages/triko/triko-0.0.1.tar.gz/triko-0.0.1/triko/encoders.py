import typing as t
import tensorflow as tf


def tf_rec_bytes_encoder(key: str, value: t.Any):
    return {key: tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))}


def tf_rec_int_encoder(key: str, value: t.Any):
    return {key: tf.train.Feature(int64_list=tf.train.Int64List(value=[value]))}


def tf_rec_float_encoder(key: str, value: t.Any):
    return {key: tf.train.Feature(float_list=tf.train.FloatList(value=[value]))}
