FROM python:3

WORKDIR /usr/src/app

COPY config/requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt
RUN pip3 install git+https://github.com/tweepy/tweepy
EXPOSE 5000/TCP

CMD [ "python", "./app.py" ]