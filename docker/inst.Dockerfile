FROM python:3.7

COPY test-reqs.txt .
RUN pip install -r test-reqs.txt

COPY requirements.txt .
RUN pip install -r requirements.txt
RUN python -m nltk.downloader vader_lexicon


RUN pip install git+https://git@github.com/ping/instagram_private_api.git --upgrade --force-reinstall

RUN mkdir -p /home/instagrammer
WORKDIR /home/instagrammer
COPY . .

RUN mkdir -p db

ENV FLASK_APP=instagrammer
ENV FLASK_ENV=development
ENV FLASK_RUN_HOST=0.0.0.0
ENV DATABASE_URL=sqlite:///$PWD/app.db
ENV SECRET_KEY=verysecretkey

CMD bash docker/inst.entrypoint.sh
