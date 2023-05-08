# Blogging APIs

A Blogging app where one can see all the Blogs, signup as a user and can create their own blog


## Context:
Building a blogging platform using Django, where users can register, create,
and manage their blog posts. You should create a backend API for the blog platform that can
handle requests from the frontend.



## Application Overview:
* Users will be able to register and login to the platform.
* Only authenticated users will be able to create, edit and delete their blog posts.
* Users should be able to create, read, update, and delete their blog posts
* Each blog post should have a title, body, and date of creation.

## Technologies/Framework/Libraries Used:

### Django
Django is a high-level Python web framework that enables rapid development of secure and maintainable websites. Built by experienced developers, Django takes care of much of the hassle of web development, so you can focus on writing your app without needing to reinvent the wheel. It is free and open source, has a thriving and active community, great documentation, and many options for free and paid-for support.

#### Why Django?
Django's comprehensive feature set, strong security, and established community make it a popular choice for building complex web applications. FastAPI and Flask, on the other hand, prioritize speed, flexibility, and simplicity. 

### PostgreSQL
PostgreSQL is a powerful, open source object-relational database system with over 35 years of active development that has earned it a strong reputation for reliability, feature robustness, and performance.
There is a wealth of information to be found describing how to install and use PostgreSQL through the official documentation. The open source community provides many helpful places to become familiar with PostgreSQL, discover how it works, and find career opportunities. Learn more on how to engage with the community.


#### Why PostgreSQL?
Firstly, it offers excellent scalability, which means that it can handle large datasets and complex queries with ease. It also supports a wide range of data types, making it a versatile choice for a variety of applications. 
Another key advantage of PostgreSQL is its robust security features. It offers multiple levels of authentication and encryption, as well as the ability to restrict access to specific tables or columns. This makes it a great choice for businesses that handle sensitive data.


### REST API
A REST API is a popular way for systems to expose useful functions and data. REST, which stands for representational state transfer, can be made up of one or more resources that can be accessed at a given URL and returned in various formats, like JSON, images, HTML, and more.

### Django REST Framework
Django REST framework (DRF) is a powerful and flexible toolkit for building Web APIs. Reasone for using:
* The Web browsable API is a huge usability win.
* Authentication policies including packages for OAuth1a and OAuth2.
* Serialization that supports both ORM and non-ORM data sources.
* Customizable all the way down - just use regular function-based views if you don't need the more powerful features.

### Knox
Knox provides easy to use authentication for Django REST Framework The aim is to allow for common patterns in applications that are REST based, with little extra effort; and to ensure that connections remain secure. 
Knox authentication is token based, similar to the "TokenAuthentication" built in to DRF.

#### Why Knox
* DRF tokens are limited to one per user. This does not facilitate securely signing in from multiple devices, as the token is shared. It also requires all devices to be logged out if a server-side logout is required (i.e. the token is deleted).

* DRF tokens are stored unencrypted in the database. This would allow an attacker unrestricted access to an account with a token if the database were compromised.

* DRF tokens track their creation time, but have no inbuilt mechanism for tokens expiring. Knox tokens can have an expiry configured in the app settings (default is 10 hours.)

### WhiteNoise

With a couple of lines of config WhiteNoise allows your web app to serve its own static files, making it a self-contained unit that can be deployed anywhere without relying on nginx, Amazon S3 or any other external service. (Especially useful on Heroku, OpenShift and other PaaS providers.)

### Validators
Python Data Validation for Humans™.
Python has all kinds of validation tools, but every one of them requires defining a schema. A simple validation library where validating a simple value does not require defining a form or a schema

## API Reference

#### Register

```
  POST /register
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `username`      | `string` | **Required**. Username for Register        |
| `password`      | `string` | **Required**. Password for Register        |
| `email`      | `string` | **Required**. Email for Register        |

#### Login

```
  POST /login
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `username`      | `string` | **Required**. Username for login        |
| `password`      | `string` | **Required**. Password for login        |

Output: TOKEN
####
Pass this token in Header of each API request as:
####
Authorization:  token {{TOKEN}}

