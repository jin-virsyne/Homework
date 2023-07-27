FROM python:3.10-alpine

WORKDIR /app
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . /app/

CMD ["litestar", "run", "-H", "0.0.0.0"]