import datetime
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class UserProfile(models.Model):
    user = models.OneToOneField(
        User, unique=True, related_name='profile', on_delete=models.CASCADE)
    id = models.CharField(max_length=7, primary_key=True)
    is_admin = models.BooleanField(default=True)
    branches = [('puc', 'PUC'), ('cse', 'CSE'), ('mech', 'MECH'),
                ('chem', 'CHEM'), ('ece', 'ECE'), ('mme', 'MME'), ('civil', 'CIVIL')]
    branch = models.CharField(max_length=5, choices=branches, default='cse')
    years = [('p1', 'P1'), ('p2', 'P2'), ('e1', 'E1'),
             ('e2', 'E2'), ('e3', 'E3'), ('e4', 'E4')]
    year = models.CharField(max_length=2, choices=years, default='e1')


class LeaveCount(models.Model):
    count = models.IntegerField(default=0)
    user = models.OneToOneField(
        UserProfile, on_delete=models.SET_NULL, null=True)


class Leaves(models.Model):
    user = models.ForeignKey(
        UserProfile, on_delete=models.SET_NULL, related_name='leaveuser', blank=True, null=True)
    reason = models.CharField(max_length=50, default=None)
    description = models.CharField(max_length=999, default=None)
    proof = models.FileField(default=None, blank=True, null=True)
    out_date = models.DateTimeField(default=None, blank=True, null=True)
    in_date = models.DateTimeField(default=None,  blank=True, null=True)
    statuses = [('submitted', 'submitted'), ('granted',
                                             'granted'), ('rejected', 'rejected')]
    status = models.CharField(
        max_length=9, choices=statuses, default='submitted')
