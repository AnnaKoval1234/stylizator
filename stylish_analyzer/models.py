from django.db import models

class Lexem(models.Model):
    word = models.TextField(unique=True)
    style = models.TextField()
