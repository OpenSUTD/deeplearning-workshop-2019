FROM python:3.6.8-slim-stretch
MAINTAINER Dude "dude@example.com"

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

RUN python -c "import nltk;nltk.download('vader_lexicon');nltk.download('stopwords')"

EXPOSE 5000

ENTRYPOINT [ "python" ]

CMD [ "app.py" ]