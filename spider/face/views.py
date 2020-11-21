from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
import hashlib
import pymysql
from lib.s3wrapper import S3Wrapper
import os
from wrapper.redis_wrapper import RedisWrapper
from django.conf import settings

def register(request):

    if request.method == "POST":

        name = request.POST["name"]
        email = request.POST["email"]
        id = request.POST["id"]
        pw = request.POST["pw"]

        project_spider = pymysql.connect(
            user = settings.RDB_USER,
            passwd = settings.RDB_PW,
            host = settings.RDB_HOST,
            db = settings.RDB_DB,
            charset = settings.RDB_CHARSET
        )

        cursor = project_spider.cursor()

        cursor.execute("CALL spider_register('"+name+"','"+email+"','"+id+"','"+pw+"');")

        answer = cursor.fetchone()

        project_spider.close()

        if answer[0] == "fail":
            print("Existing ID")
            return HttpResponse("Fail")

        else:
            print("Successfully registered")
            return HttpResponse("Success")

    else:
        print("Method incorrect")


def faceregister(request):

    if request.method == "POST":

        id = request.POST["id"]
        upload_file = request.FILES["file"]
        
        project_spider = pymysql.connect(
            user = settings.RDB_USER,
            passwd = settings.RDB_PW,
            host = settings.RDB_HOST,
            db = settings.RDB_DB,
            charset = settings.RDB_CHARSET
        )
        
        #print(dir(upload_file))
        #print(type(upload_file))

        cursor = project_spider.cursor()

        cursor.execute("CALL spider_bringdata_by_id('"+id+"');")

        answer = cursor.fetchall()

        #print(answer)

        m = hashlib.md5()
        m.update(upload_file.read())
        hash_filename = m.hexdigest()

        converted_filename = hash_filename+"_"+answer[0][2] 
        
        #print(converted_file)
        
        fs = FileSystemStorage(
            location = settings.STORAGE_DIRECTORY
        )
        filename = fs.save(converted_filename, upload_file)

        s3 = S3Wrapper(settings.S3_ACCESS_KEY, settings.S3_SECRET_KEY)
        s3.upload("spider-face-bucket", settings.STORAGE_DIRECTORY+converted_filename, converted_filename)

        os.remove(settings.STORAGE_DIRECTORY+converted_filename)

        if answer[0][0] == None:
            print("No Existing ID")
            project_spider.close()
            return HttpResponse("Fail")

        else:
            print("Successfully face-registered")
            cursor.execute("CALL spider_faceregister('"+str(answer[0][0])+"','"+converted_filename+"');")
            project_spider.close()
            return HttpResponse("Success")
        
    else:
        print("Method incorrect")

        

def identify(request):
    
    if request.method == "POST":

        id = request.POST["id"]
        #upload_file = request.FILES["file"]

        project_spider = pymysql.connect(
            user = settings.RDB_USER,
            passwd = settings.RDB_PW,
            host = settings.RDB_HOST,
            db = settings.RDB_DB,
            charset = settings.RDB_CHARSET
        )
        '''
        fs = FileSystemStorage(
            location = "/opt/projects/spider/storage"
        )
        filename = fs.save(upload_file.name(), upload_file)
        '''
        cursor = project_spider.cursor()

        cursor.execute("CALL spider_bringfacedata_by_id('"+id+"');")

        answer = cursor.fetchall()

        s3 = S3Wrapper(settings.S3_ACCESS_KEY, settings.S3_SECRET_KEY)

        for i in answer:
            #print(i)
            s3.download("spider-face-bucket", i[0], STORAGE_DIRECTORY+i[0])
            # if (Compare filename with the downloaded image) is true:
            #     print("Qualified")
            #     break

        r = RedisWrapper('localhost', '6379', settings.WRAPPER_PW)
        r.setvalue('spider_request_queue','{"user_id":"%s"}'%(id))
        print("set value")

        return HttpResponse("Success")
    
    else:
        print("Method Incorrect")


# Create your views here.
