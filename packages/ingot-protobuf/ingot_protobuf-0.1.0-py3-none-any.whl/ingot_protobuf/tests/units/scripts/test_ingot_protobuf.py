import typing as t
from unittest import TestCase

from ingots.tests.units.scripts.test_base import BaseDispatcherTestsMixin

from ingot_protobuf.scripts.ingot_protobuf import IngotProtobufDispatcher

__all__ = ("IngotProtobufDispatcherTestsMixin",)


class IngotProtobufDispatcherTestsMixin(BaseDispatcherTestsMixin):
    """Contains tests for the IngotProtobufDispatcher class and checks it."""

    tst_cls: t.Type = IngotProtobufDispatcher
    tst_builder_name = "test"


class IngotProtobufDispatcherTestCase(IngotProtobufDispatcherTestsMixin, TestCase):
    """Checks the IngotProtobuf class."""
