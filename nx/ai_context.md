# django-nx 0.7.0 — AI API context

django-nx provides small, opinionated extensions for Django models and Django
REST Framework. Treat the API listed here as public. Prefer it over inspecting
implementation files.

## Imports

Use the top-level package:

```python
import nx
```

`from nx import nx` remains compatible but is legacy. DRF helpers are available
under `nx.drf`; `nx.Router` is also exported at the top level.

## Model base and queryset

```python
class Product(nx.Model):
    name = nx.CharField("Name")
```

- `nx.Model`: abstract Django model with `created_at`, `updated_at`, and
  `is_deleted`. Unless explicitly configured, its table name is
  `{app_label}_{snake_case_model_name}`.
- `nx.QuerySet.valid()`: filter the configured deletion field to `False` for a
  BooleanField, otherwise `0`.
- `nx.QuerySet.invalid()`: filter the deletion field to `True` for a
  BooleanField, otherwise `1`.
- The deletion field name is read from `Model.Meta.deleted_field` and defaults
  to `is_deleted`.

## Model fields

All field classes accept the corresponding Django field arguments. When
`help_text` is omitted, relationship and scalar fields generally derive it from
`verbose_name`.

| API | Added defaults or behavior |
| --- | --- |
| `nx.CharField` | `default=""`, `blank=True`, `max_length=128` |
| `nx.TextField` | `default=""`, `blank=True` |
| `nx.IntegerField` | Django IntegerField with automatic help text |
| `nx.MoneyField` | `max_digits=18`, `decimal_places=2`, `default=Decimal("0")` |
| `nx.BooleanField` | `default=False`, `blank=True` |
| `nx.DateField` | `null=True`, `blank=True` |
| `nx.DateTimeField` | `null=True`, `blank=True` |
| `nx.IntChoiceField` | Requires `choices`; defaults to the first choice |
| `nx.TextChoiceField` | Requires `choices`; `max_length=64`; defaults to first choice |
| `nx.ForeignKey` | `on_delete=CASCADE`, `null=True`, `blank=True`, `default=None` |
| `nx.OneToOne` | Same defaults as `ForeignKey` |
| `nx.ManyToMany` | `blank=True`, `default=None` |
| `nx.ShadowForeignKey` | `ForeignKey` defaults plus `db_constraint=False` |
| `nx.ShadowOneToOne` | `OneToOne` defaults plus `db_constraint=False` |
| `nx.ShadowManyToMany` | `ManyToMany` defaults plus `db_constraint=False` |
| `nx.ObjectField` | JSONField with `default=dict`, `blank=True` |
| `nx.ArrayField` | JSONField with `default=list`, `blank=True` |
| `nx.ShortUUIDField` | Auto-generated, URL-safe 22-character UUID string |

Choice fields accept a Django Choices class or a list of `(value, label)`
pairs:

```python
class Product(nx.Model):
    status = nx.IntChoiceField("Status", choices=ProductStatus)
```

## Django REST Framework

```python
class ProductSerializer(
    nx.drf.AutoInstanceLookupMixin,
    serializers.ModelSerializer,
):
    price = nx.drf.MoneyField()
    quantity = nx.drf.QuantityField()
    display_name = nx.drf.MethodField()
```

- `nx.drf.MoneyField`: DecimalField with `max_digits=18` and
  `decimal_places=2`.
- `nx.drf.QuantityField`: IntegerField with `min_value=0`.
- `nx.drf.MethodField`: alias subclass of SerializerMethodField.
- `nx.drf.AutoInstanceLookupMixin`: before saving, uses an input `id` to find
  and assign an existing `Meta.model` instance when no instance was supplied.
- `nx.drf.ListMetadataMixin`: calls `get_list_metadata(request, queryset,
  response)` during list responses. With `list_metadata_root` set, metadata is
  placed below that key; otherwise it is merged into the response root.

## Router

```python
router = nx.Router()
router.register("products", ProductViewSet)
```

`nx.Router` is a DRF DefaultRouter with no trailing slash by default. If
`basename` is omitted, `register()` derives it from the singular form of
`prefix`; the example above uses `product`. An explicit basename always wins.
The same class is available as `nx.drf.Router`.

## Utilities

```python
from nx.utils import get_stat_datetime_range

ranges = get_stat_datetime_range()
```

`get_stat_datetime_range()` returns a `StatDatetimeRange` dataclass containing
inclusive `(start, end)` tuples for `today`, `week`, `month`, and `year`. It
respects Django's `USE_TZ` setting.

## Compatibility and boundaries

- Python: 3.9 or newer.
- Django: 3.2 through versions below 6.1.
- Django REST Framework: 3.12.4 through versions below 3.18.
- Do not depend on names omitted from `nx.__all__`, `nx.drf.__all__`, or this
  document.
- Consult implementation source only when behavior is absent from this public
  contract or while diagnosing a django-nx defect.
