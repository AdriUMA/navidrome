#!/bin/bash
# downloader_yt.sh - Descarga una canción de YouTube como MP3 con metadatos y carátula

DESTINO="/music"

if [ -z "$1" ]; then
  echo "Uso: $0 <URL de YouTube>"
  exit 1
fi

yt-dlp \
  --extract-audio \
  --audio-format mp3 \
  --audio-quality 0 \
  --embed-thumbnail \
  --add-metadata \
  --metadata-from-title "%(artist)s - %(title)s" \
  -o "${DESTINO}/%(artist)s - %(title)s.%(ext)s" \
  "$1"
