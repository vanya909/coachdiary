from django.core.exceptions import ValidationError
from django.utils import timezone
from auth.users.models import User
from standards.models.standards import StudentClass, Student, Standard, StandardValue, Level, StudentStandard

def create_test_data():
    # Create a test user
    test_user = User.objects.create_user(email='testuser@example.com', password='password', name='Петр Петров Петрович')

    # Create test StudentClass instances
    student_classes = [
        StudentClass.objects.create(number=5, class_name='A', class_owner=test_user, recruitment_year=2020),
        StudentClass.objects.create(number=8, class_name='B', class_owner=test_user, recruitment_year=2019),
    ]

    # Create test Student instances
    students = [
        Student.objects.create(
            full_name='Ivan Ivanov', student_class=student_classes[0], birthday='2005-03-15', gender=Student.Gender.male
        ),
        Student.objects.create(
            full_name='Anna Petrovna', student_class=student_classes[1], birthday='2008-07-21', gender=Student.Gender.female
        ),
    ]

    # Create test Standard instances
    standards = [
        Standard.objects.create(name='100m Sprint', who_added=test_user, has_numeric_value=True),
        Standard.objects.create(name='English Grammar', who_added=test_user, has_numeric_value=False),
    ]

    # Create test StandardValue instances
    standard_values = [
        StandardValue.objects.create(standard=standards[0], student_class=student_classes[0]),
        StandardValue.objects.create(standard=standards[1], student_class=student_classes[1]),
    ]

    # Create test Level instances
    levels = [
        Level.objects.create(
            level_number=1,
            low_level_value=10.0,
            middle_level_value=9.5,
            high_level_value=9.0,
            standard=standard_values[0],
            gender=Level.Gender.male
        ),
        Level.objects.create(
            level_number=1,
            low_level_value=85.0,
            middle_level_value=90.0,
            high_level_value=95.0,
            standard=standard_values[1],
            gender=Level.Gender.female
        ),
    ]

    # Create test StudentStandard instances
    student_standards = [
        StudentStandard.objects.create(
            student=students[0],
            standard=standards[0],
            grade='B',
            value=11.2
        ),
        StudentStandard.objects.create(
            student=students[1],
            standard=standards[1],
            grade='A',
            value=93.5
        ),
    ]

    print("Test data created successfully")

# Run the function to create test data
create_test_data()