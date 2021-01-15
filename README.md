To start the project on localhost, in an active virtual environment, enter the following commands:
pip install -r my_geekshop/requirements.txt
python my_geekshop/manage.py migrate
python my_geekshop/manage.py runserver

Superuser name "django". Type "python my_geekshop/manage.py changepassword django" if you want to use admin panel.
