from django.db import models


class Level(models.Model):
    level = models.CharField(max_length=255)


class Gender(models.Model):
    gender = models.CharField(max_length=255)


class Classes(models.Model):
    number = models.IntegerField()


class Students(models.Model):
    classes = models.ForeignKey(Classes, on_delete=models.CASCADE)
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE)
    recruitment_year = models.DateField()
    class_name = models.CharField(max_length=255)
    birthday = models.DateField()


class Grades(models.Model):
    grade = models.CharField(max_length=255)


class Standards(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    has_numeric_value = models.BooleanField()


class StandardsValues(models.Model):
    standard = models.ForeignKey(Standards, on_delete=models.CASCADE)
    classes = models.ForeignKey(Classes, on_delete=models.CASCADE)
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    value = models.FloatField()


class StudentsStandards(models.Model):
    student = models.ForeignKey(Students, on_delete=models.CASCADE)
    standard = models.ForeignKey(Standards, on_delete=models.CASCADE)
    classes = models.ForeignKey(Classes, on_delete=models.CASCADE)
    grade = models.ForeignKey(Grades, on_delete=models.CASCADE)
    value = models.FloatField()
