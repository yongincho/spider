# Spider / Design

Spider is a Django-based RESTful API that uses a face detection technique provided by the OpenCV library to implement an access control security solution. Bootstrap-based front-end is used with HTML, CSS, and JavaScript, and it is implemented with Django template-based front-end rendering and back-end linkage with Python 3.8. The server infrastructure has been built using Amazon Web Service (AWS) EC2 and S3 Cloud Storage. Database design and modeling have been implemented using PostgreSQL and Object-relational Mapping (ORM). Various hardwares/devices that have camera module such as PCs and Raspberry Pi can be used as hardware for Spider.

Below describes the design decisions made in Spider:
- Django
- Amazon Web Service - EC2 and S3
- Database - PostgreSQL and Object-relational Mapping
- OpenCV Library 
- RESTful API


### Django

Django is an open-source framework for back-end web applications based on Python. Spider uses the Django Framework because it is fast, simple, secure, well-established, and provides a wide range of features. Django uses the principle of rapid development and DRY philosophy to allow developers to do more than one iteration at a time and reuse existing codes, which allows developers to rapidly develop a project. It also has one of the best security systems and helps developers avoid common security issues, which is essential for security solutions like Spider. Django is also well-established with great documentation and resources, easy for developers to implement. Lastly, it provides various other features such as Magical ORM, HTTP libraries, etc., which are used in Spider.

[ References1 ]


### Amazon Web Service - EC2 and S3

Amazon Elastic Compute Cloud (Amazon EC2) is one of the most widely used web services that provides resizable compute capacity in the cloud. Spider uses AWS EC2 for its web server because it is very easy and quick to make and boot new server instances. It is also secure through Amazon VPC, reliable due to its proven network, comparably inexpensive, and is widely used by many developers. AWS EC2 also provides Amazon S3, which is a repository for internet data. S3 provides reliable and fast data storage infrastructure, which is used by Spider for facial image storage. It is easy to store and retrieve data from within Amazon EC2 or anywhere on the web, which is why it is utilized in Spider.

[ References2 ], [ References3 ]


### Database - PostgreSQL and Object-relational Mapping

ERD Cloud - DB Mapping
![alt text](https://github.com/yongincho/spider/blob/main/extra/Spider_erdcloud.png)

PostgreSQL is an enterprise-class open source database management system that supports both SQL for relational and JSON for non-relational queries. Spider uses PostgreSQL as it is a free and open-source software unlike Oracle or some features of MySQL. Spider also uses pgAdmin, a management tool for PostgreSQL. Object-relational mapping (ORM) is used in Spider to reduce the writing of SQL queries and procedures.

[ References4 ], [ References5 ]


### OpenCV Library

OpenCV is one of the largest open-source libraries for computer vision, machine learning, and image processing. As it is the most used image-related framework, it has a lot of related references and is reliable. OpenCV is used for face detection in Spider.

[ References6 ]


### RESTful API

RESTful API is one of the most popular types of API. REST (Representational State Transfer) can be used on nearly any protocol and takes advantage of HTTP when used for web APIs. It provides a lot of flexibility for diverse customers, and Spider uses RESTful API as it is one of the most common API and its flexibility allows various users to use Spider. 

[ References7 ]


[//]: # (These are reference links)


   [ References1 ]: <https://djangostars.com/blog/why-we-use-django-framework/>
   [ References2 ]: <https://www.amazonaws.cn/en/ec2/>
   [ References3 ]: <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/AmazonS3.html>
   [ References4 ]: <https://stackoverflow.com/questions/398134/what-are-the-advantages-of-using-an-orm#:~:text=At%20a%20very%20high%20level,lot%20of%20parsing%2Fserialization%20yourself.>
   [ References5 ]: <https://rajivrnair.dev/why-orm>
   [ References6 ]: <https://www.geeksforgeeks.org/opencv-overview/#:~:text=OpenCV%20is%20the%20huge%20open,even%20handwriting%20of%20a%20human.>
   [ References7 ]: <https://www.mulesoft.com/resources/api/restful-api#:~:text=One%20of%20the%20key%20advantages,the%20correct%20implementation%20of%20hypermedia.>