####
At every login or register a new token is generated for the user


#### Logout

```
  POST /logout
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `Authorization`      | `string` | **Required**. The authentication token for the user making the request      |

#### Change Password

```
  PUT /change-password
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `old_password`      | `string` | **Required**. Old password of the user      |
| `new_password`      | `string` | **Required**. new password of the user      |
| `Authorization`      | `string` | **Required**. The authentication token for the user making the request      |

Change-Password, Token(Header) should be passed in "Body: form-data" type:JSON

#### List Blogs

```
  GET /api/posts/?page=1
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `Authorization`      | `string` | **Required**. The authentication token for the user making the request      |
| `page`      | `int` | The page no. as the list is Paginated by 10     |


#### List a Particular Blog

```
  GET /api/posts/<int:pk>
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `pk`      | `int` | **Required**. The ID of the blog to retrieve      |
| `Authorization`      | `string` | **Required**. The authentication token for the user making the request      |

Filter out Blog on the basis of its primary key

#### Create a Blog

```
  POST /api/create
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `title`      | `string` | **Required**. The title of the blog      |
| `content`      | `string` | **Required**. The content of the blog      |
| `image`      | `file` | An image file to use as the blog image  |
| `Authorization`      | `string` | **Required**. The authentication token for the user making the request      |


Lets you create a new blog, all fields except Token(Header) should be passed in "Body: form-data" type:JSON


#### Edit a Particular Blog

```
  PUT /api/posts/<int:pk>/edit
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `pk`      | `int` | **Required**. The ID of the blog to retrieve(Only which you have created)     |
| `title`      | `string` | **Required**. The title of the blog      |
| `content`      | `string` | **Required**. The content of the blog      |
| `image`      | `file` | An image file to use as the blog image  |
| `Authorization`      | `string` | **Required**. The authentication token for the user making the request      |



Lets you create a new blog, all fields except Token(Header) and pk should be passed in "Body: form-data" type:JSON


#### Delete a Particular Blog

```
  DELETE /api/<int:pk>/delete
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `pk`      | `int` | **Required**. The ID of the blog to retrieve(Only which you have created)     |
| `Authorization`      | `string` | **Required**. The authentication token for the user making the request      |


User can delete a blog and user can do so only once
######
pk= id which will filter out the blog and user will be fetched by Auth Token

## Run Locally

To downlaod this project

```bash
  git clone https://github.com/rishabhkesarwanii/Blogging_api.git
```

Create a Virtualenv
```bash
  Linux/MacOS: python3 -m venv env
  Windows: py -m venv env
```

Start Virtualenv
```bash
  Linux/macOS: source env/bin/activate
  Windows: .\env\Scripts\activate
```

Install all the dependencies 

```bash
  pip install -r requirements.txt
```


Configure the Environment Varaible

```bash
  Change name of ".env copy" to ".env"
```
```bash
  Configure all the Variable in .env as per your Database settings

  Note: Create a New PostgreSQL Database and Configure all variables in .env

```

Export READ_DOT_ENV_FILE to Terminal

```bash
  export READ_DOT_ENV_FILE=True

  #Read the .env file Locally
```

Make Migrations of the models

```python
  python manage.py makemigrations
```

Migrate Models to Database

```python
  python manage.py migrate
```

Runserver Locally

```python
  python manage.py runserver
```

#### Your server shoud be running Locally!!!

## Live

The api is already deployed on DigitalOcean, You can request the api from postman or any other service 
```
  https://plankton-app-ivsf4.ondigitalocean.app
```

## Postman Collection file

Postman Collections are a group of saved requests. Every request you send in Postman appears under the History tab of the sidebar. On a small scale, reusing requests through the history section is convenient.
```url
  https://github.com/rishabhkesarwanii/Blogging_api/blob/main/Blogging_api.postman_collection.json
```

Import postman collection file in postman from root folder of project or downlaod from above 
####
## Other(s)


Download python

```https
  https://www.python.org/downloads/
```

Install Virtualenv

```https
  https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/
```
Download PostgreSQL

```https
  https://www.postgresql.org/download/
```