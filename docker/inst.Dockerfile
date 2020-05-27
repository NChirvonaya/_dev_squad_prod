FROM python:3.7

COPY requirements.txt .

RUN pip install -r requirements.txt
RUN python -m nltk.downloader vader_lexicon

COPY . .

RUN mkdir -p db

ENV FLASK_APP=instagrammer
ENV FLASK_ENV=development
ENV FLASK_RUN_HOST=0.0.0.0
ENV DATABASE_URL=sqlite:///$PWD/app.db
ENV SECRET_KEY=verysecretkey

CMD bash docker/inst.entrypoint.sh
