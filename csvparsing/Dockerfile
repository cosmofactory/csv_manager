FROM python:3.10.6-slim
WORKDIR /app
COPY requirements.txt .
RUN pip3 install -r requirements.txt --no-cache-dir
COPY . .
RUN python manage.py collectstatic --no-input
RUN python manage.py migrate
CMD ["gunicorn", "csvparsing.wsgi:application", "--bind", "0:8000"]