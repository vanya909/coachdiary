from rest_framework import serializers, exceptions

from coachdiary.api.utils.serializers import get_id_serializer_for_model
from drf_writable_nested.serializers import WritableNestedModelSerializer

from .. import models


class StandardSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Standard
        fields = (
            "name",
            "has_numeric_value",
        )
        read_only_fields = (
            "name",
        )

    def update(self, instance, validated_data):
        updated_numeric_value_field = validated_data.get("has_numeric_value")

        if instance.has_numeric_value != updated_numeric_value_field:
            raise exceptions.ValidationError(
                "Нельзя изменять тип норматива после создания."
            )

        return super().update(instance, validated_data)


class LevelSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Level
        fields = (
            "id",
            "level_number",
            "low_level_value",
            "middle_level_value",
            "high_level_value",
        )
        read_only_fields = (
            "id",
        )


class StandardValueSerializer(WritableNestedModelSerializer):
    standard = StandardSerializer()
    student_class = get_id_serializer_for_model(models.StudentClass)
    levels = LevelSerializer(many=True)

    class Meta:
        model = models.StandardValue
        fields = (
            "id",
            "standard",
            "student_class",
            "levels",
        )
        read_only_fields = (
            "id",
        )

    def validate(self, attrs: dict):
        if "standard" in attrs and "has_numeric_value" in attrs["standard"]:
            levels_data = attrs.get("levels", [])
            is_numeric_value = attrs["standard"]["has_numeric_value"]

            if not is_numeric_value and levels_data:
                raise exceptions.ValidationError(
                    "Умение не поддерживает уровни. "
                    "Либо выберите норматив, либо не задавайте уровни.",
                )

        return super().validate(attrs)

    def create(self, validated_data: dict):
        levels_data = validated_data.pop("levels")
        standard = super().create(validated_data)

        for single_level_data in levels_data:
            standard.levels.create(**single_level_data)

        return standard
