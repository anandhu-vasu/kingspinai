# Generated by Django 3.1.6 on 2021-03-02 20:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('username', models.CharField(max_length=60, verbose_name='user name')),
                ('email', models.EmailField(max_length=60, unique=True, verbose_name='email address')),
                ('company_name', models.CharField(max_length=200, verbose_name='company name')),
                ('phone', models.CharField(max_length=20, verbose_name='Mobile number')),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='date joined')),
                ('last_login', models.DateTimeField(auto_now=True, verbose_name='last login')),
                ('is_admin', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=True)),
                ('is_superuser', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
