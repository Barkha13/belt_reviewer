from __future__ import unicode_literals
import bcrypt
from django.db import models
# from datetime import datetime
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z]')

# Create your models here.
class UserManager(models.Manager):
    def reg_validator(self, postData):
        errors = {}
        if (len(postData['name']) or len(postData['alias']) or len(postData['email']) or len(postData['pass']) or len(postData['conf_pass'])) < 1:
            errors['field_empty'] = "Fields can not be empty!"   
    
        if (len(postData['name']) or len(postData['alias'])) < 2:
            errors['name_length'] = "At least needs 2 characters for Name/Alias!!"
        
        if (not NAME_REGEX.match(postData['name'])) or (not NAME_REGEX.match(postData['alias'])):
            errors['name_type'] = "Name/Alias only contains letters!!"
        
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid Email Address!"
        
        if len(postData['pass']) < 8:
            errors['pass'] = "Password should be at least 8 characters long!"
        
        if postData['conf_pass'] != postData['pass']:
            errors['pass2'] = "Passwords didn't match!"
        return errors;

    def login_validator(self,postData):
        errors1 = {}
        if (len(postData['login_email']) or len(postData['login_pass'])) < 1:
            errors1['field_empty'] = "Fields can not be empty!"
        user_list = []
        user_list = User.objects.filter(email = postData['login_email'])
        if (user_list):
            login_pass = postData['login_pass']
            check = bcrypt.checkpw(login_pass.encode(),user_list[0].password.encode())
            if(check is False):
                errors1['wrong'] = "Wrong Username or Password!"
        else:
            errors1['wrong'] = "Wrong Username or Password!"
        return errors1;


class User(models.Model):
    name = models.CharField(max_length = 255)
    alias = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    
    objects = UserManager()

# class Author(models.Model):
#     author_name = models.CharField(max_length = 255)
#     created_at = models.DateTimeField(auto_now = True)
#     updated_at = models.DateTimeField(auto_now_add = True)

class Book(models.Model):
    title = models.CharField(max_length = 255)
    users = models.ForeignKey(User,related_name = "books")
    author = models.CharField(max_length = 255)
    # authors = models.ForeignKey(Author,related_name = "authors_books")
    # created_at = models.DateTimeField(auto_now = True)
    # updated_at = models.DateTimeField(auto_now_add = True)

class Review(models.Model):
    review = models.TextField()
    rating = models.IntegerField()
    reviewer = models.ForeignKey(User, related_name = "reviews")
    book_reviews = models.ForeignKey(Book,related_name="books_reviews")
    # created_at = models.DateTimeField(auto_now = True)
    # updated_at = models.DateTimeField(auto_now_add = True)




