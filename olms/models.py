import datetime
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.core.validators import FileExtensionValidator


class UserProfile(models.Model):
    user = models.OneToOneField(
        User, unique=True, related_name='profile', on_delete=models.CASCADE)
    uid = models.CharField(max_length=7, primary_key=True)
    usertypes = [('student', 'Student'), ('admin', 'Admin'),
                 ('security', 'Security')]
    usertype = models.CharField(
        max_length=8, choices=usertypes, default='student')
    branches = [('puc', 'PUC'), ('cse', 'CSE'), ('mech', 'MECH'),
                ('chem', 'CHEM'), ('ece', 'ECE'), ('mme', 'MME'), ('civil', 'CIVIL')]
    branch = models.CharField(max_length=5, choices=branches, default='puc')
    years = [('p1', 'P1'), ('p2', 'P2'), ('e1', 'E1'),
             ('e2', 'E2'), ('e3', 'E3'), ('e4', 'E4')]
    year = models.CharField(max_length=2, choices=years, default='p1')
    in_campus = models.BooleanField(default=True)


class LeaveCount(models.Model):
    count = models.IntegerField(default=0)
    user = models.OneToOneField(
        UserProfile, on_delete=models.SET_NULL, null=True)


class Leaves(models.Model):
    user = models.ForeignKey(
        UserProfile, on_delete=models.SET_NULL, related_name='leaveuser', blank=True, null=True)
    reason = models.CharField(max_length=50, default=None)
    description = models.CharField(max_length=999, default=None)
    proof = models.FileField(default=None, blank=True,
                             null=True, upload_to='proofs/', validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx', 'jpg', 'png', 'xlsx', 'xls'])])
    out_date = models.DateTimeField(default=None, blank=True, null=True)
    in_date = models.DateTimeField(default=None,  blank=True, null=True)
    actual_out_date = models.DateTimeField(default=None, blank=True, null=True)
    actual_in_date = models.DateTimeField(default=None, blank=True, null=True)
    statuses = [('pending', 'pending'), ('granted',
                                         'granted'), ('rejected', 'rejected'), ('on_leave', 'On Leave'), ('completed', 'Completed')]
    status = models.CharField(
        max_length=9, choices=statuses, default='pending')
    remark = models.CharField(max_length=100, default='No remark')


class Personal_info(models.Model):
    aadhar_no = models.IntegerField(primary_key=True)
    userprofile = models.OneToOneField(
        UserProfile, on_delete=models.CASCADE, related_name='personal_info')
    phone_no = models.IntegerField()
    Parent_name = models.CharField(max_length=50)
    Parent_phn_no = models.IntegerField()
    address = models.CharField(max_length=300)
    city = models.CharField(max_length=20)
    district = models.CharField(max_length=30)
