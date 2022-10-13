# Student Unique Identification System
SIP Portal is a unique identification system for both Students and Institutions, which eases the work of both student and institution.

The method seeks to cut down on the amount of time and hassle it takes to verify a student's credentials and educational background for institutions, organisations, and students.

Our goal is to offer real-time verification of student information and give government agencies and other NGOs access to a set of data so they may assist students in need. Additionally, our system makes it simple to provide fellowships, grants, and scholarships.

Demo : https://link.ashwinr.dev/sihvideo

## Running on LocalHost
1. Donwload this Repository and Unzip it.
2. Install Python and Install the Requirements
``` 
pip install requirements
```
3. Install MySQL Server and create a database sipportal
```
create database sipportal;
```
4. Migrate the Models to MySQL
```
#Create Migrations
python manage.py makemigrations
#Make the migrations in mysql
python manage.py migrate
```
5. create a super user
```
python manage.py createsuperuser
```
6. Run the server
```
python manage.py runserver
```
## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
