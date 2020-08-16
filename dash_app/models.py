from django.db import models
import datetime
import re


class UserManager(models.Manager):
    def validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email_address'] = "Invalid email address"
        if len(postData['fname']) < 2:
            errors['first_name'] = "Your first name must be more than 2 characters!!"
        if len(postData['lname']) < 2:
            errors['last_name'] = "Your last name must be more than 2 characters!!"
        if len(postData['password']) < 8:
            errors['password'] = "Password must be at least 8 characters!!"
        if postData['password'] != postData['confirm_password']:
            errors['confirm_password'] = "Password and confirm password do not match!!"
        return errors
    def edit_validator(self,postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email_address'] = "Email should be in this format: test@gmail.com!!"
        if len(postData['fname']) < 2:
            errors['first_name'] = "Your first name must be more than 2 characters!!"
        if len(postData['lname']) < 2:
            errors['last_name'] = "Your last name must be more than 2 characters!!"
        return errors

class QuoteManager(models.Manager):
    def validator(self, postData):
        errors = {}
        if len(postData['content']) < 10:
            errors['content'] = "Quote must be at least 10 characters!"
        if len(postData['author']) < 3:
            errors['author'] = "Author name must be at lease 3 characters!"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    
    def fullname(self):
        return (f'{self.first_name}  {self.last_name}')


class Quote(models.Model):
    author = models.CharField(max_length=100)
    content = models.TextField()
    poster = models.ForeignKey(User, related_name="posted_quotes", on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name="likes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = QuoteManager()



