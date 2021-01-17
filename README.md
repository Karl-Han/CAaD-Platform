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
- course list(index) && join course
- my courses in user profile (API: getUC)

## TODO
- CSS for app:users
- more details in profile
- tests
- limit string length in frontend form
- member list in course page (API: getCM)
- (more TODOs in code files)

## Optimization
- moved self apis to utils

## Index
- /users/signup: signup page
- /users/login: login page
- /users/\<user nickname\>: user profile
- /courses/: courses index
- /courses/createCourse: create course
- /courses/\<course name\>: course page
- /courses/\<course name\>/join: join course api(for visitor)

## Addition
### signed up users (for testing)
- 123:123
- 121:121
- 111:111

