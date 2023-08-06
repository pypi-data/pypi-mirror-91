import typing as t
from unittest import TestCase

from ingots.tests.units.scripts.test_base import BaseDispatcherTestsMixin

from ingot_aws.scripts.ingot_aws import IngotAwsDispatcher

__all__ = ("IngotAwsDispatcherTestsMixin",)


class IngotAwsDispatcherTestsMixin(BaseDispatcherTestsMixin):
    """Contains tests for the IngotAwsDispatcher class and checks it."""

    tst_cls: t.Type = IngotAwsDispatcher
    tst_builder_name = "test"


class IngotAwsDispatcherTestCase(IngotAwsDispatcherTestsMixin, TestCase):
    """Checks the IngotAws class."""
