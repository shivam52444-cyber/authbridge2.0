FROM python:3.11.9-slim

WORKDIR /app

COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirment.txt

EXPOSE 10000

CMD ["streamlit", "run", "main_app.py", "--server.port=10000", "--server.address=0.0.0.0"]
