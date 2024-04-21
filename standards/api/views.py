from rest_framework import mixins, viewsets, permissions, generics, views, status
from rest_framework.response import Response
from .serializers import StandardValueSerializer, StudentSerializer, StudentClassSerializer
from ..models import StandardValue, Student, StudentClass
from .filters import StudentFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import PermissionDenied


class StudentsByClassView(generics.ListAPIView):
    serializer_class = StudentSerializer
    permission_classes = [permissions.IsAuthenticated]  # Require authentication

    def get_queryset(self):
        # Start with all students
        queryset = Student.objects.all()

        # Filter students by the classes owned by the current user
        queryset = queryset.filter(student_class__class_owner=self.request.user)

        # Get query parameters for filtering
        birth_year = self.request.query_params.get('birth_year')
        gender = self.request.query_params.get('gender')
        class_number = self.request.query_params.get('class_number')
        class_name = self.request.query_params.get('class_name')
        standard_id = self.request.query_params.get('standard_id')

        # Apply filters
        if birth_year:
            queryset = queryset.filter(birthday__year=birth_year)

        if gender:
            queryset = queryset.filter(gender=gender)

        if class_number and class_name:
            queryset = queryset.filter(student_class__number=class_number, student_class__class_name=class_name)
        elif class_number:
            queryset = queryset.filter(student_class__number=class_number)

        if standard_id:
            # Filter students who have records in StudentStandard for the specified standard_id
            queryset = queryset.filter(studentstandard__standard_id=standard_id)

        return queryset
        

class StandardsByClassView(generics.ListAPIView):
    serializer_class = StandardValueSerializer
    permission_classes = [permissions.IsAuthenticated]  # Require authentication

    def get_queryset(self):
        # Get the query parameters for class_number and class_name
        class_number = self.request.query_params.get('class_number')
        class_name = self.request.query_params.get('class_name')

        if class_number and class_name:
            # Try to find the class based on class_number and class_name
            try:
                student_class = StudentClass.objects.get(number=class_number, class_name=class_name)
            except StudentClass.DoesNotExist:
                # If the class does not exist, raise PermissionDenied (403 Forbidden)
                raise PermissionDenied(f"Class {class_number}{class_name} does not exist.")
            
            # Filter the standards for the specified class
            queryset = StandardValue.objects.filter(student_class=student_class)
            
            # Check if the current user owns the specified class
            if student_class.class_owner != self.request.user:
                raise PermissionDenied("You do not have permission to access the standards for this class.")

            return queryset

        # If no class_number or class_name is provided, return an empty queryset or handle differently based on your requirements
        return StandardValue.objects.none()

class ClassesByOwnerView(generics.ListAPIView):
    serializer_class = StudentClassSerializer
    permission_classes = [permissions.IsAuthenticated]  # Require authentication

    def get_queryset(self):
        # Filter classes by the current logged-in user
        return StudentClass.objects.filter(class_owner=self.request.user)
    

class FilterOptionsView(views.APIView):
    # Require that the user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # Get the query parameters for class number and class name
        class_number = request.query_params.get('class_number')
        class_name = request.query_params.get('class_name')

        # Check ownership of the class or parallel
        # Filter classes that the user owns
        user = request.user
        
        if class_number and class_name:
            # Check if the user owns the specific class
            user_classes = Student.objects.filter(student_class__class_owner=user,
                                                   student_class__number=class_number,
                                                   student_class__class_name=class_name)
            if not user_classes.exists():
                # Raise a permission error if the user does not own the class
                raise PermissionDenied("You do not own this class.")
        elif class_number:
            # Check if the user owns the classes in the specified parallel
            user_classes = Student.objects.filter(student_class__class_owner=user,
                                                   student_class__number=class_number)
            if not user_classes.exists():
                # Raise a permission error if the user does not own any classes in the parallel
                raise PermissionDenied("You do not own any classes in this parallel.")

        # Filter students based on the ownership of the class or parallel
        queryset = user_classes
        
        # Calculate distinct filter options from the filtered queryset
        birth_years = queryset.dates('birthday', 'year').distinct()
        grades = queryset.values_list('studentstandard__grade', flat=True).distinct()
        genders = queryset.values_list('gender', flat=True).distinct()

        # Create a response dictionary
        options = {
            'birth_years': [year.year for year in birth_years],
            'grades': list(grades),
            'genders': list(genders)
        }

        # Return the filter options as a JSON response
        return Response(options, status=status.HTTP_200_OK)

#--------------------CRUDS--------------------------
class StandardValueViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = StandardValueSerializer
    queryset = StandardValue.objects.all()
    permission_classes = (
        permissions.IsAuthenticated,
    )


