FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install markdown



COPY . .

ENV PYTHONPATH=/app
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0

EXPOSE 8501

WORKDIR dashboard/src/dashboard

CMD ["streamlit", "run", "conversational_chatbot.py"]