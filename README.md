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

## DONE
- signup && login && naive profile
- create course && naive course page
- course list(index) && join course
- my courses in user profile (getUC)
- member list in course page (getCM)
- update password in a course
- delete user in a course

## TODO
- See projects in github
- (more TODOs in code files)

## Optimization
- move self apis to utils (Done)
- get 10 elems in getUC/getCM(change to API) (TODO)

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

