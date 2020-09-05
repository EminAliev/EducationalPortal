# Educational Portal

A platform for creating courses for online learning. As well as creating tests and testing them.

# Building

It is best to use the python virtualenv tool to build locally:

```python
$ virtualenv-2.7 venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ DEVELOPMENT=1 python manage.py runserver
```
Then visit http://localhost:8000 to view the app. 
