FROM python:3-slim
WORKDIR /usr/src/app
COPY http.reqs.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt
COPY ./restaurant.py .
CMD [ "python", "./restaurant.py" ]