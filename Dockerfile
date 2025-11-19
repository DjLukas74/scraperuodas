FROM python:3.12-slim

# ---------- System Dependencies ----------
RUN apt-get update && apt-get install -y \
    wget curl unzip gnupg \
    xvfb xauth x11-apps \
    libglib2.0-0 libnss3 libx11-6 libxcomposite1 libxcursor1 libxdamage1 \
    libxi6 libxtst6 libcups2 libxrandr2 libasound2 libatk1.0-0 \
    libatk-bridge2.0-0 libpangocairo-1.0-0 libgtk-3-0 libpango-1.0-0 \
    libcairo2 libatspi2.0-0 libdrm2 libgbm1 libxkbcommon0 \
    tigervnc-standalone-server fluxbox \
    && rm -rf /var/lib/apt/lists/*

# ---------- Python + Playwright ----------
RUN pip install playwright beautifulsoup4 lxml && playwright install --with-deps chromium

# Workdir
WORKDIR /app
COPY . /app

# Default command (headless scraping)
CMD ["python", "main.py"]
