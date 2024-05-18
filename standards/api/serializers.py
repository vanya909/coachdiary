from rest_framework import serializers, exceptions
from rest_framework.exceptions import ValidationError

from auth.users.api.serializers import UserSerializer
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


class StudentStandardSerializer(serializers.ModelSerializer):
    standard = StandardSerializer()

    class Meta:
        model = models.StudentStandard
        fields = (
            'standard',
            'grade',
            'value')


class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Level
        fields = (
            "id",
            "level_number",
            "low_level_value",
            "middle_level_value",
            "high_level_value",
            "gender"
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
            "levels"

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


class StudentClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.StudentClass
        fields = ("class_name", "number", "recruitment_year")

    def create(self, validated_data):
        request_user = self.context['request'].user
        student_class, created = models.StudentClass.objects.get_or_create(
            number=validated_data['number'],
            class_name=validated_data['class_name'],
            defaults={'class_owner': request_user}
        )

        if not created and student_class.class_owner != request_user:
            raise ValidationError("Only the class owner can add students to this class.")

        return student_class


class FullClassNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.StudentClass
        fields = ('number', 'class_name')


class StudentSerializer(WritableNestedModelSerializer):
    student_class = FullClassNameSerializer()

    class Meta:
        model = models.Student
        fields = ("id", "full_name", "student_class", "birthday", "gender")

    def create(self, validated_data):
        student_class_data = validated_data.pop('student_class')
        request_user = self.context['request'].user

        class_instance, created = models.StudentClass.objects.get_or_create(
            number=student_class_data['number'],
            class_name=student_class_data['class_name'],
            defaults={'class_owner': request_user}
        )

        if not created and class_instance.class_owner != request_user:
            raise ValidationError("Only the class owner can add students to this class.")

        student = models.Student.objects.create(student_class=class_instance, **validated_data)
        return student


class StudentResultSerializer(serializers.ModelSerializer):
    student_class = serializers.SerializerMethodField()
    standard = serializers.SerializerMethodField()
    value = serializers.CharField(source='studentstandard.value')
    grade = serializers.CharField(source='studentstandard.grade')

    class Meta:
        model = models.Student
        fields = ['id', 'full_name', 'student_class', 'birthday', 'gender', 'standard', 'value', 'grade']

    def get_student_class(self, obj):
        return {
            "id": obj.student_class.id,
            "number": obj.student_class.number,
            "class_name": obj.student_class.class_name
        }

    def get_standard(self, obj):
        student_standard = obj.studentstandards.first()  # assuming one-to-one relationship
        return {
            "id": student_standard.standard.id
        }
