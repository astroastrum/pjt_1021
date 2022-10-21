from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    def full_name(self):
        return f"{self.last_name}{self.first_name}"
