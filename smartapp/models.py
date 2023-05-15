from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver

# User Profile picture path
def user_directory_path(instance, filename):
    return 'UserProfiles/user_{0}/{1}'.format(instance.user.username, filename)

# Doctor Profile picture path
def doc_directory_path(instance, filename):
    return 'DoctorProfiles/user_{0}/{1}'.format(instance.user.username, filename)

# Consultation Images Path
def additional_directory_path(instance, filename):
    return 'consult/images/user_{0}/{1}'.format(instance.user.username, filename)

# Models
class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    contact = models.CharField(max_length=100, null=True)
    nic = models.CharField(max_length=14, null=True)
    address = models.CharField(max_length=100, null=True)
    dob = models.DateField(null=True)
    image = models.FileField(upload_to=user_directory_path, null=True)
    prime_subscription = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.user.first_name
@receiver(pre_delete, sender=UserProfile)
def mymodel_delete(sender, instance, **kwargs):
    instance.image.delete(False)


class Doctor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    contact = models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=100, null=True)
    category = models.CharField(max_length=100, null=True)
    image = models.FileField(upload_to=doc_directory_path, null=True)
    slmc = models.IntegerField(null=True)

    def __str__(self):
        return self.user.first_name

@receiver(pre_delete, sender=Doctor)
def mymodel_delete(sender, instance, **kwargs):
    instance.image.delete(False)

class Type(models.Model):
    name = models.CharField(max_length=100, null=True)


    def __str__(self):
        return self.name

class ArticleCategory(models.Model):
    name = models.CharField(max_length=100, null=True)
    def __str__(self):
        return self.name


class News_Article(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=300, null=True)
    content = models.TextField(null=True)
    date = models.DateField(null=True)
    category = models.CharField(max_length=100, null=True)
    image = models.FileField(upload_to='newsImages/%y%m%d/', null=True)

    def __str__(self):
        return '{} - {}'.format(self.date, self.title)
@receiver(pre_delete, sender=News_Article)
def mymodel_delete(sender, instance, **kwargs):
    instance.image.delete(False)

class Feedback(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True)
    messages = models.TextField(null=True)
    date = models.DateField(null=True)

    def __str__(self):
        return '{} - {}'.format(self.user.user.username, self.date)

class Consult(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    fname = models.CharField(max_length=300, null=True)
    age = models.IntegerField(null=True)
    weight = models.CharField(max_length=300, null=True)
    height = models.CharField(max_length=300, null=True)
    bmi = models.CharField(max_length=300, null=True)
    symptoms = models.TextField(null=True)
    allergiesEms = models.TextField(null=True, blank=True)
    date = models.DateField(null=True)
    advice = models.TextField(null=True)
    doc = models.CharField(max_length=300, null=True)
    prescribe_img = models.ImageField(upload_to=additional_directory_path, null=True, blank=True)
    img1 = models.ImageField(upload_to=additional_directory_path, null=True, blank=True)
    img2 = models.ImageField(upload_to=additional_directory_path, null=True, blank=True)
    img3 = models.ImageField(upload_to=additional_directory_path, null=True, blank=True)

    def __str__(self):
        return '{} - {}'.format(self.fname, self.date)

@receiver(pre_delete, sender=Consult)
def mymodel_delete(sender, instance, **kwargs):
    instance.img1.delete(False)
    instance.img2.delete(False)
    instance.img3.delete(False)
    instance.prescribe_img.delete(False)

class Payment(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True)
    payment_date = models.DateField(null=True)
    email = models.CharField(max_length=300, null=True)
    amount = models.FloatField(max_length=5, null=True)
    tr_id = models.CharField(max_length=20, null=True)

    def __str__(self):
        return '{} - {}'.format(self.user.user.username, self.payment_date)