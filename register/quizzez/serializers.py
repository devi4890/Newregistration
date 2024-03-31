from django.forms import ValidationError
from rest_framework import serializers
from .models import CustomUser
from django.core.mail import send_mail
from django.conf import settings
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .models import Course,Quizzes, QuizQuestions, QuizChoices,QuizAttendance
from rest_framework_simplejwt.tokens import RefreshToken,AccessToken
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email','password', 'first_name', 'last_name', 'phone_number']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    def validate_email(self, value):
        try:
            validate_email(value)
        except ValidationError as e:
            raise serializers.ValidationError(str(e))
        return value
    

    def create(self, validated_data):
        
        
        user = CustomUser.objects.create_user(**validated_data)
        
        
        send_welcome_email(user.email)
        return user
        
         
    

def send_welcome_email(email):
    subject = 'Welcome to our platform'
    message = 'Thank you for registering/login to our platform.'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)
class LoginSerializer(serializers.Serializer):
    email= serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=128, write_only=True)

    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)

        if email is None or password is None:
            raise serializers.ValidationError(
                'Both email and password are required to log in.'
            )

        user = CustomUser.objects.filter(email=email).first()

        if user is None:
            raise serializers.ValidationError(
                'No user found with given email.'
            )

        if not user.check_password(password):
            raise serializers.ValidationError(
                'Incorrect password.'
            )

        refresh = RefreshToken.for_user(user)
        
        return {
            'email': user.email,
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh)
        }

class QuizAttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizAttendance
        fields = ('id', 'start_time', 'end_time','score','status')


class QuizChoicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizChoices
        fields = ( 'choice_text', 'is_correct')

class QuizQuestionsSerializer(serializers.ModelSerializer):
    #choices = QuizChoicesSerializer(many=True, read_only=True)
    choices=serializers.SerializerMethodField()             
    class Meta:
        model = QuizQuestions
        fields = ('question_text', 'choices')
    def get_choices(self, obj):
        choices = QuizChoices.objects.filter(question_id=obj)
        serialized_choices = QuizChoicesSerializer(choices, many=True).data
        return serialized_choices


class QuizzesSerializer(serializers.ModelSerializer):
    #quizQuestion = QuizQuestionsSerializer(many=True, read_only=True)
    quizQuestion =serializers.SerializerMethodField()
    class Meta:
        model = Quizzes
        fields = ('id', 'quiz_title', 'quizQuestion')

    def get_quizQuestion(self, obj):
        questions = QuizQuestions.objects.filter(quiz_id=obj)
        serialized_questions = QuizQuestionsSerializer(questions, many=True).data
        return serialized_questions


class CourseSerializer(serializers.ModelSerializer):
    #quiz = QuizzesSerializer(many=True, read_only=True)
    quizzes = serializers.SerializerMethodField()
    
    
    class Meta:
        model = Course
        #fields = ['course_id', 'course_name', 'slug', 'course_price', 'course_offer_price', 'course_description', 'course_status', 'course_type', 'thumbnail','quiz']
        fields = ['course_id','course_name', 'course_price','course_offer_price','course_type','course_status', 'course_description','slug','quizzes']

    def get_quizzes(self, obj):
        quizzes = Quizzes.objects.filter(course_id=obj.course_id)
        serialized_quizzes = QuizzesSerializer(quizzes, many=True).data
        return serialized_quizzes














