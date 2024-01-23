from django.db import models


class GameHistory(models.Model):
    user_id = models.IntegerField()
    opponent_id = models.IntegerField()
    discipline = models.CharField(max_length=255)
    result = models.CharField(max_length=255)
    has_ended = models.BooleanField()

    class Meta:
        db_table = 'game_history'


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