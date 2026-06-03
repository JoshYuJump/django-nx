from django.db import models


class IntegerChoicesMeta(type(models.IntegerChoices)):
    def __new__(mcls, name, bases, attrs):
        meta = attrs.pop("Meta", None)
        member_names = getattr(attrs, "_member_names", None)
        if member_names and "Meta" in member_names:
            member_names.remove("Meta")
        start = getattr(meta, "start", 1)
        counter = start
        for k, v in list(attrs.items()):
            if k.startswith("_"):
                continue
            if isinstance(v, tuple):
                continue
            if isinstance(v, int):
                counter = max(counter, v + 1)
                continue
            if isinstance(v, str):
                dict.__setitem__(attrs, k, (counter, v))
                counter += 1
        return super().__new__(mcls, name, bases, attrs)


class IntegerChoices(models.IntegerChoices, metaclass=IntegerChoicesMeta):
    """Use inner Meta.start to control first integer (default 1).

    ```python
    class Priority(nx.IntegerChoices):
        class Meta:
            start = 1   # cleaner than top-level _start

        LOW = "Low Priority"
        MEDIUM = "Medium Priority"
        HIGH = "High Priority"
    ```
    """

    pass


class LowerTextChoicesMeta(type(models.TextChoices)):
    def __new__(mcls, name, bases, attrs):
        for k, v in list(attrs.items()):
            if not k.startswith("_") and isinstance(v, str):
                dict.__setitem__(attrs, k, (k.lower(), v))
        return super().__new__(mcls, name, bases, attrs)


class TextChoices(models.TextChoices, metaclass=LowerTextChoicesMeta):
    pass
