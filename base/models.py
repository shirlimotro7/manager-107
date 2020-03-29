from django.db import models

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, User



class MyAccountManager(BaseUserManager):
    def create_user(self, personal_num, username, password=None):
        if not personal_num:
            raise ValueError('Users must have an personal num')
        if not username:
            raise ValueError('Users must have a username')

        user = self.model(
            personal_num=personal_num,
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, personal_num, username, password):
        user = self.create_user(
            personal_num=personal_num,
            password=password,
            username=username,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

# Create your models here.
class Account(AbstractBaseUser):
    email 					= models.EmailField(verbose_name="email", max_length=60, unique=True)
    username 				= models.CharField(max_length=30, unique=True)
    date_joined				= models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login				= models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin				= models.BooleanField(default=False)
    is_active				= models.BooleanField(default=True)
    is_staff				= models.BooleanField(default=False)
    is_superuser			= models.BooleanField(default=False)
    last_name               = models.CharField(max_length=32)
    movil_CHOICES = (('yes', 'yes'), ('no', 'no'))
    movil = models.CharField(max_length=3, choices=movil_CHOICES)
    category_CHOICES = (('Pilot', 'Pilot'), ('Navigator', 'Navigator'))
    category = models.CharField(max_length=9, choices=category_CHOICES)
    personal_num            = models.CharField(max_length=20)
    first_name              = models.CharField(max_length=30)


    USERNAME_FIELD = 'personal_num'
    REQUIRED = ['username', 'personal_num']
    objects = MyAccountManager()


    def __str__(self):
        return self.first_name +' ' +  self.last_name

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    personal_num = models.CharField
    movil_CHOICES = (('yes', 'yes'), ('no', 'no'))
    movil = models.CharField(max_length=3, choices=movil_CHOICES)
    category_CHOICES = (('Pilot', 'Pilot'), ('Navigator', 'Navigator'))
    category = models.CharField(max_length=9, choices=category_CHOICES)

    def __str__(self):
        return self.user.username
