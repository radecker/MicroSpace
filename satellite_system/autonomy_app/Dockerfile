FROM python:3.7

# working directory
WORKDIR /usr/src/app

# add the python application
ADD autonomy_app.py .
ADD message_pb2.py .
ADD TCPClient.py .
ADD UDPClient.py .

# copy requirements file to working directory
COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT ["python", "./autonomy_app.py"]
