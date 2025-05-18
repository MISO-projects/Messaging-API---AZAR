FROM python:3.9-alpine

WORKDIR /app

COPY . /app/

RUN pip install -r requirements.txt

RUN pip install --no-cache-dir newrelic

EXPOSE 8000

CMD ["newrelic-admin", "run-program", "flask", "--app", "application", "run", "-h", "0.0.0.0", "-p", "8000"]