# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

import bcrypt

# Create your models here.
class UserManager(models.Manager):
    def validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors['first_name_error'] = "Name field must be at least two characters."
        if len(postData['last_name']) < 2:
            errors['last_name_error'] = "Name field must be at least two characters."
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Must enter a valid email address."
        if len(postData['password']) < 8 or len(postData['confirm']) < 8:
            errors['password_length'] = "Password must be 8 or more characters."
        if postData['password'] != postData['confirm']:
            errors['password_match'] = "Passwords must match."
        return errors

    def login(self, postData):
        errors = {}
        user_check = User.objects.filter(email = postData['email'])
        if len(user_check) > 0:
            user_check = user_check[0]
            if bcrypt.checkpw(postData['password'].encode(), user_check.password.encode()):
                user = User.objects.filter()
            else:
                errors['error'] = "Email/password combination is invalid."
                return errors

class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()
