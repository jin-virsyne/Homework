FROM klakegg/hugo:latest

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . /app/

RUN python manage.py makemigrations --merge
RUN python manage.py migrate --noinput

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
