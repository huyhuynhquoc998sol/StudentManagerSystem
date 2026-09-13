# mt python 3.10 nhe
FROM python:3.10-slim

# bofile rac+hienloi
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# cd gd tkinter+driver-pmkn sql
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-tk \
    g++ \
    unixodbc-dev \
    && rm -rf /var/lib/apt/lists/*

# thumuc lv
WORKDIR /app

# cdthuvien requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# allcode c nhom-container
COPY . .

# chay
CMD ["python", "app.py"]