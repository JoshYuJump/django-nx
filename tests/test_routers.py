from rest_framework.viewsets import ViewSet

from nx import nx


class ExampleViewSet(ViewSet):
    def list(self, request):
        pass


def test_router_disables_trailing_slashes():
    router = nx.Router()
    router.register("users", ExampleViewSet)

    assert nx.drf.Router is nx.Router
    assert router.trailing_slash == ""
    assert str(router.urls[0].pattern) == "^users$"


def test_router_uses_singular_prefix_as_basename():
    router = nx.Router()

    router.register("users", ExampleViewSet)
    router.register("categories", ExampleViewSet)

    assert router.registry == [
        ("users", ExampleViewSet, "user"),
        ("categories", ExampleViewSet, "category"),
    ]


def test_router_preserves_explicit_basename():
    router = nx.Router()

    router.register("people", ExampleViewSet, basename="account")

    assert router.registry == [("people", ExampleViewSet, "account")]
