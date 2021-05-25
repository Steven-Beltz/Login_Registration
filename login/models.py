from django.db import models
import re

class User_Manager(models.Manager):
    def user_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Email invalid, try again."
        email_check = self.filter(email=postData['email'])
        if email_check:
            errors['email'] = "Email already in use."
        if len(postData['first_name']) < 2 :
            errors['first_name'] = "First Name must be larger than 2 characters."
        if str.isalpha(postData['first_name']) != True :
            errors['first_name'] = "First Name can only contain alpabet characters"
        if len(postData['last_name']) < 2 :
            errors['last_name'] = "Last Name must be larger than 2 characters."
        if str.isalpha(postData['last_name']) != True :
            errors['lasst_name'] = "Last Name can only contain alpabet characters"
        if len(postData['password']) < 8 :
            errors['password'] = "Password must be at least 8 characters long."
        if postData['password'] != postData['password_confirm']:
            errors['password'] = "Passwords do not match."
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=75)
    passWord = models.CharField(max_length=50)
    objects = User_Manager()

