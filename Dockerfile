FROM python:3

WORKDIR startapp

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./manage.py" ]