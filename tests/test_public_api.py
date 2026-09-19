import nx


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
        "DateField",
        "DateTimeField",
        "ForeignKey",
        "IntChoiceField",
        "IntegerField",
        "ManyToMany",
        "Model",
        "MoneyField",
        "ObjectField",
        "OneToOne",
        "QuerySet",
        "Router",
        "ShadowForeignKey",
        "ShadowManyToMany",
        "ShadowOneToOne",
        "ShortUUIDField",
        "TextChoiceField",
        "TextField",
        "drf",
        "nx",
    }
