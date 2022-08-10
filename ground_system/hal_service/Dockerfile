FROM python:3.9

# working directory
WORKDIR /usr/src/app

# add the python application
ADD hal_service.py .
ADD message_pb2.py .
ADD config_pb2.py .
ADD BaseApp.py .
ADD Arduino.py .
ADD TCPServer.py .
ADD TCPClient.py .
ADD UDPClient.py .

# copy requirements file to working directory
COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT ["python", "./hal_service.py"]
