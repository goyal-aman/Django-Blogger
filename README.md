# Django-Blogger

Django-Blogger is a micro blogging site powered by Django framework with full-fledged support for user
authentication. Users can follow/unfollow multiple users on platform. 

## Getting Started

start playing around by getting your copy of source code by running this command in your terminal

```
git clone https://github.com/goyal-aman/Django-TodoApp.git
```

### Prerequisites

You will need various packages to work with this project. So start by creating a virtual envioronment. Run this command in terminal in same directory where you cloned repository
```
python -m venv myvenv
```

and then to activate the environment

If using  bash: ```. myvenv/scripts/activate```

If using windows cmd : ``` myvenv/scripts/activate.bat```

If using windows powershell : ```myvenv/scripts/activate.ps1```


### Installing

Now you need to install all the packages project needs, cd into the project directory containing ```manage.py``` file and run this command

```pip install -r requirments.txt```

this should install all the required packages.


## Running Django Server

To finally use this you need to makemigrations and migrate without which there will be various errors. Run these commands

```python manage.py makemigrations```

```python manage.py migrate```

and finally you are ready to run development server by using this  command

```python manage.py runserver```

but you still cannot login to admin page for which you need to create the admin user, use this command to create the admin user

````python manage.py createsuperuser````

and You are done. Enjoy

##Problems

If there is any problem with any steps above, or find a problem is the project create a issue
