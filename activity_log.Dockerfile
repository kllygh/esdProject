FROM python:3-slim
WORKDIR /usr/src/app
<<<<<<< HEAD
COPY amqp.reqs.txt ./
RUN python -m pip install --no-cache-dir -r amqp.reqs.txt
COPY ./activity_log.py ./amqp_setup.py ./
CMD [ "python", "./activity_log.py" ]
=======
COPY requirements.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt
COPY ./activity_log.py .
CMD [ "python", "./activity_log.py" ]
>>>>>>> c796eaf1976b442f37001b20113cb022bfa21729
