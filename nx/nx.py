"""
Nx package - Extended Django model fields and utilities.

This package provides custom Django model fields with enhanced defaults
and behaviors, including automatic help_text generation and specialized
field types for common use cases.

Quick Start
-----------

Import fields directly from the nx package::

    from nx import nx


"""

from .models.fields import (
    CharField,  # noqa: F401
    IntegerField,  # noqa: F401
    TextField,  # noqa: F401
    BooleanField,  # noqa: F401
    DateField,  # noqa: F401
    DateTimeField,  # noqa: F401
    IntChoiceField,  # noqa: F401
    TextChoiceField,  # noqa: F401
    MoneyField,  # noqa: F401
    ForeignKey,  # noqa: F401
    OneToOne,  # noqa: F401
    ManyToMany,  # noqa: F401
    ShadowForeignKey,  # noqa: F401
    ShadowOneToOne,  # noqa: F401
    ShadowManyToMany,  # noqa: F401
    ObjectField,  # noqa: F401
    ArrayField,  # noqa: F401
    ShortUUIDField,  # noqa: F401
)
from .models.base import Model  # noqa: F401
from . import restframework as drf  # noqa: F401
