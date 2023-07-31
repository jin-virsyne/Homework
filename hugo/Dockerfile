FROM klakegg/hugo:latest

WORKDIR /app
COPY . /app/

RUN hugo --minify

CMD ["hugo", "server", "--bind=0.0.0.0", "--port=1313"]
