from django.contrib.auth.models import AbstractUser
from django.db import models
from autoslug import AutoSlugField

class CustomUser(AbstractUser):
    email = models.EmailField(max_length=250, unique=True)
    username = models.CharField(max_length=250, unique=True)
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return self.username
    

class Course(models.Model):
    course_id = models.IntegerField(primary_key=True, unique=True, editable=False)
    course_name = models.CharField(max_length=250, unique=True)
    slug = AutoSlugField(populate_from='course_name', unique=True, always_update=True, null=True)
    course_price = models.CharField(max_length=10, default=None ,null=True,blank=True)
    course_offer_price= models.CharField(max_length=10, default=None,null=True,blank=True)
    course_description = models.TextField()
    course_type = models.CharField(max_length=10, choices=[('paid', 'Paid'), ('free', 'Free')])  # True for Paid, False for Unpaid
    course_status = models.CharField(max_length=10, choices=[('active', 'Active'), ('inactive', 'Inactive')])
    slug = AutoSlugField(populate_from='course_name', unique=True, always_update=True, null=True)
    thumbnail = models.ImageField(
        upload_to='unique_course_name',
        blank=True,
        null=True, 
        default='course/default.png'
    )
    
    create_at = models.DateField(null=True, blank=True, auto_now=True)
    update_at = models.DateField(null=True, blank=True, auto_now=True)
    delete_at = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.course_name}"


class Quizzes(models.Model):
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    #course_name = models.ForeignKey(Course, on_delete=models.CASCADE)
    quiz_title = models.CharField(max_length=100)
    description = models.TextField()
    time_limit = models.IntegerField()
    randomize_questions = models.BooleanField()
    attempts_allowed = models.IntegerField()

    def __str__(self):
        return f"{self.quiz_title}"


class QuizQuestions(models.Model):
    quiz_id = models.ForeignKey(Quizzes, on_delete=models.CASCADE)
    question_text = models.TextField()
    question_type = models.CharField(max_length=50,choices=[('MCQ','Multiple Choice Question'),('TF','True/False Questions'),('Obj Typ','Objective Type Questions')])
    points = models.IntegerField()

    def __str__(self):
        return f"{self.question_text} "


class QuizChoices(models.Model):
    question_id = models.ForeignKey(QuizQuestions, on_delete=models.CASCADE)
    choice_text = models.TextField()
    is_correct = models.BooleanField()

    def __str__(self):
        return f"{self.choice_text}"


class QuizAttendance(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    quiz_id = models.ForeignKey(Quizzes, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    score = models.IntegerField()
    status = models.CharField(max_length=20,choices=[('in_progress','in_progress'),('completed','completed')])

    def __str__(self):
        #return f"{self.user.username}"
        return f"{self.status} - {self.user.username}'s - Quiz on {self.quiz_id.quiz_title}"
