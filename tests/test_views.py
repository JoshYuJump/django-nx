from rest_framework import serializers, viewsets

from nx import drf


class DefaultSerializer(serializers.Serializer):
    pass


class ListSerializer(serializers.Serializer):
    pass


class ExampleViewSet(drf.SerializerClassesMixin, viewsets.GenericViewSet):
    serializer_class = DefaultSerializer
    serializer_classes = {"list": ListSerializer}


def test_serializer_classes_selects_serializer_for_action():
    view = ExampleViewSet()
    view.action = "list"

    assert view.get_serializer_class() is ListSerializer


def test_serializer_classes_falls_back_to_default():
    view = ExampleViewSet()
    view.action = "retrieve"

    assert view.get_serializer_class() is DefaultSerializer


def test_serializer_classes_falls_back_before_action_is_set():
    assert ExampleViewSet().get_serializer_class() is DefaultSerializer
