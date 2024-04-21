# пока никак не используемая хуета. пока не удаляй, может, еще настанет её час


from django_filters import rest_framework as filters
from ..models import Student

class StudentFilter(filters.FilterSet):
    # Define the fields and their filter types
    birth_year = filters.NumberFilter(field_name='birthday', lookup_expr='year')
    gender = filters.ChoiceFilter(choices=Student.Gender.choices)
    grade = filters.CharFilter(field_name='studentstandard__grade')
    
    class Meta:
        model = Student
        fields = ['birth_year', 'gender', 'grade']
