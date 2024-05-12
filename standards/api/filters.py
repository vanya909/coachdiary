from django_filters import rest_framework as filters
from django.db.models.functions import ExtractYear
from ..models import Student
from datetime import datetime
from django.core.validators import MinValueValidator, MaxValueValidator

class StudentFilter(filters.FilterSet):
    gender = filters.CharFilter(field_name="gender", lookup_expr="iexact")
    birthdate_lower = filters.NumberFilter(field_name="birthday", lookup_expr='gte', method='filter_by_year_gte')
    birthdate_upper = filters.NumberFilter(field_name="birthday", lookup_expr='lte', method='filter_by_year_lte')

    class Meta:
        model = Student
        fields = ['gender', 'student_class', 'birthdate_lower', 'birthdate_upper']

    def filter_by_year_gte(self, queryset, name, value):
        year_validator = [MinValueValidator(2000), MaxValueValidator(datetime.now().year)]
        for validator in year_validator:
            validator(value)
        return queryset.annotate(year=ExtractYear('birthday')).filter(year__gte=value)

    def filter_by_year_lte(self, queryset, name, value):
        return queryset.annotate(year=ExtractYear('birthday')).filter(year__lte=value)