from typing import Any, Dict, Optional
from rest_framework.response import Response


class ListMetadataMixin:
    """
    Mixin to inject a top-level `meta` object into the list response.
    - Scoped to the `list` action only.
    - Subclasses should override get_list_metadata(request, queryset, response)
      and return a JSON-serializable dict of metadata to merge into response.data['meta'].
    """

    list_metadata_root: Optional[str] = None

    def get_list_metadata(
        self, request, queryset: Optional[Any], response: Optional[Response]
    ) -> Dict[str, Any]:
        """
        Hook to provide metadata for list responses.
        - request: current request object
        - queryset: filtered queryset (may be None if unavailable)
        - response: Response instance returned from super().list(...)
        Should return a plain dict (JSON-serializable).
        """
        return {}

    def list(self, request, *args, **kwargs) -> Response:
        # Call parent list to preserve filtering/pagination/serialization behavior.
        response = super().list(request, *args, **kwargs)

        try:
            queryset = self.filter_queryset(self.get_queryset())
        except Exception:
            queryset = None

        # Call hook to get extra metadata; swallow exceptions to avoid breaking response.
        try:
            extra_meta = self.get_list_metadata(request, queryset, response) or {}
        except Exception:
            extra_meta = {}

        # Assume response.data is dict-like in common DRF usage.
        try:
            data = dict(response.data) if response.data is not None else {}
        except Exception:
            # Fallback: wrap original payload if it isn't dict-like
            original = getattr(response, "data", None)
            data = {"results": original}

        if self.list_metadata_root is None:
            # Merge metadata into top-level response.data (may overwrite same-named keys)
            data.update(extra_meta)
        else:
            # Merge into a dedicated root key (ensure it's a dict)
            root = data.get(self.list_metadata_root) or {}
            if not isinstance(root, dict):
                root = {"value": root}
            root.update(extra_meta)
            data[self.list_metadata_root] = root

        response.data = data
        return response
