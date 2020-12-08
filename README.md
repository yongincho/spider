# Spider / Best Security Solution



Spider is an access control security solution aimed for various security usage.

  - Hardware and Software (Raspberry Pi 3 and Django Framework)
  - Face Recognition / Identification
  - User Statistics and Profiling

Specific Description:
> Spider is an access control security solution that allows face detection to login using both the hardware (Raspberry Pi) and the software (Django), which will work as an 'Access control service' for various usage. Spider allows users to 'sign up' by uploading their facial images, which will be stored in the AWS S3 Cloud Storage. When the user wants to log in to a platform, Spider will detect the user's face using the camera module of Raspberry Pi, and it will download the facial image (labeled to that user) from the cloud storage and will compare with the user's face who's trying to login. If the facial description matches (using OpenCV library), the user will be granted access. If not, they will be denied access. The focus of this security solution is the use of both the hardware and software components to create a safe and quick 'access control system.' The admin of Spider is provided with user statics and profiling through the dashboard frontend. 

### Tech

Below is the specification for technologies used in Spider:

* [ Infrastructure] - [AWS (Amazon Web Service)] - EC2, S3 (Cloud Storage)
* [ Database ] - [Postgresql]
* [ Language ] - Python 3.8 (BackEnd), Html, Javascript, CSS (FrontEnd)
* [ Framework ] - Django (BackEnd), [Bootstrap] (FrontEnd)
* [ Open-source Libraries ] - [OpenCV] (for face identification), Django ([rest_framework]) 
* [ Specific Points ] 
     *  [Raspberry Pi 3] Hardware based Face Recognition and Detection
     *  Using both hardware and software
     *  Seeking stable system development by separated analysis system (Raspberry Pi) from the user interface (API server)


### Installation

Install from git. Download zip file or git clone.

Install python dev and pip3:
```sh
$ apt-get install python3-dev
$ apt-get install python3-pip
```

For production environment:
```sh
$ pip3 install virtualenv
$ virtualenv envspider
```

Enter environment:
```sh
$ cd envspider/bin
$ source activate
```
If virtualenv is successfully activated, the command line should look like (envspider) ~~~

Spider requires a number of python libraries to run. Install requirements.txt:
```sh
$ pip3 install -r requirements.txt
```

Migrate Postgres DB:
```sh
$ python3 manage.py makemigrations
$ python3 manage.py migrate
```

Create superuser for Postgres DB:
```sh
$ python3 manage.py createsuperuser
```

Collect static and Run server (port: 8080):
```sh
$ python3 manage.py collectstatic
$ python3 manage.py runserver 0.0.0.0:8080
```


### User Manual
1. Login or Register for an admin account
        - This will redirect the admin to the dashboard.
2. Upload Facial Images through the Face Register tab on the Navbar
        - Those with Facial Images uploaded are granted access by face detection (using the camera module of the Raspberry Pi 3).
        - Admin can upload as many pictures of the users who will be granted access.
3. Dashboard tab shows the user statistics and profiling.
4. About tab shows the general information on Spider.
5. User Profile tab shows the user info who has been granted access by the admin.
6. The sidebar allows the admin to change background colors for the web.

### WireFrame
![alt text](https://github.com/yongincho/spider/blob/main/extra/Spider_webdesign.png)


### Screenshots of Spider
![alt text](https://github.com/yongincho/spider/blob/main/extra/Spider_screenshot1.png)
![alt text](https://github.com/yongincho/spider/blob/main/extra/Spider_screenshot2.png)
![alt text](https://github.com/yongincho/spider/blob/main/extra/Spider_screenshot3.png)
![alt text](https://github.com/yongincho/spider/blob/main/extra/Spider_screenshot4.png)
![alt text](https://github.com/yongincho/spider/blob/main/extra/Spider_screenshot5.png)
![alt text](https://github.com/yongincho/spider/blob/main/extra/Spider_screenshot6.png)

License
----

Spider Co. Ltd.


**Hope you make the most out of Spider!**

[//]: # (These are reference links)


   [AWS (Amazon Web Service)]: <https://aws.amazon.com/>
   [Postgresql]: <https://www.postgresql.org/>
   [Bootstrap]: <https://getbootstrap.com/docs/5.0/getting-started/introduction/>
   [OpenCV]: <https://opencv.org/>
   [rest_framework]: <https://www.django-rest-framework.org/>
   [Raspberry Pi 3]: <https://www.raspberrypi.org/products/raspberry-pi-3-model-b/?resellerType=home>
