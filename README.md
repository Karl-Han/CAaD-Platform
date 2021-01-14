# \_

## setup
```
# app:users
python manage.py startapp users
python manage.py makemigrations users
python manage.py migrate

# app:courses
python manage.py startapp courses
python manage.py makemigrations courses
python manage.py migrate

python manage.py runserver
#python manage.py shell

```

## Finished
- signup && login && naive profile
- create course && naive course page

## TODO
- CSS for app:users
- more details in profile
- tests
- limit string length in frontend form
- course list && join course
- (more TODOs in code files)

## Index
- /users/signup: signup page
- /users/login: login page
- /users/\<user nickname\>: user profile
- /courses/: courses index
- /courses/createCourse: create course
- /courses/\<course name\>: course page


## Addition
### signed up users (for testing)
- 123:123
- 121:121
