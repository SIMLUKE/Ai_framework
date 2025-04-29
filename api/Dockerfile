FROM python

WORKDIR /app

COPY requirement.txt .

RUN pip install -r requirement.txt

COPY . /app

EXPOSE 8080

CMD [ "python", "-m", "src.main" ]
