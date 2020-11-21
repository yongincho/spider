from django.db import models

class spider_userinfo(models.Model):

    user_id = models.CharField(
            max_length=255,
            null=False
            )
    user_name = models.CharField(
            max_length=255,
            null=False 
            )
    user_pw = models.CharField(
            max_length=255,
            null=False
            )
    user_email = models.CharField(
            max_length=255,
            null=False
            )
    login_time = models.DateField(
            auto_now_add=True, # auto_now_add - when doing any select, insert, update, delete, etc, update time
            null=False
            )
    signup_time = models.DateField(
            auto_now=True, # auto_add - when adding new column, update time
            null=False
            )

    def __str__(self):
        return "%s / %s" % (self.user_name, self.login_time)

class spider_userface(models.Model):

    user_info = models.ForeignKey(spider_userinfo, on_delete=models.CASCADE)

    user_face = models.CharField(
            max_length=255,
            null=False
            )

    def __str__(self):
        return "%s" % (self.user_info)

class spider_log(models.Model):

    user_info = models.ForeignKey(spider_userinfo, on_delete=models.CASCADE)

    log_body = models.CharField(
            max_length=255,
            null=False
            )

    log_type = models.IntegerField(
            null=False
            )

    log_time = models.DateField(
            auto_now_add=True,
            null=False
            )

    def __str__(self):
        return "%s / %d / %s" % (self.log_body, self.log_type, self.log_time)



# Create your models here.
