from rest_framework import viewsets, permissions
from .models import Profile, User
from rest_framework.views import APIView
from .serializers import ProfileSerializer, UserSerializer
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from .utils import generate_jwt, get_user_id_from_request
from django.utils.crypto import get_random_string
from django.contrib.auth.hashers import make_password

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    
class LoginView(APIView):
    """
    API endpoint for user login.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        # Authenticate the user
        user = authenticate(request, email=username, password=password)
        if user is not None:
            # Generate JWT token
            payload = {
                "user_id": user.id,
                "username": user.email
            }
            token = generate_jwt(payload)
            return Response({"token": token}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        
        
class ResetPasswordView(APIView):
    """
    API endpoint for resetting a user's password.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        new_password = request.data.get("new_password")
        if not new_password:
            return Response({"error": "New password required"}, status=status.HTTP_400_BAD_REQUEST)

        user = request.user  # DRF Simple JWT sets request.user
        user.password = make_password(new_password)
        user.save()

        return Response({"message": "Password reset successfully."}, status=status.HTTP_200_OK)
    
    
class RegistrationView(APIView):
    """
    API endpoint for user registration.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        # Check if the email or username already exists
        # if User.objects.filter(username=username).exists():
            # return Response({"error": "Username already exists."}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(email=email).exists():
            return Response({"error": "Email already exists."}, status=status.HTTP_400_BAD_REQUEST)

        # Create a new user
        user = User.objects.create(
            email=email,
            password=make_password(password)  # Hash the password
        )
        user.save()

        return Response({"message": "User registered successfully."}, status=status.HTTP_201_CREATED)
    
    

class ProfileView(APIView):
    """
    Get, create, or update the profile of the logged-in user.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        profile, created = Profile.objects.get_or_create(user=request.user)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        profile, created = Profile.objects.get_or_create(user=request.user)
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)