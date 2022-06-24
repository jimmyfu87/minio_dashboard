

FROM python:3.7


COPY ./ /

WORKDIR /

RUN pip install -r requirements.txt

EXPOSE 8080

CMD ["python", "main.py"]

