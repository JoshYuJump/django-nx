import humps
from django.db import models


class Model(models.Model):
    """
    Abstract base model that auto-sets db_table to: {app_label}_{snake_case_model_name}
    Uses humps.decamelize to convert PascalCase to snake_case.
    Does not override an explicitly set Meta.db_table.
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True

    @classmethod
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        meta = cls._meta

        # If the model already set a custom db_table, leave it alone.
        if getattr(meta, "db_table", None):
            return

        # Convert PascalCase name to snake_case using humps (handles acronyms).
        snake_name = humps.decamelize(cls.__name__)

        # Set db_table without any prefix.
        meta.db_table = f"{meta.app_label}_{snake_name}"
