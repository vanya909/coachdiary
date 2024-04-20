import datetime
from django.db import models
from django_softdelete.models import SoftDeleteModel
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError


class StudentClass(SoftDeleteModel):
    number = models.IntegerField(
        verbose_name="Номер учебного класса",
        validators=(
            MinValueValidator(1),
            MaxValueValidator(11),
        ),
    )
    class_name = models.CharField(
        max_length=1,
        verbose_name="Буква учебного класса",
        help_text="А, Б, В, ..."
    )
    class_owner = models.ForeignKey(
        "users.User",
        on_delete=models.PROTECT,
        verbose_name="Куратор класса",
    )
    recruitment_year = models.IntegerField(
        verbose_name="Год набора",
        validators=(
            MinValueValidator(2000),
        )
    )

    class Meta:
        unique_together = (
            "number",
            "class_name",
        )

    def clean(self):
        if self.recruitment_year > datetime.date.today().year:
            raise ValidationError(
                "Год набора не может быть позднее текущего года.",
            )

    def __str__(self) -> str:
        return f"{self.number}{self.class_name}"


class Student(SoftDeleteModel):
    full_name = models.CharField(
        max_length=1024,
        verbose_name="Полное имя ученика",
        help_text="Петров Петр Петрович",
    )
    student_class = models.ForeignKey(
        StudentClass,
        on_delete=models.CASCADE,
        verbose_name="Класс ученика",
    )
    birthday = models.DateField(
        verbose_name="Дата рождения ученика",
    )

    class Gender(models.TextChoices):
        male = "m", "Мужской"
        female = "f", "Женский"
    gender = models.CharField(
        max_length=1,
        choices=Gender.choices,
        verbose_name="Пол ученика",
    )

    def __str__(self) -> str:
        return (
            f"Ученик {self.full_name} ({self.birthday} г.р.), "
            f"{self.student_class}"
        )


class Standard(SoftDeleteModel):
    who_added = models.ForeignKey(
        "users.User",
        on_delete=models.PROTECT,
        verbose_name="Кто добавил норматив",
    )
    name = models.CharField(
        max_length=255,
        verbose_name="Название норматива",
    )
    has_numeric_value = models.BooleanField(
        verbose_name="Является ли это умением или нормативом",
        help_text="Если True, то это умение. Иначе - норматив",
    )

    def __str__(self) -> str:
        return self.name


class StandardValue(SoftDeleteModel):
    standard = models.ForeignKey(
        Standard,
        on_delete=models.CASCADE,
        verbose_name="Норматив",
    )
    student_class = models.ForeignKey(
        StudentClass,
        on_delete=models.CASCADE,
        verbose_name="Класс",
    )
    level = models.CharField(
        max_length=255,
        verbose_name="Уровень физподготовки",
    )
    value = models.FloatField(
        verbose_name="Значение",
    )

    class Gender(models.TextChoices):
        male = "m", "Мужской"
        female = "f", "Женский"
    gender = models.CharField(
        max_length=1,
        choices=Gender.choices,
        verbose_name="Пол ученика",
    )

    def __str__(self) -> str:
        return (
            f"Норматив: {self.standard}, "
            f"Класс: {self.student_class}, "
            f"Уровень ФП: {self.level}, "
            f"Значение: {self.value}"
        )


class StudentStandard(SoftDeleteModel):
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        verbose_name="Ученик",
    )
    standard = models.ForeignKey(
        Standard,
        on_delete=models.CASCADE,
        verbose_name="Норматив",
    )
    grade = models.CharField(
        max_length=255,
        verbose_name="Оценка",
    )
    value = models.FloatField(
        verbose_name="Значение",
    )

    def __str__(self) -> str:
        return (
            f"{self.student} - {self.standard} "
            f"({self.value}, Оценка: {self.grade})"
        )
