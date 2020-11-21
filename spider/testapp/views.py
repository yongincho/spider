from django.shortcuts import render
from django.http import HttpResponse
from .models import *


def get_bank_info(request):

    if request.method == "POST":
        username = request.POST["UserName"]

        #info = client_info.objects.all()
        value = client_info.objects.filter(client_info_UserName=username).all() #client_info의 정보를 username에 따라 불러옴
       
        user_list = []
        for user in value:
            dictionary = {}
            dictionary["Name"]=user.client_info_Name #client_info에서 Name 가져옴
            dictionary["UserName"]=user.client_info_UserName #client_info에서 UserName 가져옴
            dictionary["Location"]=user.client_info_Location #client_info에서 Location 가져옴
            user_list.append(dictionary)
        
        #print(info)
        print(value)

    return HttpResponse(user_list) #가져온 정보 찍어주기


def update_bank_info(request):

    if request.method == "POST":
        bank_account = request.POST["Bank Account"]
        credit = request.POST["Credit"]
        debit = request.POST["Debit"]

        bank_info = bankaccount.objects.filter(bankaccount_number=bank_account).all() #bankaccount의 정보를 bankaccount_number에 따라 가져옴
        
        value, created = bankinfo.objects.update_or_create(
                id=None, defaults={"bankinfo_user": bank_info[0], "bankinfo_credit": int(credit), "bankinfo_debit": int(debit)}
        ) # 만약 id가 존재한다면 bankinfo를 defaults와 같이 업데이트 해줌. 만약 id가 위와같이 None이면 bankinfo를 defaults와 같이 생성해줌.
        
        bankaccount_info = bankaccount.objects.filter(bankaccount_user=bank_info[0].bankaccount_user).all() #bankaccount의 정보를 bankaccount_user에 따라 가져옴
        
        account, updated = bankaccount.objects.update_or_create(
                id=None, defaults={"bankaccount_user": bank_info[0].bankaccount_user, "bankaccount_number": bank_account, "bankaccount_totalvalue": bankaccount_info[0].bankaccount_totalvalue + int(credit) - int(debit), "bankaccount_loan": 0}   
        ) # 만약 id가 존재한다면 bankaccount를 defaults와 같이 업데이트 해줌. 만약 id가 위와같이 None이면 bankaccount를 defaults와 같이 생성해줌.
        
        #print(bank_info[0]) 
        #print(bank_info[0].bankaccount_user)
        #print(dir(bankaccount_info[0]))

    return HttpResponse("success")


# Create your views here.
