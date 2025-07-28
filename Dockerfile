FROM alpine:latest

RUN mkdir -p /root/navidrome/config /root/navidrome/music

RUN apk update && \
    apk add --no-cache python3 py3-pip curl ffmpeg

RUN curl -L https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp -o /usr/local/bin/yt-dlp
RUN chmod +x /usr/local/bin/yt-dlp

WORKDIR /root/downloader-service
COPY /downloader-service/* /root/downloader-service/

WORKDIR /root/downloader-service

RUN chmod +x downloader-yt.sh
RUN pip install fastapi uvicorn --break-system-packages

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
