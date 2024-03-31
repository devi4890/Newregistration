from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication,permissions,generics
from rest_framework import status
from .serializers import UserSerializer,LoginSerializer
from .models import CustomUser
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer,LoginSerializer,CourseSerializer,QuizzesSerializer,QuizQuestionsSerializer,QuizChoicesSerializer
from .models import Course, QuizAttendance, QuizChoices, QuizQuestions, Quizzes
from django.utils import timezone
from datetime import timedelta
from rest_framework_simplejwt.views import TokenRefreshView
from django.http import HttpRequest

class RegistrationAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login_user(request):
    if request.method == 'POST':
      serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
         return Response(serializer.validated_data, status=status.HTTP_200_OK)
    else:
         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class MyProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user  # This will give you the logged-in user
        content = {'message': f'Welcome, {user.username}! '}
        return Response(content)
    
class CourseCreateAPIView(APIView):
    

    def post(self, request, format=None):
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CourseListAPIView(generics.ListAPIView):

    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class CourseDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    lookup_field='slug'


    def put(self, request, *args, **kwargs):
        partial=kwargs.pop('partial',False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        #serializer.save()
        self.perform_update(serializer)
        return Response(serializer.data)
        
    def perform_update(self, serializer):
        serializer.save()
 

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response("Course deleted",status=204)

@api_view(['GET'])
def course_quiz_data(request, course_id):
    try:
        course = Course.objects.get(course_id=course_id)
    except Course.DoesNotExist:
        return Response({"message": "Course not found"}, status=404)
    
    # Serialize course data including associated quizzes and questions
    serializer = CourseSerializer(course)

    # Customize the response format
@api_view(['GET'])
def course_quiz_data(request):
    courses = Course.objects.all()
    data = []

    for course in courses:
        course_data = {
            "Course": course.course_name,
            "quiz": []
        }

        quizzes = Quizzes.objects.all()

        for quiz in quizzes:
            quiz_data = {
                "quizQuestion": Quizzes.quiz_title,
                "choices": []
            }

            questions = QuizQuestions.objects.all()

            for question in questions:
                choices = QuizChoices.objects.all().values_list('choice_text', flat=True)
                quiz_data["choices"].append(choices)

            course_data["quiz"].append(quiz_data)

        data.append(course_data)
        

    return Response(data)

@api_view(['GET'])
def get_course_details(request, slug):
    try:
        course = Course.objects.get(slug=slug)
    except Course.DoesNotExist:
        return Response({"message": "Course not found"}, status=404)

    serializer = CourseSerializer(course)
    return Response(serializer.data)

@api_view(['POST'])
def refresh_token_view(request):
    refresh_token = request.data.get('refresh_token')

    if refresh_token:
        try:
            # Create a new request object with the refresh token
            new_request = HttpRequest()
            new_request.method = 'POST'
            new_request.data = {'refresh_token': refresh_token}  # Set the data with refresh token

            # Use TokenRefreshView provided by simplejwt to refresh the token
            response = TokenRefreshView.as_view()(new_request)
            return Response({
                'access_token': response.data['access'],
                'expires_at': response.data['exp'],
            }, status=response.status_code)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'detail': 'Refresh token not provided'}, status=status.HTTP_400_BAD_REQUEST)