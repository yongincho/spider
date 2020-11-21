# Generated by Django 2.2.14 on 2020-11-17 10:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='spider_userinfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(max_length=255)),
                ('user_name', models.CharField(max_length=255)),
                ('user_pw', models.CharField(max_length=255)),
                ('user_email', models.CharField(max_length=255)),
                ('login_time', models.DateField(auto_now_add=True)),
                ('signup_time', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='spider_userface',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_face', models.CharField(max_length=255)),
                ('user_info', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='face.spider_userinfo')),
            ],
        ),
        migrations.CreateModel(
            name='spider_log',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('log_body', models.CharField(max_length=255)),
                ('log_type', models.IntegerField()),
                ('log_time', models.DateField(auto_now_add=True)),
                ('user_info', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='face.spider_userinfo')),
            ],
        ),
    ]