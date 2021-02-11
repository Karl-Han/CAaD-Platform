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

## clean
```
rm -rf media/
rm db.sqlite3
```

## DONE
- signup && login && naive profile
- create course && naive course page
- course list(index) && join course
- my courses in user profile (getUC)
- member list in course page (getCM)
- update password in a course
- delete user and change privilege in a course
- Homework models and create homework in a course
- get homework and auto update homework status (signals)
- commit homework for student and score homework for teacher
- File model and upload homeworkfile and get homeworkfile in homeworkPage
- create docker from dockerfile

## TODO
- See projects in github
- (more TODOs in code files)

## Optimization
- move self apis to utils (Done)
- get 10 elems in getUC/getCM(change to API) (TODO)
- hash filename

## Urls
(see urls.py)

## Addition
### signed up users (for testing)
- 123:123  admin
- 121:121  teacher
- 111:111  studert
- 222:222  visitor

