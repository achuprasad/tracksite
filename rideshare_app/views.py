from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Ride
from .permissions import IsDriver
from .serializers import UserRegistrationSerializer, UserLoginSerializer, RideSerializer
from rest_framework.permissions import IsAuthenticated


class UserRegistrationView(APIView):
    """
    API endpoint for user registration.
    """
    def post(self, request):
        """
        Handle user registration.
        Args:
            request (Request): The HTTP request object containing user registration data.
        Returns:
            Response: JSON response indicating the registration status.
        """
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        else:
            error_message = "Invalid registration data. Please check your input and try again."
            return Response({'message': error_message, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    """
    API endpoint for user login.
    """

    def post(self, request):
        """
        Args:
            request (Request): The HTTP request object containing user login data.
        Returns:
            Response: JSON response indicating the login status.
        """
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)
            if user:
                return Response({'message': 'User logged in successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RideCreateView(APIView):
    """
    API endpoint for creating a new ride.
    """
    permission_classes = [IsAuthenticated]
    def post(self, request):
        """
        Handle ride creation.
        Args:
            request (Request): The HTTP request object containing ride data.
        Returns:
            Response: JSON response indicating the ride creation status.
        """
        serializer = RideSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RideDetailView(APIView):
    """
    API endpoint for retrieving, updating, or deleting a specific ride.
    """
    permission_classes = [IsAuthenticated]

    def get_ride(self, pk):
        """
        Get the ride instance by its primary key.
        Args:
            pk (int): The primary key of the ride.
        Returns:
            Ride: The ride instance if found, else None.
        """
        try:
            return Ride.objects.get(pk=pk)
        except Ride.DoesNotExist:
            return None

    def get(self, request, pk):
        """
        Retrieve a specific ride.
        Args:
            request (Request): The HTTP request object.
            pk (int): The primary key of the ride.
        Returns:
            Response: JSON response containing the ride data or a message indicating the ride was not found.
        """
        ride = self.get_ride(pk)
        if ride:
            serializer = RideSerializer(ride)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'message': 'Ride not found'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        """
        Update a specific ride.
        Args:
            request (Request): The HTTP request object containing updated ride data.
            pk (int): The primary key of the ride.
        Returns:
            Response: JSON response indicating the update status or errors if the update fails.
        """
        ride = self.get_ride(pk)
        if ride:
            serializer = RideSerializer(ride, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'Ride not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        """
        Delete a specific ride.
        Args:
            request (Request): The HTTP request object.
            pk (int): The primary key of the ride.
        Returns:
            Response: JSON response indicating the deletion status or a message if the ride was not found.
        """
        ride = self.get_ride(pk)
        if ride:
            ride.delete()
            return Response({'message': 'Ride cancelled successfully'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'message': 'Ride not found'}, status=status.HTTP_404_NOT_FOUND)


class RideListView(APIView):
    """
    API endpoint for listing all rides.
    """
    def get(self, request):
        """
        Retrieve a list of all rides.
        Args:
            request (Request): The HTTP request object.
        Returns:
            Response: JSON response containing a list of rides.
        """
        rides = Ride.objects.all()
        serializer = RideSerializer(rides, many=True)
        return Response(serializer.data)


class RideAcceptView(APIView):
    """
    API endpoint for updating the status of a ride by a driver.
    """
    permission_classes = [IsAuthenticated, IsDriver]
    def post(self, request, pk):
        """
        Update the status of a ride.
        Args:
            request (Request): The HTTP request object containing the updated ride status.
            pk (int): The primary key of the ride.
        Returns:
            Response: JSON response indicating the status update status or errors if the update fails.
        """
        ride = self.get_ride(pk)
        if ride:
            new_status = request.data.get('status')
            if new_status in Ride.STATUS_CHOICES:
                ride.status = new_status
                ride.save()
                serializer = RideSerializer(ride)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({'message': 'Invalid status update'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'Ride not found'}, status=status.HTTP_404_NOT_FOUND)
