FROM python:3.10-alpine
WORKDIR /usr/src/app
EXPOSE 8443
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python3", "app.py"]