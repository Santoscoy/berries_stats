FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./run.sh code/run.sh

RUN chmod +x code/run.sh

COPY ./app /code/app

CMD ["code/run.sh"]