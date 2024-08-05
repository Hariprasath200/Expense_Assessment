from django.views.decorators.csrf import csrf_exempt
from rest_framework import permissions, status, viewsets, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from .models import CustomUser, Expense
from .serializers import ExpenseSerializer, UserSerializer
from django.contrib.auth.hashers import make_password
import logging

logger = logging.getLogger(__name__)

# Login View
class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    @csrf_exempt
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        role = request.data.get('role')

        logger.debug(f"Login attempt with email: {email}, role: {role}")

        try:
            user = CustomUser.objects.get(email=email)

            if user.check_password(password):
                if user.role == role:
                    token, created = Token.objects.get_or_create(user=user)
                    return Response({'token': token.key, 'role': user.role})
                else:
                    logger.debug("Role mismatch")
                    return Response({'error': 'Role mismatch'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                logger.debug("Invalid password")
                return Response({'error': 'Invalid password'}, status=status.HTTP_400_BAD_REQUEST)
        except CustomUser.DoesNotExist:
            logger.debug("User does not exist")
            return Response({'error': 'User does not exist'}, status=status.HTTP_400_BAD_REQUEST)

# Register View
class RegisterView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password1 = request.data.get('password1')
        password2 = request.data.get('password2')
        role = request.data.get('role')

        if password1 != password2:
            return Response({'error': 'Passwords do not match'}, status=status.HTTP_400_BAD_REQUEST)

        if CustomUser.objects.filter(email=email).exists():
            return Response({'error': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)

        user = CustomUser(
            email=email,
            role=role,
            password=make_password(password1)  # Hash the password
        )
        user.save()
        return Response({'email': user.email, 'role': user.role}, status=status.HTTP_201_CREATED)

# Expense ViewSet
class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

# Expense List and Create View
class ExpenseListView(generics.ListCreateAPIView):
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'Admin':
            return Expense.objects.all()
        return Expense.objects.filter(created_by=user)

# User Detail View
class UserDetailView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Expense
from .serializers import ExpenseSerializer

class ExpenseCreateView(generics.CreateAPIView):
    """
    API view to create a new expense entry.
    Only authenticated users can access this view.
    """
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """
        Save the expense entry with the user making the request as the creator.
        """
        serializer.save(created_by=self.request.user)
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import JsonResponse

@ensure_csrf_cookie
def my_view(request):
    return JsonResponse({'detail': 'CSRF cookie set'})
# views.py
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import JsonResponse

# views.py
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie

@ensure_csrf_cookie
def get_csrf_token(request):
    csrf_token = request.META.get('CSRF_COOKIE')
    print(f"CSRF Token: {csrf_token}")  # Log the CSRF token for debugging
    return JsonResponse({'csrfToken': csrf_token})
