from typing import Any

from rest_framework import serializers

__all__ = [
    "AutoInstanceLookupMixin",
    "MethodField",
    "MoneyField",
    "QuantityField",
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
