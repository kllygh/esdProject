FROM python:3.9
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt
COPY ./payment.py .
CMD [ "python", "./refund.py" ]