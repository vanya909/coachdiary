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
            "id",
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
            "levels"
        )
        read_only_fields = (
            "id",
        )

    def validate(self, attrs: dict):
        if "standard" in attrs and "has_numeric_value" in attrs["standard"]:
            levels_data = attrs.get("levels", [])
            is_numeric_value = attrs["standard"]["has_numeric_value"]

            if is_numeric_value:
                for level in levels_data:
                    if any([level.get('low_level_value') is not None,
                            level.get('middle_level_value') is not None,
                            level.get('high_level_value') is not None]):
                        raise exceptions.ValidationError(
                            "Для навыков не поддерживаются значения уровней. "
                            "Заполните только номер уровня."
                        )
            else:
                for level in levels_data:
                    if not all([level.get('low_level_value') is not None,
                                level.get('middle_level_value') is not None,
                                level.get('high_level_value') is not None]):
                        raise exceptions.ValidationError(
                            "Для нормативов необходимо задать значения уровней: "
                            "Минимальное, Среднее и Лучшее."
                        )

        return super().validate(attrs)

    def create(self, validated_data: dict):
        levels_data = validated_data.pop("levels", [])
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

    def update(self, instance, validated_data):
        request_user = self.context['request'].user

        if instance.class_owner != request_user:
            raise ValidationError("Only the class owner can update this class.")

        # Update instance fields with validated data
        instance.number = validated_data.get('number', instance.number)
        instance.class_name = validated_data.get('class_name', instance.class_name)

        # Ensure the class_owner is set to the current user
        instance.class_owner = request_user

        # Save the updated instance
        instance.save()
        return instance


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

    def update(self, instance, validated_data):
        student_class_data = validated_data.pop('student_class', None)
        request_user = self.context['request'].user

        if student_class_data:
            class_instance, created = models.StudentClass.objects.get_or_create(
                number=student_class_data['number'],
                class_name=student_class_data['class_name'],
                defaults={'class_owner': request_user}
            )

            if not created and class_instance.class_owner != request_user:
                raise ValidationError("Only the class owner can update students in this class.")

            instance.student_class = class_instance

        instance.full_name = validated_data.get('full_name', instance.full_name)
        instance.birthday = validated_data.get('birthday', instance.birthday)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.save()

        return instance


class StudentResultSerializer(serializers.ModelSerializer):
    student_class = FullClassNameSerializer()
    student_standards = StudentStandardSerializer(source='studentstandard_set', many=True)

    class Meta:
        model = models.Student
        fields = ['id', 'full_name', 'student_class', 'birthday', 'gender', 'student_standards']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if representation.get('student_standards'):
            for standard in representation['student_standards']:
                representation.update(standard)
            representation.pop('student_standards')
        return representation


class StudentStandardCreateSerializer(serializers.ModelSerializer):
    student_id = serializers.IntegerField(write_only=True)
    standard_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = models.StudentStandard
        fields = ['student_id', 'standard_id', 'value', 'grade']
        read_only_fields = ['grade']

    def validate(self, data):
        student_id = data.get('student_id')
        standard_id = data.get('standard_id')
        value = data.get('value')

        try:
            student = models.Student.objects.get(id=student_id)
        except models.Student.DoesNotExist:
            raise serializers.ValidationError("Student does not exist")

        try:
            standard = models.Standard.objects.get(id=standard_id)
        except models.Standard.DoesNotExist:
            raise serializers.ValidationError("Standard does not exist")

        if not standard.has_numeric_value:
            data['grade'] = value
        else:
            levels = models.Level.objects.filter(
                standard__standard=standard, gender=student.gender
            ).order_by('level_number')

            if not levels.exists():
                raise serializers.ValidationError("No levels found for this standard and gender")

            grade = None
            for level in levels:
                if value >= level.low_level_value:
                    if value >= level.high_level_value:
                        grade = '5'
                    elif value >= level.middle_level_value:
                        grade = '4'
                    else:
                        grade = '3'
                    break

            if grade is None:
                grade = '2'  # Default to the lowest grade if no level matches

            data['grade'] = grade

        data['student'] = student
        data['standard'] = standard

        return data

    def create(self, validated_data):
        student_standard = models.StudentStandard.objects.create(
            student=validated_data['student'],
            standard=validated_data['standard'],
            value=validated_data['value'],
            grade=validated_data['grade']
        )
        return student_standard
