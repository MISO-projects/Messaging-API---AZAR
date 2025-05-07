FROM python:3.9-alpine

WORKDIR /app

COPY . /app/

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["flask", "--app","application", "run", "-h", "0.0.0.0", "-p", "8000"]