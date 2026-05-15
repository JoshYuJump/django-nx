"""
Nx package - Extended Django model fields and utilities.

This package provides custom Django model fields with enhanced defaults
and behaviors, including automatic help_text generation and specialized
field types for common use cases.

Quick Start
-----------

Import fields directly from the nx package::

    from nx import nx

Available Fields
----------------

:CharField: CharField with empty string default and auto help_text
:IntegerField: IntegerField with auto help_text support
:IntChoiceField: SmallIntegerField for choice options
:TextChoiceField: CharField for text-based choices
:MoneyField: DecimalField configured for monetary amounts
"""

from .models.fields import (
    CharField,
    IntegerField,
    TextField,
    IntChoiceField,
    TextChoiceField,
    MoneyField,
)
from . import restframework as drf
