# flask-celery
A simple example to get started with Celery using Redis in Flask

### Installation
```
cd flask-celery
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
FLASK_APP=myflaskapp.py flask run
celery -A myflaskapp.celery worker -l info
celery -A myflaskapp.celery beat -l info
```