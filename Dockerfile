FROM python:3.11.6
RUN mkdir -p /app
WORKDIR /app
COPY . /app
RUN apt-get update && apt-get install -y portaudio19-dev
RUN apt-get update && apt-get install -y ffmpeg
RUN pip install -r requirements.txt
EXPOSE 8000
CMD ["python","manage.py","runserver","0.0.0.0:8000"]