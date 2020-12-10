from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin
from django.utils import timezone

class UserManager(BaseUserManager):

    use_in_migrations = True

    def create_user(self, email, nickname, place="", password=None):
        if not email:
            raise ValueError('require email form')
        user = self.model(
                email = self.normalize_email(email),
                nickname = nickname,
                place = ""
                )
        print (dir(user))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nickname, place="", password=None):
        if not email:
            raise ValueError('require email or place')
        user = self.create_user(
            email = self.normalize_email(email),
            nickname = nickname,
            place = place,
            password=password
        )
        print (dir(user))
        #user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class SpiderUser(AbstractBaseUser, PermissionsMixin):  # Create SpiderUser table

    objects = UserManager()

    email = models.EmailField(
            max_length=255,
            unique=True,
            )  # Create email column
    nickname = models.CharField(
            max_length=20,
            null=False,
            unique=True
            )  # Create nickname column
    place = models.CharField(
            max_length=40,
            null=True
            )  # Create place column

    is_active = models.BooleanField(default=True)  # Create is_active column
    #is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)  # Create is_superuser column
    is_staff = models.BooleanField(default=False)  # Create is_staff column
    date_joined = models.DateTimeField(auto_now_add=True)  # Create date_joined column
    USERNAME_FIELD = 'nickname'
    REQUIRED_FIELDS = ['email']

class SpiderIdentifyRequest(models.Model):  # Create SpiderIdentifyRequest table

    user_info = models.ForeignKey(SpiderUser, on_delete=models.CASCADE)
    
    identify_username = models.CharField(
            max_length=255,
            null=False
            )  # Create identify_username column

    s3_path = models.CharField(
            max_length=255,
            null=False
            )  # Create s3_path column

    status = models.IntegerField(
            null=False,
            default=0 
            )  # Create status column
    
    ticket = models.CharField(
            max_length=300,
            null=False
            )  # Create ticket column

    request_time = models.DateField(
            auto_now_add=True,
            null=False
            )  # Create request_time column

class SpiderUserLog(models.Model):  # Create SpiderUserLog table

    user_info = models.ForeignKey(SpiderUser, on_delete=models.CASCADE)  # Add foreign key to SpiderUser table

    log_body = models.CharField(
            max_length=255,
            null=False
            # Specify User Log info
            )  # Create log_body column

    log_type = models.IntegerField(
            null=False
            # 1 = user_login, 2 = admin_login, 3 = admin_register, 4 = face_register
            )  # Create log_type column

    log_success = models.IntegerField(
            null=False
            # 1 = success, 2 = fail
            )  # Create log_success column

    log_ticket = models.CharField(
            max_length=300,
            null=True
            )

    log_time = models.DateField( 
            auto_now_add=True,
            null=False
            )  # Create log_time column

    def __str__(self):
        return "%s / %d / %s" % (self.log_body, self.log_type, self.log_time)  # Output log_body, log_type, and log_time as the name of the data on the DB


class SpiderUserFace(models.Model):  # Create SpiderUserFace table

    user_info = models.ForeignKey(SpiderUser, on_delete=models.CASCADE)  # Add foreign key to SpiderUser table

    user_face = models.CharField(
            max_length=255,
            null=False
            )  # Create user_face column

    def __str__(self):
        return "%s" % (self.user_info)  # Output user_info as the name of the data on the DB

