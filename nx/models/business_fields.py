"""Model fields for common business values."""

from decimal import Decimal
from typing import Any

from django.db import models

from .fields import CharField, TextField

__all__ = [
    "CodeField",
    "EmailField",
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


def _set_help_text(args: tuple[Any, ...], kwargs: dict[str, Any]) -> None:
    if "help_text" not in kwargs:
        verbose_name = kwargs.get("verbose_name", args[0] if args else None)
        if verbose_name:
            kwargs["help_text"] = verbose_name


class MoneyField(models.DecimalField):
    """Monetary amount stored as DECIMAL(18, 2) by default."""

    def __init__(self, verbose_name: Any = None, *args: Any, **kwargs: Any) -> None:
        kwargs.setdefault("max_digits", 18)
        kwargs.setdefault("decimal_places", 2)
        kwargs.setdefault("default", Decimal("0"))
        # Preserve the previous MoneyField help_text behavior.
        if "help_text" not in kwargs and kwargs.get("verbose_name"):
            kwargs["help_text"] = kwargs["verbose_name"]
        super().__init__(verbose_name, *args, **kwargs)


class QuantityField(models.PositiveIntegerField):
    """Nonnegative whole-number quantity, defaulting to zero."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        kwargs.setdefault("default", 0)
        _set_help_text(args, kwargs)
        super().__init__(*args, **kwargs)


class WeightField(models.DecimalField):
    """Weight stored as DECIMAL(18, 3) by default."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        kwargs.setdefault("max_digits", 18)
        kwargs.setdefault("decimal_places", 3)
        kwargs.setdefault("default", Decimal("0"))
        _set_help_text(args, kwargs)
        super().__init__(*args, **kwargs)


class PercentField(models.DecimalField):
    """Percentage points stored as DECIMAL(5, 2) by default."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        kwargs.setdefault("max_digits", 5)
        kwargs.setdefault("decimal_places", 2)
        kwargs.setdefault("default", Decimal("0"))
        _set_help_text(args, kwargs)
        super().__init__(*args, **kwargs)


class SequenceField(models.PositiveIntegerField):
    """Nonnegative ordering value, defaulting to zero."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        kwargs.setdefault("default", 0)
        _set_help_text(args, kwargs)
        super().__init__(*args, **kwargs)


class NameField(CharField):
    """Optional name with a 128-character limit."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        _set_help_text(args, kwargs)
        super().__init__(*args, **kwargs)


class CodeField(CharField):
    """Optional code with a 64-character limit."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        kwargs.setdefault("max_length", 64)
        _set_help_text(args, kwargs)
        super().__init__(*args, **kwargs)


class RemarkField(TextField):
    """Optional free-form remark."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        _set_help_text(args, kwargs)
        super().__init__(*args, **kwargs)


class PhoneField(CharField):
    """Optional phone number stored as text, with a 32-character limit."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        kwargs.setdefault("max_length", 32)
        _set_help_text(args, kwargs)
        super().__init__(*args, **kwargs)


class EmailField(models.EmailField):
    """Optional email address with Django's email validation."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        kwargs.setdefault("default", "")
        kwargs.setdefault("blank", True)
        _set_help_text(args, kwargs)
        super().__init__(*args, **kwargs)


class UrlField(models.URLField):
    """Optional URL with Django's URL validation."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        kwargs.setdefault("default", "")
        kwargs.setdefault("blank", True)
        _set_help_text(args, kwargs)
        super().__init__(*args, **kwargs)
