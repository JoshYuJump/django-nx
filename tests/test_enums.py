import pytest  # noqa

from nx.models.enums import IntegerChoices, TextChoices


class TestIntegerChoices:
    def test_auto_numbering_starts_at_one(self):
        class Priority(IntegerChoices):
            LOW = "Low"
            MEDIUM = "Medium"
            HIGH = "High"

        assert Priority.LOW.value == 1
        assert Priority.MEDIUM.value == 2
        assert Priority.HIGH.value == 3

    def test_custom_start_via_meta(self):
        class Priority(IntegerChoices):
            class Meta:
                start = 10

            LOW = "Low"
            MEDIUM = "Medium"

        assert Priority.LOW.value == 10
        assert Priority.MEDIUM.value == 11

    def test_explicit_int_value(self):
        class Status(IntegerChoices):
            PENDING = "Pending"
            APPROVED = 10
            REJECTED = "Rejected"

        assert Status.PENDING.value == 1
        assert Status.APPROVED.value == 10
        assert Status.REJECTED.value == 11

    def test_tuple_value_preserved(self):
        class Status(IntegerChoices):
            PENDING = "Pending"
            CUSTOM = (99, "Custom Label")

        assert Status.PENDING.value == 1
        assert Status.CUSTOM.value == 99
        assert Status.CUSTOM.label == "Custom Label"

    def test_labels(self):
        class Priority(IntegerChoices):
            LOW = "Low Priority"
            MEDIUM = "Medium Priority"

        assert Priority.LOW.label == "Low Priority"
        assert Priority.MEDIUM.label == "Medium Priority"

    def test_choices_method(self):
        class Priority(IntegerChoices):
            LOW = "Low"
            MEDIUM = "Medium"

        assert Priority.choices == [(1, "Low"), (2, "Medium")]


class TestTextChoices:
    def test_auto_lowercase_value(self):
        class TriggerType(TextChoices):
            SALE_AMOUNT = "Sale Amount"
            ORDER_COUNT = "Order Count"

        assert TriggerType.SALE_AMOUNT.value == "sale_amount"
        assert TriggerType.ORDER_COUNT.value == "order_count"

    def test_labels(self):
        class TriggerType(TextChoices):
            SALE_AMOUNT = "Sale Amount"

        assert TriggerType.SALE_AMOUNT.label == "Sale Amount"

    def test_tuple_value_preserved(self):
        class Status(TextChoices):
            ACTIVE = "Active"
            CUSTOM = ("custom_key", "Custom Label")

        assert Status.ACTIVE.value == "active"
        assert Status.CUSTOM.value == "custom_key"
        assert Status.CUSTOM.label == "Custom Label"

    def test_choices_method(self):
        class Color(TextChoices):
            RED = "Red"
            GREEN = "Green"

        assert Color.choices == [("red", "Red"), ("green", "Green")]

    def test_private_not_transformed(self):
        class Foo(TextChoices):
            BAR = "Bar"
            _private = "Private"

        assert Foo.BAR.value == "bar"
        # Single-underscore names are still enum members in Python,
        # but our metaclass skips transformation for them.
        assert Foo._private.value == "Private"
        # Django auto-generates label as key.replace("_", " ").title()
        assert Foo._private.label == " Private"
