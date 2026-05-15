"""
Custom Django model fields with enhanced defaults and behaviors.

This module provides extended versions of Django's model fields with:

- Automatic help_text generation from verbose_name
- Sensible default values for common use cases
- Specialized fields for money/decimal amounts
- Choice field variants for integer and text options

Available Fields
----------------

:CharField: CharField with empty string default and auto help_text
:IntegerField: IntegerField with auto help_text support
:MoneyField: DecimalField configured for monetary amounts
:IntChoiceField: SmallIntegerField for choice options
:TextChoiceField: CharField for text-based choices
"""

from decimal import Decimal

from django.db import models


class CharField(models.CharField):
    """
    A CharField that defaults to an empty string and allows blank values.
    This is useful for character fields where you want to avoid NULL values in the database
    and have a consistent empty string as the default.

    If help_text is not provided, it will use the verbose_name as help_text.

    default max_length is 128
    """

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("default", "")
        kwargs.setdefault("blank", True)
        kwargs.setdefault("max_length", 128)

        # If help_text not provided, use verbose_name when available
        if "help_text" not in kwargs and "verbose_name" in kwargs:
            kwargs["help_text"] = kwargs["verbose_name"]

        super().__init__(*args, **kwargs)


class IntegerField(models.IntegerField):
    """

    If help_text is not provided, it will use the verbose_name as help_text.

    """

    def __init__(self, *args, **kwargs):
        # If help_text is not provided, use verbose_name as help_text
        if "help_text" not in kwargs and "verbose_name" in kwargs:
            kwargs["help_text"] = kwargs["verbose_name"]

        super().__init__(*args, **kwargs)


class MoneyField(models.DecimalField):
    """
    MoneyField for monetary amounts using DECIMAL under the hood.

    :param verbose_name: Human-readable name for the field
    :param max_digits: Maximum number of digits (default: 18)
    :param decimal_places: Number of decimal places (default: 2)
    :param default: Default value (default: Decimal('0'))

    Example::

        amount = MoneyField('金额')
        tax = MoneyField('税额', max_digits=14, decimal_places=4)
    """

    def __init__(self, verbose_name=None, *args, **kwargs):
        # Sensible defaults; allow override by explicit kwargs
        kwargs["max_digits"] = kwargs.get("max_digits", 18)
        kwargs["decimal_places"] = kwargs.get("decimal_places", 2)
        kwargs["default"] = kwargs.get("default", Decimal("0"))

        # If help_text not provided, mirror verbose_name when available
        if (
            "help_text" not in kwargs
            and "verbose_name" in kwargs
            and kwargs["verbose_name"]
        ):
            kwargs["help_text"] = kwargs["verbose_name"]

        super().__init__(verbose_name, *args, **kwargs)


class TextField(models.TextField):
    """
    A TextField that defaults to an empty string and allows blank values.
    This is useful for character fields where you want to avoid NULL values in the database
    and have a consistent empty string as the default.

    If help_text is not provided, it will use the verbose_name as help_text.
    """

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("default", "")
        kwargs.setdefault("blank", True)

        # If help_text not provided, use verbose_name when available
        if "help_text" not in kwargs and "verbose_name" in kwargs:
            kwargs["help_text"] = kwargs["verbose_name"]

        super().__init__(*args, **kwargs)


class IntChoiceField(models.SmallIntegerField):
    """
    A SmallIntegerField that present as Choice Field.

    If help_text is not provided, it will use the verbose_name as help_text.
    """

    def __init__(self, verbose_name=None, choices=None, *args, **kwargs):
        if choices is not None:
            kwargs["choices"] = choices

        # If help_text not provided, use verbose_name when available
        if "help_text" not in kwargs and verbose_name is not None:
            kwargs["help_text"] = verbose_name

        super().__init__(verbose_name, *args, **kwargs)


class TextChoiceField(models.CharField):
    """
    A CharField that present as Choice Field.

    If help_text is not provided, it will use the verbose_name as help_text.

    Default `max_length` is 64
    """

    def __init__(self, verbose_name=None, choices=None, *args, **kwargs):
        if choices is not None:
            kwargs["choices"] = choices
        kwargs.setdefault("max_length", 64)  # Default max length for choice fields

        # If help_text not provided, use verbose_name when available
        if "help_text" not in kwargs and verbose_name is not None:
            kwargs["help_text"] = verbose_name

        super().__init__(verbose_name, *args, **kwargs)
