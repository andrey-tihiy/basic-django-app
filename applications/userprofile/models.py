from django.contrib.auth.models import User
from django.db import models
from applications.utils.models import UUIDModel


class UserProfile(UUIDModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_date = models.DateField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.user.username
