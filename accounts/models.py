
from django.contrib.auth.base_user import BaseUserManager
from django.db import models as models
from django.contrib.auth.models import AbstractBaseUser
from django.utils.translation import pgettext_lazy, pgettext


def user_dir(instance, filename):
    """define the place/directory where the users
    profile pictures will be kept"""
    return 'user_{0}/{1}'.format(instance.user.id, filename)


# Create your models here.
class MyUserManager(BaseUserManager):
    """This class will manage the MyUser model"""

    def create_user(self, username, password=None):
        """
        Creates and saves a User with the given username, email, date of
        birth, profile picture and password.

         email, date_of_birth, profile_pic,


         email=self.normalize_email(email),
                          date_of_birth=date_of_birth,
                          profile_pic=profile_pic
        """
        if not username:
            raise ValueError('Users must have a a username')
        user = self.model(username=username,

                          )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None):
      
        """
        Creates and saves a superuser with the given username, date of
        birth and password."""
        
        user = self.create_user(
            username,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    """model for each user on the site"""
    gender_type = models.TextChoices('gender_type', 'MALE FEMALE')
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(verbose_name='email address',
                              max_length=255)
    gender = models.CharField(blank=True, choices=gender_type.choices, max_length=6)
    date_of_birth = models.DateField(null=True, blank=True,
                                     verbose_name="Date of Birth yyyy-mm-dd")
    profile_pic = models.ImageField(verbose_name="Profile Picture",
                                    upload_to='user_profile',
                                    null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'username'

    """
    this is the user model made from
    a built in user model in django
    """
    def get_profile_pic(self):
        """

        :return: the url of a user profile picture
        """
        if str(self.gender).upper() == 'MALE':
            default_pic = '/media/profile/male_profile.png'
        elif str(self.gender).upper() == 'FEMALE':
            default_pic = '/media/profile/female_profile.png'
        else:
            return None
        if self.profile_pic:
            return self.profile_pic.url
        else:
            return default_pic

    def __str__(self):
        return "@{}".format(self.username)

    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        """Is the user a member of staff?"""
        # Simplest possible answer: All admins are staff
        return self.is_admin
