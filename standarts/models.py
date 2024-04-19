from django.db import models
from django_softdelete.models import SoftDeleteModel
from auth.users.models import User


class Level(SoftDeleteModel):
    _soft_delete_cascade = True
    _restore_soft_deleted_related_objects = True
    level = models.CharField(max_length=255, verbose_name="Уровень физподготовки")


class Gender(SoftDeleteModel):
    _soft_delete_cascade = True
    _restore_soft_deleted_related_objects = True
    gender = models.CharField(max_length=255, verbose_name="Пол ученика")


class Classes(SoftDeleteModel):
    _soft_delete_cascade = True
    _restore_soft_deleted_related_objects = True
    number = models.IntegerField(verbose_name="Класс ученика (номер)")
    class_name = models.CharField(max_length=255, verbose_name="Класс ученика (буква)")
    class_owner = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="Куратор класса")


class Students(SoftDeleteModel):
    _soft_delete_cascade = True
    _restore_soft_deleted_related_objects = True
    classes = models.ForeignKey(Classes, on_delete=models.CASCADE, verbose_name="Класс ученика (номер)")
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE, verbose_name="Пол ученика")
    recruitment_year = models.DateField(verbose_name="Год набора")
    birthday = models.DateField(verbose_name="Дата рождения ученика")


class Grades(SoftDeleteModel):
    _soft_delete_cascade = True
    _restore_soft_deleted_related_objects = True
    grade = models.CharField(max_length=255, verbose_name="Оценка")


class Standards(SoftDeleteModel):
    _soft_delete_cascade = True
    _restore_soft_deleted_related_objects = True
    who_added = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="Кто добавил норматив")
    name = models.CharField(max_length=255, verbose_name="Название норматива")
    has_numeric_value = models.BooleanField(verbose_name="Если True, то это умение. Иначе - норматив")


class StandardsValues(SoftDeleteModel):
    standard = models.ForeignKey(Standards, on_delete=models.CASCADE, verbose_name="Норматив")
    classes = models.ForeignKey(Classes, on_delete=models.CASCADE, verbose_name="Класс")
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE, verbose_name="Пол ученика")
    level = models.ForeignKey(Level, on_delete=models.CASCADE, verbose_name="Уровень физподготовки")
    value = models.FloatField(verbose_name="Значение")


class StudentsStandards(SoftDeleteModel):
    student = models.ForeignKey(Students, on_delete=models.CASCADE, verbose_name="Ученик")
    standard = models.ForeignKey(Standards, on_delete=models.CASCADE, verbose_name="Норматив")
    classes = models.ForeignKey(Classes, on_delete=models.CASCADE, verbose_name="Класс")
    grade = models.ForeignKey(Grades, on_delete=models.CASCADE, verbose_name="Оценка")
    value = models.FloatField(verbose_name="Значение")
