from django.db import models


class History(models.Model):
    history_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    opponent_id = models.IntegerField()
    discipline = models.ForeignKey('Discipline', on_delete=models.PROTECT)
    result = models.IntegerField()

    class Meta:
        db_table = 'history'


class Ongoing(models.Model):
    ongoing_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    opponent_id = models.IntegerField()
    discipline = models.ForeignKey('Discipline', on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'ongoing'


class Requested(models.Model):
    requested_id = models.AutoField(primary_key=True)
    activity = models.ForeignKey('Activity', on_delete=models.CASCADE)
    receiver_id = models.IntegerField()

    class Meta:
        db_table = 'requested'


class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    phone = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = 'users'


class Discipline(models.Model):
    discipline_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = 'disciplines'


class Activity(models.Model):
    activity_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    discipline_id = models.IntegerField()
    elo = models.IntegerField()

    class Meta:
        db_table = 'activities'
