import datetime
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError

from .base import BaseModel


class StudentClass(BaseModel):
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


class Student(BaseModel):
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


class Standard(BaseModel):
    name = models.CharField(
        max_length=255,
        unique=True,
        primary_key=True,
        verbose_name="Название норматива",
    )
    who_added = models.ForeignKey(
        "users.User",
        on_delete=models.PROTECT,
        verbose_name="Кто добавил норматив",
    )
    has_numeric_value = models.BooleanField(
        verbose_name="Является ли это умением или нормативом",
        help_text="Если True, то это умение. Иначе - норматив",
    )

    def __str__(self) -> str:
        return self.name


class StandardValue(BaseModel):
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

    def __str__(self) -> str:
        return (
            f"Норматив: {self.standard}, "
            f"Класс: {self.student_class}, "
        )


class Level(BaseModel):
    level_number = models.IntegerField(
        validators=(
            MinValueValidator(1),
        ),
        verbose_name="Номер уровня норматива",
    )
    low_level_value = models.FloatField(
        validators=(
            MinValueValidator(0),
        ),
        verbose_name="Минимальное значение для уровня",
    )
    middle_level_value = models.FloatField(
        validators=(
            MinValueValidator(0),
        ),
        verbose_name="Среднее значение для уровня",
    )
    high_level_value = models.FloatField(
        validators=(
            MinValueValidator(0),
        ),
        verbose_name="Лучшее значение для уровня",
    )
    standard = models.ForeignKey(
        StandardValue,
        on_delete=models.CASCADE,
        related_name="levels",
        verbose_name="Норматив, к которому относится данный уровень",
    )

    class Gender(models.TextChoices):
        male = "m", "Мужской"
        female = "f", "Женский"
    gender = models.CharField(
        max_length=1,
        choices=Gender.choices,
        verbose_name="Пол учеников, для которого рассчитан данный уровень",
    )


class StudentStandard(BaseModel):
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
