import typing as t
import numpy as np
from abc import ABC
from collections import ChainMap
import tensorflow as tf

from triko.config import _TfRecConfig
from triko.types import TrikoError, TF_REC_ENCODE_FUNC_TYPE

RAW = t.TypeVar("RAW")
ENCODED = t.TypeVar("ENCODED")
DECODED = t.TypeVar("DECODED")


class TrikoFeature(ABC, t.Generic[RAW, ENCODED, DECODED]):
    """
    Encapsulates the encoding/decoding process of TFRecord framework.
    The class is based on generic types:
    RAW - a type of data you want to encode.
    ENCODED - to be able to store your data as TFRecord, the raw data must be converted/casted
              to one of the types presented in TF_REC_ENCODE_CONFIG_MAP below.
              Important: Override _encode_raw if RAW and ENCODED are not of the same type
    DECODED - a type of your decoded raw data.
              Important: Override _decode_value if ENCODED and DECODED are not of the same type.

    Example:
        You work on image classification problem and you
        want to save images and labels in TFRecord format.

        For images you use:
        RAW - bytes, you just read images from disk in binary format.
        ENCODED - bytes, so you don't need to override _encode_raw.
        DECODED - np.ndarray, since you want images to be ready for modeling.

        For labels you use:
        RAW - str, because your raw data goes as "cat"/"dog"
        ENCODED - int, so you map string labels to int labels by overriding _encode_raw
        DECODED - int, so you do nothing since ENCODED type is the same.

    Init parameters:
    key: str
        Unique descriptive identifier for a feature
    fixed_len_feature: bool
        Whether you feature is of fixed len (see TFRecord docs).
        Important: only True case is supported for now
    """

    TF_REC_ENCODE_CONFIG_MAP: t.Dict[t.Any, _TfRecConfig] = {
        bool: _TfRecConfig.int_config(),
        int: _TfRecConfig.int_config(),
        np.float32: _TfRecConfig.float_config(float_32=True),
        np.float64: _TfRecConfig.float_config(float_32=False),
        str: _TfRecConfig.bytes_config(),
        bytes: _TfRecConfig.bytes_config(),
    }

    def __init__(self, key: str, fixed_len_feature: bool = True):
        # this is a way to get to actual ENCODED type
        # I don't like the look of it, and also I'm not sure that it's the right way doing that
        ORIG_BASES_IDX = 0
        RAW_ARG_IDX = 0
        ENCODED_ARG_IDX = 1
        DECODED_ARG_IDX = 2
        generic_types = self.__class__.__orig_bases__[ORIG_BASES_IDX].__args__
        raw_type = generic_types[RAW_ARG_IDX]
        encoded_type = generic_types[ENCODED_ARG_IDX]
        decoded_type = generic_types[DECODED_ARG_IDX]
        #

        if not self.TF_REC_ENCODE_CONFIG_MAP.get(encoded_type):
            available_types = list(self.TF_REC_ENCODE_CONFIG_MAP.keys())
            raise TrikoError(f"type ({encoded_type}) is not recognized, available types: {available_types}")

        self._tf_rec_config: _TfRecConfig = self.TF_REC_ENCODE_CONFIG_MAP[encoded_type]
        self._key = key
        self._fixed_len_feature = fixed_len_feature

        self._raw_type: t.Type = raw_type
        self._encoded_type: t.Type = encoded_type
        self._decoded_type: t.Type = decoded_type

        self._must_override_encode = self._raw_type != self._encoded_type
        self._must_override_decode = self._encoded_type != self._decoded_type

    @property
    def key(self) -> str:
        return self._key

    # MAIN METHODS

    @staticmethod
    def encode_features_to_string(
        features: t.List["TrikoFeature"], raw_value_getter: t.Callable[["TrikoFeature"], RAW],
    ) -> str:
        """
        Generates a string representing encoded given features.
        :param features: list of TrikoFeature
            List of features for your problem that you wish to encode and save using TFRecord
        :param raw_value_getter: callable
            Callback that maps TrikoFeature with a raw value. You may distinguish TrikoFeatures by key property.
        :return:
        TFRecord compatible string with encoded features.
        """
        example_features = [feature._encode(raw_value=raw_value_getter(feature)) for feature in features]
        tf_rec_composite_feature = dict(ChainMap(*example_features))
        tf_rec_example = tf.train.Example(features=tf.train.Features(feature=tf_rec_composite_feature))
        return tf_rec_example.SerializeToString()

    @staticmethod
    def decoder(features: t.List["TrikoFeature"]) -> t.Callable[[t.Any], t.Any]:
        """
        Returns a function you should use in combination with TFRecordDataset.
        So before performing any operations on TFRecordDataset, do something like:

        dataset.map(TrikoFeature.decoder(features=features))

        Then you can access your successfuly decoded data the way you want.

        :param features: list of TrikoFeature
            List of features for your problem that you wish to encode and save using TFRecord

        :return:
        Function for decoding TFRecord example.
        """
        features_dict = dict(ChainMap(*[feature._get_decode_config() for feature in features]))

        def _parse_function(proto):
            """
            :param proto:
                Raw data from TFRecord that must be decoded.
            """
            parsed_features = tf.io.parse_single_example(proto, features_dict)

            ready_parsed_features = [
                feature._decode_value(encoded_value=parsed_features[feature._key]) for feature in features
            ]
            return ready_parsed_features

        return _parse_function

    ###

    def _get_decode_config(self) -> t.Dict[str, tf.io.FixedLenFeature]:
        assert self._fixed_len_feature, "Only fixed len features are supported for now"
        return {self._key: tf.io.FixedLenFeature([], self._tf_rec_config.tf_type)}

    def _encode(self, raw_value: RAW) -> t.Dict[str, tf.train.Feature]:
        if not self._validate_raw_value(raw_value=raw_value):
            raise TrikoError(
                f"Feature {self.key} haven't passed the validation, "
                f"check your data/_validate_raw_value func implementation."
            )

        value = self._encode_raw(raw_value=raw_value)

        encoder: TF_REC_ENCODE_FUNC_TYPE = self._tf_rec_config.tf_rec_encoder
        return encoder(self._key, value)

    # OVERRIDE IF NEEDED

    def _encode_raw(self, raw_value: RAW) -> ENCODED:
        if self._must_override_encode:
            self._raise_need_for_custom_encode()

        assert self._raw_type == self._encoded_type

        return raw_value

    def _validate_raw_value(self, raw_value: RAW) -> bool:
        return raw_value is not None

    def _decode_value(self, encoded_value: ENCODED) -> DECODED:
        if self._must_override_decode:
            self._raise_need_for_custom_decode()

        return encoded_value

    ###

    def _raise_need_for_custom_encode(self):
        raise TrikoError(
            f"You must override _encode_raw, since provided raw data "
            f"type {self._raw_type} and encoded data type {self._encoded_type} are different"
        )

    def _raise_need_for_custom_decode(self):
        raise TrikoError(
            f"You must override _decode_value, since provided encoded data "
            f"type {self._encoded_type} and decoded data type {self._decoded_type} are different"
        )
