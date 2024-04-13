from django.contrib.auth import authenticate, login
from django.middleware.csrf import get_token
from rest_framework import response, status, views
from rest_framework.exceptions import ValidationError


class UserLoginView(views.APIView):

    def get(self, request):
        """Return CSRF token."""
        return response.Response({"csrf": get_token(request)})

    def post(self, request):
        """Login user."""
        email = request.data.get("email")
        password = request.data.get("password")

        self._validate_email_and_password(email, password)

        user = authenticate(request, email=email, password=password)
        if user is None or not user.is_authenticated:
            return response.Response(
                {
                    "status": "error",
                    "details": "Email or password is not correct.",
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )

        login(request, user)
        return response.Response(
            {
                "status": "ok",
                "details": "Logged In.",
            }
        )

    def _validate_email_and_password(self, email: str, password: str):
        """Check whether both fields are provided."""
        if not email and password:
            raise ValidationError("`email` field must be provided.")
        if email and not password:
            raise ValidationError("`password` field must be provided.")
        if not email and not password:
            raise ValidationError(
                "`email` and `password` fields must be provided.",
            )
