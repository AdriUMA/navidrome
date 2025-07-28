#!/bin/bash

OUTPUT_FOLDER="/music"

if [ -z "$1" ]; then
  logger "Use: $0 <YouTube URL>. Current output folder is $OUTPUT_FOLDER."
  exit 1
fi

logger "Processing $0"

yt-dlp \
  --extract-audio \
  --audio-format mp3 \
  --audio-quality 0 \
  --embed-thumbnail \
  --add-metadata \
  --metadata-from-title "%(artist)s - %(title)s" \
  -o "${OUTPUT_FOLDER}/%(artist)s - %(title)s.%(ext)s" \
  "$1"

logger "Done $0"
