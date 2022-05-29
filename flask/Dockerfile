FROM python:3.10

WORKDIR /
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN mkdir app
COPY . app
CMD ["gunicorn", "-w 4", "-b 0.0.0.0:8001", "app.app:app"]
EXPOSE 8001
