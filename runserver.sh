python manage.py collectstatic --no-input

python manage.py migrate

gunicron --worker-tmp-dir /dev/shm blogging.wsgi