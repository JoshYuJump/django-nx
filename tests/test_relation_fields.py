import pytest
from django.db.migrations.writer import MigrationWriter

import nx


@pytest.mark.parametrize("field_type", [nx.ManyToMany, nx.ShadowManyToMany])
@pytest.mark.parametrize("blank", [None, True, False])
@pytest.mark.parametrize("keyword_label", [False, True])
def test_many_to_many_migration_round_trip(field_type, blank, keyword_label):
    options = {} if blank is None else {"blank": blank}
    if keyword_label:
        field = field_type("auth.Group", verbose_name="部门", **options)
    else:
        field = field_type("auth.Group", "部门", **options)

    serialized, imports = MigrationWriter.serialize(field)
    namespace = {}
    for statement in imports:
        exec(statement, namespace)
    restored = eval(serialized, namespace)

    for candidate in (field, field.clone(), restored):
        assert candidate.verbose_name == "部门"
        assert candidate.help_text == "部门"
        assert candidate.blank is (True if blank is None else blank)
        assert candidate.remote_field.db_constraint is (field_type is nx.ManyToMany)
        assert candidate.remote_field.model.lower() == "auth.group"


def test_shadow_many_to_many_explicit_options_survive_clone():
    field = nx.ShadowManyToMany(
        "auth.Group", "部门", blank=False, help_text="选择部门", db_constraint=True
    )

    for candidate in (field, field.clone()):
        assert candidate.verbose_name == "部门"
        assert candidate.blank is False
        assert candidate.help_text == "选择部门"
        assert candidate.remote_field.db_constraint is True
