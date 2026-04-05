FROM eclipse-temurin:21-jre

WORKDIR /app

RUN apt-get update && apt-get install -y curl python3 python3-pip && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip3 install --no-cache-dir --break-system-packages -r requirements.txt

COPY app.py .
COPY mc /app/mc

RUN cd /app/mc && \
    if [ ! -f server.jar ]; then \
        echo "Downloading Paper Minecraft server..."; \
        curl -L -o /tmp/paper.jar https://api.papermc.io/v2/projects/paper/versions/1.21.1/builds/128/downloads/paper-1.21.1-128.jar && \
        if [ $(stat -f%z /tmp/paper.jar 2>/dev/null || stat -c%s /tmp/paper.jar) -gt 10485760 ]; then \
            mv /tmp/paper.jar server.jar; \
        else \
            echo "Download failed or file too small"; \
            exit 1; \
        fi; \
    fi

EXPOSE 7860

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]
