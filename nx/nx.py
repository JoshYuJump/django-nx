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
    CharField,
    IntegerField,
    TextField,
    BooleanField,
    IntChoiceField,
    TextChoiceField,
    MoneyField,
    ForeignKey,
    OneToOne,
    ManyToMany,
    ObjectField,
    ArrayField,
)
from . import restframework as drf
