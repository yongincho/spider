# Spider / Best Security Solution



Spider is an access control security solution aimed for various security usage.

  - Software (Django Framework) with any other device with camera module
  - Face Recognition / Identification
  - User Statistics and Profiling

Specific Description:
> Spider is an access control security solution that allows face detection to login through the software (Django) API along with other hardwares with camera module, which will work as an 'Access control service' for various usage. Spider allows the admin to sign up users by uploading their facial images, which will be stored in the AWS S3 Cloud Storage. When the user wants to log in to a platform, Spider will detect the user's face using the camera module of a hardware device, and it will download the facial image (labeled to that user) from the cloud storage and will compare with the user's face who is trying to login. If the facial description matches (using OpenCV library), the user will be granted access. If not, they will be denied access. The focus of this security solution is to create a safe and quick 'access control system' by providing friendly admin interface and user API. The admin of Spider is provided with user statics and profiling through the dashboard interface. However, some part of the admin interface has yet to be implemented, and the API has been tested through Postman, an API development tool.

### Tech

Below is the specification for technologies used in Spider:

* [ Infrastructure] - [AWS (Amazon Web Service)] - EC2, S3 (Cloud Storage)
* [ Database ] - [Postgresql]
* [ Language ] - Python 3.8 (BackEnd), Html, Javascript, CSS (FrontEnd)
* [ Framework ] - Django (BackEnd), [Bootstrap] (FrontEnd)
* [ Open-source Libraries ] - [OpenCV] (for face identification), Django ([rest_framework]) 


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

Install OpenCV Library:
```sh
$ brew install ninja pkg-config
$ wget http://dlib.net/files/dlib-19.2.tar.bz2 -O /tmp/dlib-19.2.tar.bz2
$ tar xvjf /tmp/dlib-19.2.tar.bz2 -C ./
$ cd dlib-19.2
$ mkdir build && cd build
$ cmake -G Ninja ..
$ cmake --build . --config Release
$ cd ../
$ sudo python setup.py install
```
If installing setup.py does not work:
```sh
$ brew cask install xquartz
$ brew install gtk+3 boost
$ brew install boost-python3
$ pip3 install face_recognition
$ pip3 install opencv-python
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


### Admin Manual
1. Login or Register for an admin account
        - This will redirect the admin to the dashboard.
2. Upload User's Facial Images through the Face Register tab on the Navbar
        - Those with Facial Images uploaded are granted access by face detection.
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


### Into Video Link
- https://youtu.be/3Ngv1-RI9tw


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
