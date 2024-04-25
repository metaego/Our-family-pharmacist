# from django.db import models
# from django.contrib.auth.models import AbstractUser

# class User(AbstractUser):
#     user_id = models.PositiveIntegerField(primary_key=True)
#     user_email = models.CharField(unique=True, max_length=50)
#     user_password = models.CharField(max_length=50)
#     user_role = models.CharField(max_length=20)
#     user_status = models.CharField(max_length=10)
#     created_at = models.DateTimeField()
#     modified_at = models.DateTimeField(blank=True, null=True)
#     deleted_at = models.DateTimeField(blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'user'