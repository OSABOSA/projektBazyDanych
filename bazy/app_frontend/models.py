from django.db import models

# Create your models here.


def create_dynamic_model(table_name):
    class DynamicModel(models.Model):
        name = models.CharField(max_length=255)

        class Meta:
            db_table = table_name

    return DynamicModel


class User(models.Model):
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=100)

    class Meta:
        db_table = 'users'


class Activity(models.Model):
    user_id = models.IntegerField()
    discipline_id = models.CharField(max_length=100)
    elo = models.IntegerField()

    class Meta:
        db_table = 'activities'


class Discipline(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'disciplines'