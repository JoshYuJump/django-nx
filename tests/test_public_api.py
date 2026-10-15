import nx
from nx.models import business_fields, fields


def test_recommended_top_level_api():
    assert nx.Model is nx.nx.Model
    assert nx.CharField is nx.nx.CharField
    assert nx.Router is nx.nx.Router
    assert nx.Router is nx.drf.Router


def test_public_api_is_explicit():
    assert set(nx.__all__) == {
        "ArrayField",
        "BooleanField",
        "CharField",
        "CodeField",
        "DateField",
        "DateTimeField",
        "EmailField",
        "ForeignKey",
        "IntChoiceField",
        "IntegerField",
        "ManyToMany",
        "Model",
        "MoneyField",
        "NameField",
        "ObjectField",
        "OneToOne",
        "PercentField",
        "PhoneField",
        "QuantityField",
        "QuerySet",
        "RemarkField",
        "SequenceField",
        "Router",
        "ShadowForeignKey",
        "ShadowManyToMany",
        "ShadowOneToOne",
        "ShortUUIDField",
        "TextChoiceField",
        "TextField",
        "UrlField",
        "WeightField",
        "drf",
        "nx",
    }


def test_business_fields_are_exported_at_each_public_path():
    for name in business_fields.__all__:
        field_type = getattr(business_fields, name)
        assert getattr(nx.models, name) is field_type
        assert getattr(nx.nx, name) is field_type
        assert getattr(nx, name) is field_type

    assert fields.MoneyField is business_fields.MoneyField
    legacy_exports = {}
    exec("from nx.models.fields import *", legacy_exports)
    assert legacy_exports["MoneyField"] is business_fields.MoneyField
