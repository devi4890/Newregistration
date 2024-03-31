
from django.urls import path
from .views import RegistrationAPIView,refresh_token_view, login_user,MyProtectedView,CourseDetailAPIView,CourseCreateAPIView,CourseListAPIView,get_course_details
from . import views 

urlpatterns = [
    path('register/', views.RegistrationAPIView.as_view(), name='register'),
    path('login/', login_user, name='login'),
    path('protected/', MyProtectedView.as_view(), name='protected-view'),
    path('courses/',CourseCreateAPIView.as_view(),name='validated-view'),
    path('courseslist/',CourseListAPIView.as_view(),name='validated-list'),
    path('courses/<slug:slug>/', CourseDetailAPIView.as_view(), name='course-detail'),
    path('quiz/<slug:slug>/', get_course_details, name='get_course_details'),
     path('refresh-token/', refresh_token_view, name='refresh_token'),
 
 
 ]