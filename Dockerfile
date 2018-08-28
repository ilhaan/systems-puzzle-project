FROM python:3

ENV PYTHONUNBUFFERED 1
RUN mkdir -p /opt/services/flaskapp/src
COPY requirements_app.txt /opt/services/flaskapp/src/
WORKDIR /opt/services/flaskapp/src
RUN pip install -r requirements_app.txt
COPY . /opt/services/flaskapp/src
EXPOSE 5000

CMD ["python", "app.py"]
