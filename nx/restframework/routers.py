from typing import Any, Optional

from rest_framework.routers import DefaultRouter

__all__ = ["Router"]


_UNCOUNTABLE_NOUNS = {
    "data",
    "equipment",
    "fish",
    "information",
    "news",
    "rice",
    "series",
    "sheep",
    "species",
}

_IRREGULAR_NOUNS = {
    "children": "child",
    "feet": "foot",
    "geese": "goose",
    "men": "man",
    "mice": "mouse",
    "people": "person",
    "teeth": "tooth",
    "women": "woman",
}


def _singularize(value: str) -> str:
    """Return a conservative English singular form while preserving case."""
    lower_value = value.lower()
    if lower_value in _UNCOUNTABLE_NOUNS:
        return value

    irregular = _IRREGULAR_NOUNS.get(lower_value)
    if irregular is not None:
        if value.isupper():
            return irregular.upper()
        if value.istitle():
            return irregular.title()
        return irregular

    if lower_value.endswith("ies") and len(value) > 3:
        return value[:-3] + ("Y" if value[-1].isupper() else "y")
    if lower_value.endswith(("ches", "shes", "sses", "xes", "zes")):
        return value[:-2]
    if lower_value.endswith("s") and not lower_value.endswith(("ss", "us", "is")):
        return value[:-1]
    return value


class Router(DefaultRouter):
    """A ``DefaultRouter`` with slashless routes and inferred singular basenames."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        if not args:
            kwargs.setdefault("trailing_slash", False)
        super().__init__(*args, **kwargs)

    def register(
        self, prefix: str, viewset: Any, basename: Optional[str] = None
    ) -> None:
        if basename is None:
            basename = _singularize(prefix)
        return super().register(prefix, viewset, basename)
