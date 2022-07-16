FROM python:3.9
WORKDIR /

COPY ./requirement.txt .
RUN pip install -r requirement.txt
COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host=0.0.0.0", "--reload"]
