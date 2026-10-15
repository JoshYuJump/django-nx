from typing import Any

from rest_framework import serializers

__all__ = [
    "AutoInstanceLookupMixin",
    "CodeField",
    "EmailField",
    "MethodField",
    "MoneyField",
    "NameField",
    "PercentField",
    "PhoneField",
    "QuantityField",
    "RemarkField",
    "SequenceField",
    "UrlField",
    "WeightField",
]


class MoneyField(serializers.DecimalField):
    """
    A DecimalField pre-configured for monetary values with 18 digits and 2 decimal places.
    """

    def __init__(self, **kwargs: Any) -> None:
        kwargs.setdefault("max_digits", 18)
        kwargs.setdefault("decimal_places", 2)
        super().__init__(**kwargs)


class MethodField(serializers.SerializerMethodField):
    """Short alias for DRF's SerializerMethodField."""


class QuantityField(serializers.IntegerField):
    """
    An IntegerField pre-configured for quantity values with a minimum value of 0.
    """

    def __init__(self, **kwargs: Any) -> None:
        kwargs.setdefault("min_value", 0)
        super().__init__(**kwargs)


class WeightField(serializers.DecimalField):
    """Decimal weight with 18 digits and 3 decimal places by default."""

    def __init__(self, **kwargs: Any) -> None:
        kwargs.setdefault("max_digits", 18)
        kwargs.setdefault("decimal_places", 3)
        super().__init__(**kwargs)


class PercentField(serializers.DecimalField):
    """Percentage points with 5 digits and 2 decimal places by default."""

    def __init__(self, **kwargs: Any) -> None:
        kwargs.setdefault("max_digits", 5)
        kwargs.setdefault("decimal_places", 2)
        super().__init__(**kwargs)


class SequenceField(serializers.IntegerField):
    """Nonnegative ordering value."""

    def __init__(self, **kwargs: Any) -> None:
        kwargs.setdefault("min_value", 0)
        super().__init__(**kwargs)


class NameField(serializers.CharField):
    """Optional name with a 128-character limit."""

    def __init__(self, **kwargs: Any) -> None:
        kwargs.setdefault("max_length", 128)
        kwargs.setdefault("allow_blank", True)
        kwargs.setdefault("required", False)
        super().__init__(**kwargs)


class CodeField(serializers.CharField):
    """Optional code with a 64-character limit."""

    def __init__(self, **kwargs: Any) -> None:
        kwargs.setdefault("max_length", 64)
        kwargs.setdefault("allow_blank", True)
        kwargs.setdefault("required", False)
        super().__init__(**kwargs)


class RemarkField(serializers.CharField):
    """Optional free-form remark."""

    def __init__(self, **kwargs: Any) -> None:
        kwargs.setdefault("allow_blank", True)
        kwargs.setdefault("required", False)
        super().__init__(**kwargs)


class PhoneField(serializers.CharField):
    """Optional phone number with a 32-character limit."""

    def __init__(self, **kwargs: Any) -> None:
        kwargs.setdefault("max_length", 32)
        kwargs.setdefault("allow_blank", True)
        kwargs.setdefault("required", False)
        super().__init__(**kwargs)


class EmailField(serializers.EmailField):
    """Optional email address with a 254-character limit."""

    def __init__(self, **kwargs: Any) -> None:
        kwargs.setdefault("max_length", 254)
        kwargs.setdefault("allow_blank", True)
        kwargs.setdefault("required", False)
        super().__init__(**kwargs)


class UrlField(serializers.URLField):
    """Optional URL with a 200-character limit."""

    def __init__(self, **kwargs: Any) -> None:
        kwargs.setdefault("max_length", 200)
        kwargs.setdefault("allow_blank", True)
        kwargs.setdefault("required", False)
        super().__init__(**kwargs)


class AutoInstanceLookupMixin:
    """Look up an existing model instance by input ``id`` before saving."""

    def save(self, **kwargs: Any) -> Any:
        pk = self.validated_data.get("id") if hasattr(self, "validated_data") else None
        if not pk:
            pk = self.initial_data.get("id")
        if not self.instance and pk:
            try:
                self.instance = self.Meta.model.objects.get(pk=pk)
            except self.Meta.model.DoesNotExist:
                pass
        return super().save(**kwargs)
