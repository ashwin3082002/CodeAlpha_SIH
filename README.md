# Student Unique Identification System (SIP) Portal

- [Introduction](#introduction)
- [Features](#features)
- [Demo](#demo)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Contributing](#contributing)
- [License](#license)

## Introduction

The Student Unique Identification System (SIP) Portal is a comprehensive solution that simplifies student identification and data management for institutions and organizations. It offers real-time verification of student information, streamlines the disbursement of scholarships and grants, and provides valuable insights through dynamic reports.

## Features

- Real-time verification of student credentials and educational background
- Centralized repository for student details accessible via APIs and a GUI interface
- Direct disbursement of scholarships, grants, and fellowships to student bank accounts
- Generation of dynamic reports for specific regions or time periods
- Digital signature-enabled academic history download for students
- Predictive analytics using machine learning models for growth trends analysis

## Demo

A demonstration of the SIP Portal can be accessed at [Demo Link](https://link.ashwinr.dev/sihvideo).

## Tech Stack

The SIP Portal is built using the following technologies:

- Django: A powerful web framework for building scalable and secure applications
- Python: The programming language used for implementing the backend logic
- MySQL: A robust and reliable relational database management system for storing and retrieving data
- Django Rest Framework: A toolkit for building RESTful APIs in Django
- HTML: The markup language used for structuring the webpages
- CSS: The styling language used for designing the user interface
- JavaScript: A programming language used for implementing interactive features on the frontend

## Installation

To run the SIP Portal locally, follow these steps:

1. Clone the repository to your local machine.
2. Install Python and the required dependencies by running `pip install -r requirements.txt`.
3. Install MySQL Server and create a database named `sipportal`.
4. Migrate the models to MySQL by running the following commands:
```
python manage.py makemigrations
python manage.py migrate
```
5. Create a superuser account by running `python manage.py createsuperuser`.
6. Run the server using `python manage.py runserver`.
7. Access the SIP Portal in your web browser at `http://localhost:8000`.

## Contributing

Contributions to the SIP Portal are welcome. If you encounter any issues or have suggestions for improvements, please open an issue on the GitHub repository.

## License

The SIP Portal is open-source software licensed under the [MIT License](LICENSE).
