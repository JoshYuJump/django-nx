from decimal import Decimal

import pytest
from rest_framework import serializers

import nx
from nx.restframework import serializers as nx_serializers


@pytest.mark.parametrize(
    "name,base_type,options",
    [
        (
            "MoneyField",
            serializers.DecimalField,
            {"max_digits": 18, "decimal_places": 2},
        ),
        ("QuantityField", serializers.IntegerField, {"min_value": 0}),
        (
            "WeightField",
            serializers.DecimalField,
            {"max_digits": 18, "decimal_places": 3},
        ),
        (
            "PercentField",
            serializers.DecimalField,
            {"max_digits": 5, "decimal_places": 2},
        ),
        ("SequenceField", serializers.IntegerField, {"min_value": 0}),
        (
            "NameField",
            serializers.CharField,
            {"max_length": 128, "allow_blank": True, "required": False},
        ),
        (
            "CodeField",
            serializers.CharField,
            {"max_length": 64, "allow_blank": True, "required": False},
        ),
        (
            "RemarkField",
            serializers.CharField,
            {"allow_blank": True, "required": False},
        ),
        (
            "PhoneField",
            serializers.CharField,
            {"max_length": 32, "allow_blank": True, "required": False},
        ),
        (
            "EmailField",
            serializers.EmailField,
            {"max_length": 254, "allow_blank": True, "required": False},
        ),
        (
            "UrlField",
            serializers.URLField,
            {"max_length": 200, "allow_blank": True, "required": False},
        ),
    ],
)
def test_drf_business_field_defaults_and_exports(name, base_type, options):
    field_type = getattr(nx.drf, name)
    assert getattr(nx_serializers, name) is field_type
    field = field_type()
    assert isinstance(field, base_type)
    for key, value in options.items():
        assert getattr(field, key) == value


def test_drf_business_field_validation_and_overrides():
    assert nx.drf.WeightField().run_validation("1.234") == Decimal("1.234")
    assert nx.drf.PercentField().run_validation("12.50") == Decimal("12.50")
    assert nx.drf.CodeField().run_validation("") == ""
    assert nx.drf.EmailField().run_validation("") == ""
    assert nx.drf.UrlField().run_validation("") == ""

    with pytest.raises(serializers.ValidationError):
        nx.drf.SequenceField().run_validation(-1)
    with pytest.raises(serializers.ValidationError):
        nx.drf.EmailField().run_validation("invalid")
    with pytest.raises(serializers.ValidationError):
        nx.drf.UrlField().run_validation("invalid")
    with pytest.raises(serializers.ValidationError):
        nx.drf.PhoneField().run_validation("1" * 33)

    assert nx.drf.WeightField(decimal_places=4).decimal_places == 4
    assert nx.drf.NameField(max_length=50, allow_blank=False).max_length == 50
    assert nx.drf.NameField(max_length=50, allow_blank=False).allow_blank is False
    assert nx.drf.NameField(required=True).required is True
