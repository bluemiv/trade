FROM python:3.11.9-slim

RUN apt-get -y update

WORKDIR /home/service/

COPY . /home/service/
RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -U -r requirements.txt

CMD ["python3", "loop_infinite_trade.py"]