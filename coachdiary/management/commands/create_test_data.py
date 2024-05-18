import datetime
import random
from django.core.management.base import BaseCommand
from django.utils import timezone
from standards.models import StudentClass, Student, Standard, StandardValue, Level, StudentStandard
from auth.users.models import User


class Command(BaseCommand):
    help = "Create test data for models"

    def handle(self, *args, **kwargs):
        # Clear existing data to avoid constraint issues
        StudentStandard.objects.all().delete()
        Level.objects.all().delete()
        StandardValue.objects.all().delete()
        Standard.objects.all().delete()
        Student.objects.all().delete()
        StudentClass.objects.all().delete()
        User.objects.all().delete()

        # Create users
        users = []
        for i in range(5):
            user = User.objects.create_user(
                name=f'user{i}',
                email=f'user{i}@example.com',
                password='password',
            )
            users.append(user)

        # Create student classes
        student_classes = []
        for number in range(1, 12):
            for class_name in ['А', 'Б', 'В']:
                student_class = StudentClass.objects.create(
                    number=number,
                    class_name=class_name,
                    class_owner=random.choice(users),
                )
                student_classes.append(student_class)

        # Create students
        students = []
        for i in range(100):
            student = Student.objects.create(
                full_name=f'Student {i}',
                student_class=random.choice(student_classes),
                birthday=datetime.date(
                    random.randint(2000, 2015),
                    random.randint(1, 12),
                    random.randint(1, 28)
                ),
                gender=random.choice([Student.Gender.male, Student.Gender.female]),
            )
            students.append(student)

        # Create standards
        standards = []
        for i in range(10):
            standard = Standard.objects.create(
                name=f'Standard {i}',
                who_added=random.choice(users),
                has_numeric_value=random.choice([True, False]),
            )
            standards.append(standard)

        # Create standard values
        standard_values = []
        for standard in standards:
            for student_class in student_classes:
                standard_value = StandardValue.objects.create(
                    standard=standard,
                    student_class=student_class,
                )
                standard_values.append(standard_value)

        # Create levels
        for standard_value in standard_values:
            for i in range(1, 6):
                Level.objects.create(
                    level_number=i,
                    low_level_value=random.uniform(0, 10),
                    middle_level_value=random.uniform(10, 20),
                    high_level_value=random.uniform(20, 30),
                    standard=standard_value,
                    gender=random.choice([Level.Gender.male, Level.Gender.female]),
                )

        # Create student standards
        for student in students:
            for standard in standards:
                StudentStandard.objects.create(
                    student=student,
                    standard=standard,
                    grade=random.choice(['A', 'B', 'C', 'D', 'E']),
                    value=random.uniform(0, 100),
                )

        self.stdout.write(self.style.SUCCESS('Test data created successfully.'))

# To run this script, save it as a management command in your Django app (e.g., `your_app/management/commands/create_test_data.py`),
# and then run it with the command: `python manage.py create_test_data`.
