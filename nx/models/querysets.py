from typing import Optional, Tuple
from django.db import models
from django.db.models import QuerySet as DBQuerySet, BooleanField


class QuerySet(DBQuerySet):
    """
    Only read `deleted_field = "<field_name>"` from Model.Meta.
    Resolution result is cached on model._resolved_deleted_field (process-local).
    Provides valid(), with_deleted(), invalid(), soft_delete().
    """

    def _resolve_deleted_field(self) -> Tuple[Optional[str], Optional[models.Field]]:
        model = self.model
        cached = getattr(model, "_resolved_deleted_field", None)
        if cached is not None:
            return cached

        meta = getattr(model, "Meta", None)
        field_name = getattr(meta, "deleted_field", "is_deleted")
        if not field_name:
            model._resolved_deleted_field = (None, None)
            return None, None

        try:
            field = model._meta.get_field(field_name)
            model._resolved_deleted_field = (field_name, field)
            return field_name, field
        except Exception:
            model._resolved_deleted_field = (None, None)
            return None, None

    def valid(self):
        """
        Return queryset of records not marked as deleted.
        For BooleanField use False; for other types (Only supoort numeric fields) use 0.
        If Model.Meta does not configure deleted_field, return the original QuerySet.
        """
        name, field = self._resolve_deleted_field()
        if isinstance(field, BooleanField):
            return self.filter(**{name: False})
        # Treat NULL as equivalent to 0 by default
        return self.filter(**{name: 0})

    def invalid(self):
        """
        Return queryset of records marked as deleted.
        BooleanField -> True, others -> 1
        """
        name, field = self._resolve_deleted_field()
        if isinstance(field, BooleanField):
            return self.filter(**{name: True})
        return self.filter(**{name: 1})
