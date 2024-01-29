from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.db import models


# class UserManager(BaseUserManager):
#     def create_user(self, username, email, password=None, first_name=None, last_name=None):
#         if not email:
#             raise ValueError('User must have an email address!')
#
#         if not email:
#             raise ValueError('User must have a username!')
#
#         user = self.model(email=self.normalize_email(email))
#
#         user.set_password(password)
#         user.set_first_name(first_name)
#         user.set_last_name(last_name)
#
#         user.is_active = True
#
#         user.save(using=self._db)
#
#         return user
#
#
# class User(AbstractBaseUser):
#     username = models.CharField(
#         verbose_name='username',
#         max_length=255,
#         unique=True,
#     )
#
#     email = models.EmailField(
#         verbose_name='email',
#         max_length=255,
#         unique=True,
#     )
#
#     first_name = models.CharField(
#         verbose_name='first name',
#         max_length=255,
#         null=True
#     )
#
#     last_name = models.CharField(
#         verbose_name='last name',
#         max_length=255,
#         null=True
#     )
#
#     is_active = models.BooleanField(default=True)
#     admin = models.BooleanField(default=False)
#     staff = models.BooleanField(default=False)
#     _is_teacher = models.BooleanField(default=False)
#     _is_student = models.BooleanField(default=False)
#
#     USERNAME_FIELD = 'username'
#     REQUIRED_FIELDS = ['first_name', 'last_name']
#
#     def get_full_name(self):
#         return f'{self.first_name} {self.last_name}'
#
#     def get_email(self):
#         return self.email
#
#     def get_username(self):
#         return self.username
#
#     def has_perm(self, perm, obj=None):
#         return True
#
#     def has_module_perms(self, app_label):
#         return True
#
#     def get_first_name(self):
#         return self.first_name
#
#     def get_last_name(self):
#         return self.last_name
#
#     def set_first_name(self, first_name):
#         self.first_name = first_name
#
#     def set_last_name(self, last_name):
#         self.last_name = last_name
#
#     @property
#     def is_staff(self):
#         return self.staff
#
#     @property
#     def is_admin(self):
#         return self.admin
#
#     @property
#     def is_teacher(self):
#         return self._is_teacher
#
#     @property
#     def is_student(self):
#         return self._is_student
#
#     objects = UserManager()
#
#
# class Teacher(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     user._teacher = True
#
#     class Meta:
#         ordering = ['user__last_name', 'user__first_name']
#
#     def __str__(self):
#         return self.user.get_full_name()
#
#
# class Student(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     user._student = True
#     # group = models.ForeignKey(Group, on_delete=models.CASCADE)
#
#     class Meta:
#         ordering = ['user__last_name', 'user__first_name']
#
#     def __str__(self):
#         return self.user.get_full_name()
#
#     # def get_group(self):
#     #     return self.group
#     #
#     # def get_group_name(self):
#     #     return self.group.group_name

