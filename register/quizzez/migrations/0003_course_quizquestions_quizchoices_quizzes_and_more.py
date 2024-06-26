# Generated by Django 5.0.3 on 2024-03-10 15:33

import autoslug.fields
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizzez', '0002_alter_customuser_phone_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('course_id', models.IntegerField(editable=False, primary_key=True, serialize=False, unique=True)),
                ('course_name', models.CharField(max_length=250, unique=True)),
                ('course_price', models.CharField(default=None, max_length=10)),
                ('course_offer_price', models.CharField(default=None, max_length=10)),
                ('course_description', models.TextField()),
                ('course_type', models.CharField(choices=[('paid', 'Paid'), ('free', 'Free')], max_length=10)),
                ('course_status', models.CharField(choices=[('active', 'Active'), ('inactive', 'Inactive')], max_length=10)),
                ('slug', autoslug.fields.AutoSlugField(always_update=True, editable=False, null=True, populate_from='course_name', unique=True)),
                ('thumbnail', models.ImageField(blank=True, default='course/default.png', null=True, upload_to='unique_course_name')),
                ('create_at', models.DateField(auto_now=True, null=True)),
                ('update_at', models.DateField(auto_now=True, null=True)),
                ('delete_at', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='QuizQuestions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.TextField()),
                ('question_type', models.CharField(choices=[('MCQ', 'Multiple Choice Question'), ('TF', 'True/False Questions'), ('Obj Typ', 'Objective Type Questions')], max_length=50)),
                ('points', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='QuizChoices',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice_text', models.TextField()),
                ('is_correct', models.BooleanField()),
                ('question_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quizzez.quizquestions')),
            ],
        ),
        migrations.CreateModel(
            name='Quizzes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quiz_title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('time_limit', models.IntegerField()),
                ('randomize_questions', models.BooleanField()),
                ('attempts_allowed', models.IntegerField()),
                ('course_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quizzez.course')),
            ],
        ),
        migrations.AddField(
            model_name='quizquestions',
            name='quiz_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quizzez.quizzes'),
        ),
        migrations.CreateModel(
            name='QuizAttendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('score', models.IntegerField()),
                ('status', models.CharField(choices=[('in_progress', 'in_progress'), ('completed', 'completed')], max_length=20)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('quiz_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quizzez.quizzes')),
            ],
        ),
    ]
