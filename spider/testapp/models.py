from django.db import models

class client_info(models.Model):

    client_info_UserName = models.CharField(
            max_length=255,
            null=False
            )
    client_info_Password = models.CharField(
            max_length=255,
            null=False
            )
    client_info_Name = models.CharField(
            max_length=255,
            null=False
            )
    client_info_Location = models.CharField(
            max_length=255,
            null=False
            )

    def __str__(self):
        return "%s / %s" % (self.client_info_UserName, self.client_info_Location)

class bankaccount(models.Model):

    bankaccount_user = models.ForeignKey(client_info, on_delete=models.CASCADE)

    bankaccount_number = models.CharField(
            max_length=255,
            null=False
            )
    bankaccount_totalvalue = models.IntegerField(
            null=False
            )
    bankaccount_loan = models.IntegerField(
            null=False
            )

    def __str__(self):
        return "%s / %s" % (self.bankaccount_user, self.bankaccount_number)

class bankinfo(models.Model):    # models. = django에서 제공하는 database 관련 클레스

    bankinfo_user = models.ForeignKey(bankaccount, on_delete=models.CASCADE)

    bankinfo_credit = models.IntegerField(
            null=False
            )

    bankinfo_credit_date = models.DateField(
            auto_now_add=True,
            null=False
            )

    bankinfo_debit = models.IntegerField(
            null=False
            )

    bankinfo_debit_date = models.DateField(
            auto_now_add=True,
            null=False
            )

    def __str__(self):
        return "%s / %s / %s" % (self.bankinfo_user, self.bankinfo_credit_date, self.bankinfo_debit_date)




# Create your models here.
