FROM public.ecr.aws/lambda/python:3.13

WORKDIR /app

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .

CMD ["main.handler"]