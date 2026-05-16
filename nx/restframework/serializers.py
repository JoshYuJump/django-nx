from rest_framework import serializers


class MoneyField(serializers.DecimalField):
    """
    A DecimalField pre-configured for monetary values with 18 digits and 2 decimal places.
    """

    def __init__(self, **kwargs):
        kwargs.setdefault("max_digits", 18)
        kwargs.setdefault("decimal_places", 2)
        super().__init__(**kwargs)


class MethodField(serializers.SerializerMethodField):
    pass
