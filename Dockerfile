FROM python:3.8

WORKDIR /usr/src/app

RUN pip install Django==3.2.7 pip install  fpdf

COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]    