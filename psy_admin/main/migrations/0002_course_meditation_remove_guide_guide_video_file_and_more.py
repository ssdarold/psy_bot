# Generated by Django 4.2.11 on 2024-03-12 13:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_video_name', models.CharField(max_length=255, verbose_name='Название видеофайла')),
                ('course_video_description', models.TextField(null=True, verbose_name='Описние видеофайла')),
                ('course_video_file', models.FileField(blank=True, upload_to='static/data/videos/courses', verbose_name='Видео курса')),
            ],
            options={
                'verbose_name': 'Видео курс',
                'verbose_name_plural': 'Видео курсы',
            },
        ),
        migrations.CreateModel(
            name='Meditation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meditation_name', models.CharField(max_length=255, verbose_name='Название медитации')),
                ('meditation_description', models.TextField(null=True, verbose_name='Описние медитации')),
                ('meditation_file', models.FileField(blank=True, upload_to='static/data/audios/meditations', verbose_name='Аудио медитации')),
            ],
            options={
                'verbose_name': 'Медитация',
                'verbose_name_plural': 'Медитации',
            },
        ),
        migrations.RemoveField(
            model_name='guide',
            name='guide_video_file',
        ),
        migrations.RemoveField(
            model_name='guide',
            name='guide_video_name',
        ),
        migrations.AddField(
            model_name='guide',
            name='guide_file',
            field=models.FileField(blank=True, null=True, upload_to='static/data/videos/guide', verbose_name='Файл гайда'),
        ),
        migrations.AddField(
            model_name='guide',
            name='guide_name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Название гайда'),
        ),
        migrations.AddField(
            model_name='order',
            name='item',
            field=models.CharField(choices=[('course', 'Курс по самооценке'), ('guide', 'Видео гайд')], max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='settings',
            name='start_audio_file',
            field=models.FileField(blank=True, upload_to='static/data/audios', verbose_name='Приветственное аудио'),
        ),
        migrations.AddField(
            model_name='user',
            name='funnel_step',
            field=models.IntegerField(null=True, verbose_name='Текущий этап в воронке'),
        ),
        migrations.AlterField(
            model_name='guide',
            name='relation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='settings_relation', to='main.settings'),
        ),
    ]
