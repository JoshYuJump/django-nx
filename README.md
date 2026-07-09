# django-nx

Lightweight Django field utilities and extensions that reduce boilerplate and enforce sensible defaults.

[![PyPI version](https://badge.fury.io/py/django-nx.svg)](https://pypi.org/project/django-nx/)
[![Python](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/)
[![Django](https://img.shields.io/badge/django-3.2%7C4.x%7C5.x-green)](https://www.djangoproject.com/)

## Installation

```bash
pip install django-nx
```

Requires **Python >= 3.9**, **Django >= 3.2**, and **Django REST Framework >= 3.12.4**.

---

## Quick Start

```python
from nx import nx

class Product(nx.Model):
    name = nx.CharField('Name') # Default max_length=128
    price = nx.MoneyField('Price')
    status = nx.IntChoiceField('Status', choices=ProductStatus)
    tags = nx.ArrayField('Tags')
    metadata = nx.ObjectField('Metadata')
```

---

## Table of Contents

- [Model Fields](#model-fields)
- [Choices](#choices)
- [Base Model](#base-model)
- [QuerySet](#queryset)
- [DRF Serializers](#drf-serializers)
- [DRF Views](#drf-views)
- [Utilities](#utilities)

---

## Model Fields

All fields automatically use `verbose_name` as `help_text` when `help_text` is not explicitly provided.

### Character Fields

| Field | Default | Description |
|-------|---------|-------------|
| `CharField` | `default=""`, `blank=True`, `max_length=128` | String field with empty string default |
| `TextField` | `default=""`, `blank=True` | Long text field with empty string default |
| `TextChoiceField` | `max_length=64`, defaults to first choice | CharField backed by choices enum |

```python
name = nx.CharField('Name', max_length=255)
description = nx.TextField('Description')
priority = nx.TextChoiceField('Priority', choices=PriorityLevel)
```

### Numeric Fields

| Field | Default | Description |
|-------|---------|-------------|
| `IntegerField` | — | Standard integer with auto help_text |
| `MoneyField` | `max_digits=18`, `decimal_places=2`, `default=Decimal('0')` | Decimal field for monetary values |
| `IntChoiceField` | `default=first_choice` | SmallIntegerField backed by choices enum |

```python
quantity = nx.IntegerField('Quantity')
price = nx.MoneyField('Price')           # DECIMAL(18,2)
discount = nx.MoneyField('Discount', max_digits=5, decimal_places=4)
status = nx.IntChoiceField('Status', choices=OrderStatus)
```

### Boolean & Temporal Fields

| Field | Default | Description |
|-------|---------|-------------|
| `BooleanField` | `default=False`, `blank=True` | Boolean flag |
| `DateField` | `null=True`, `blank=True` | Date picker |
| `DateTimeField` | `null=True`, `blank=True` | DateTime picker |

```python
is_active = nx.BooleanField('Is Active')
published_at = nx.DateTimeField('Published At')
birth_date = nx.DateField('Birth Date')
```

### Relationship Fields

| Field | Default | Description |
|-------|---------|-------------|
| `ForeignKey` | `null=True`, `blank=True`, `on_delete=CASCADE` | Standard FK with nullable defaults |
| `OneToOne` | `null=True`, `blank=True`, `on_delete=CASCADE` | One-to-one with nullable defaults |
| `ManyToMany` | `blank=True` | Many-to-many relation |
| `ShadowForeignKey` | `db_constraint=False` | FK without database constraint |
| `ShadowOneToOne` | `db_constraint=False` | One-to-one without DB constraint |
| `ShadowManyToMany` | `db_constraint=False` | Many-to-many without DB constraint |

```python
user = nx.ForeignKey('auth.User', 'User')
profile = nx.OneToOne('accounts.Profile', 'Profile')
tags = nx.ManyToMany('products.Tag', 'Tags')

# Soft / logical foreign key (no DB-level constraint)
legacy_id = nx.ShadowForeignKey('legacy.Model', 'Legacy Ref')
```

### JSON & UUID Fields

| Field | Default | Description |
|-------|---------|-------------|
| `ObjectField` | `default=dict`, `blank=True` | JSONField defaulting to `{}` |
| `ArrayField` | `default=list`, `blank=True` | JSONField defaulting to `[]` |
| `ShortUUIDField` | `max_length=22`, auto-generated | URL-safe concise UUID |

```python
config = nx.ObjectField('Config')
items = nx.ArrayField('Items')
code = nx.ShortUUIDField('Code')
```

---

## Choices

### IntegerChoices

Auto-numbered integer choices starting from `1` (configurable via inner `Meta.start`).

```python
import nx

class Priority(nx.IntegerChoices):
    class Meta:
        start = 1

    LOW = "Low Priority"      # 1
    MEDIUM = "Medium Priority" # 2
    HIGH = "High Priority"    # 3

# Explicit values still work
class Status(nx.IntegerChoices):
    PENDING = "Pending"       # 1
    APPROVED = 10             # 10
    REJECTED = "Rejected"     # 11

# Custom tuples are preserved
class Custom(nx.IntegerChoices):
    NORMAL = "Normal"         # 1
    SPECIAL = (99, "Special") # 99
```

### ZeroBasedChoices

Same as `IntegerChoices`, but defaults to starting from `0`.

```python
class Priority(nx.ZeroBasedChoices):
    LOW = "Low"       # 0
    MEDIUM = "Medium" # 1
    HIGH = "High"     # 2
```

### TextChoices

Auto-lowercased values for consistent API keys.

```python
class TriggerType(nx.TextChoices):
    SALE_AMOUNT = "Sale Amount"   # value = "sale_amount"
    ORDER_COUNT = "Order Count"   # value = "order_count"

# Custom tuples are preserved
class Status(nx.TextChoices):
    ACTIVE = "Active"                  # value = "active"
    CUSTOM = ("custom_key", "Custom")  # value = "custom_key"
```

---

## Base Model

`nx.Model` is an abstract base model that provides:

- **`created_at`** – auto_now_add timestamp
- **`updated_at`** – auto_now timestamp
- **`is_deleted`** – soft-delete flag (default `False`)
- **Auto-generated `db_table`** – `{app_label}_{snake_case_model_name}` via `humps.decamelize`

```python
import nx

class Product(nx.Model):
    name = nx.CharField('Name', max_length=255)

    class Meta:
        app_label = 'shop'
        # db_table = 'shop_product'  # auto-generated if omitted
```

> Explicitly set `Meta.db_table` to skip auto-naming.

---

## QuerySet

`nx.QuerySet` adds soft-delete aware query methods. It reads `deleted_field` from `Model.Meta` (defaults to `is_deleted`).

```python
from nx.models.querysets import QuerySet

class ProductQuerySet(QuerySet):
    pass

class Product(nx.Model):
    ...
    class Meta:
        deleted_field = 'is_deleted'

Product.objects.valid()     # is_deleted=False / 0
Product.objects.invalid()   # is_deleted=True / 1
```

---

## DRF Serializers

| Class | Description |
|-------|-------------|
| `nx.drf.MoneyField` | `DecimalField(max_digits=18, decimal_places=2)` |
| `nx.drf.QuantityField` | `IntegerField(min_value=0)` |
| `nx.drf.MethodField` | Alias for `SerializerMethodField` |
| `nx.drf.AutoInstanceLookupMixin` | Mixin that auto-looks up instance by `id` on save |

```python
from rest_framework import serializers
import nx

class ProductSerializer(nx.drf.AutoInstanceLookupMixin, serializers.ModelSerializer):
    price = nx.drf.MoneyField()
    stock = nx.drf.QuantityField()
    category_name = nx.drf.MethodField()

    class Meta:
        model = Product
        fields = ['id', 'price', 'stock', 'category_name']

    def get_category_name(self, obj):
        return obj.category.name if obj.category else None
```

---

## DRF Views

### ListMetadataMixin

Inject a top-level `meta` object (or any custom root key) into `list` responses.

```python
from rest_framework import viewsets
import nx

class ProductViewSet(nx.drf.ListMetadataMixin, viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    list_metadata_root = "meta"  # optional; omit to merge at top-level

    def get_list_metadata(self, request, queryset, response):
        return {
            "total": queryset.count(),
            "timestamp": timezone.now().isoformat(),
        }
```

**Response shape with `list_metadata_root = "meta"`:**

```json
{
  "count": 100,
  "results": [...],
  "meta": {
    "total": 100,
    "timestamp": "2024-01-15T09:30:00Z"
  }
}
```

**Response shape without `list_metadata_root`:**

```json
{
  "count": 100,
  "results": [...],
  "total": 100,
  "timestamp": "2024-01-15T09:30:00Z"
}
```

---

## Utilities

### get_stat_datetime_range

Returns `today`, `week`, `month`, and `year` datetime ranges respecting `USE_TZ`.

```python
from nx.utils import get_stat_datetime_range

ranges = get_stat_datetime_range()
# ranges.today  -> (2024-01-15 00:00:00, 2024-01-15 23:59:59.999999)
# ranges.week   -> (Mon 00:00:00, Sun 23:59:59.999999)
# ranges.month  -> (1st 00:00:00, last_day 23:59:59.999999)
# ranges.year   -> (Jan 1 00:00:00, Dec 31 23:59:59.999999)
```

---

## Development

```bash
# Install dependencies
uv sync

# Run tests
pytest

# Lint
ruff check .

# Build
uv build
```

---

## License

MIT License — see [LICENSE](LICENSE) for details.
