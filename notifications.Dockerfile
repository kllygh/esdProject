FROM python:3.9
WORKDIR /usr/src/app
COPY twilio.reqs.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt
COPY ./notification.py .
CMD [ "python", "./notification.py" ]