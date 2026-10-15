from decimal import Decimal

from django.db import models
from django.core.exceptions import ValidationError
import pytest

import nx


@pytest.mark.parametrize(
    "field_type,base_type,attributes",
    [
        (
            nx.MoneyField,
            models.DecimalField,
            {"max_digits": 18, "decimal_places": 2, "default": Decimal("0")},
        ),
        (nx.QuantityField, models.PositiveIntegerField, {"default": 0}),
        (
            nx.WeightField,
            models.DecimalField,
            {"max_digits": 18, "decimal_places": 3, "default": Decimal("0")},
        ),
        (
            nx.PercentField,
            models.DecimalField,
            {"max_digits": 5, "decimal_places": 2, "default": Decimal("0")},
        ),
        (nx.SequenceField, models.PositiveIntegerField, {"default": 0}),
        (
            nx.NameField,
            models.CharField,
            {"max_length": 128, "default": "", "blank": True},
        ),
        (
            nx.CodeField,
            models.CharField,
            {"max_length": 64, "default": "", "blank": True},
        ),
        (nx.RemarkField, models.TextField, {"default": "", "blank": True}),
        (
            nx.PhoneField,
            models.CharField,
            {"max_length": 32, "default": "", "blank": True},
        ),
        (
            nx.EmailField,
            models.EmailField,
            {"max_length": 254, "default": "", "blank": True},
        ),
        (
            nx.UrlField,
            models.URLField,
            {"max_length": 200, "default": "", "blank": True},
        ),
    ],
)
def test_business_field_defaults_and_migration_round_trip(
    field_type, base_type, attributes
):
    field = field_type("Example")
    assert isinstance(field, base_type)
    for key, value in attributes.items():
        assert getattr(field, key) == value

    _, path, args, kwargs = field.deconstruct()
    assert path == f"nx.models.business_fields.{field_type.__name__}"
    restored = field_type(*args, **kwargs)
    for key, value in attributes.items():
        assert getattr(restored, key) == value


def test_business_field_options_and_validation():
    assert (
        nx.MoneyField(
            "Price", max_digits=10, decimal_places=4, default=Decimal("1")
        ).max_digits
        == 10
    )
    assert nx.WeightField("Weight", decimal_places=6).decimal_places == 6
    assert nx.CodeField("Code", max_length=20, blank=False).max_length == 20
    assert nx.EmailField("Email", blank=False).blank is False
    assert nx.NameField("Name").help_text == "Name"

    with pytest.raises(ValidationError):
        nx.EmailField().run_validators("invalid")
    with pytest.raises(ValidationError):
        nx.UrlField().run_validators("invalid")
