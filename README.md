# CAaD Platform

CAaD is short for Cyber Attack and Defense.

## Setup
Install Python3 environment in advance.

```shell
# (Optional) If you want to use virtual environment and have installed virtualenv
# Create virtual environment for project
virtualenv venv
source venv/bin/activate

# Install necessary dependencies
pip install -r requirements.txt
# Need to install in order
pip install pycrypto
pip install pycryptodome

cd src
# Do preparation for Django
python manage.py makemigrations
python manage.py migrate

# Run CAaD platform on localhost:8000
python manage.py runserver
```