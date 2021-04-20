# CAaD Platform

CAaD is short for Cyber Attack and Defense.

## Setup
Install Python3 environment in advance.

```shell
# Create virtual environment for project
virtualenv venv
source venv/bin/activate

# Install necessary dependencies
pip install -r requirements.txt

cd src
# Do preparation for Django
python manage.py makemigrations
python manage.py migrate

# Run CAaD platform
python manage.py runserver
```