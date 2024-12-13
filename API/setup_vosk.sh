#!/bin/bash

# download_vosk_model.sh
# Script to download the Vosk French model and place it inside the app's models directory.

set -e 

# Variables
MODEL_URL="https://alphacephei.com/vosk/models/vosk-model-small-fr-0.22.zip"
MODEL_ZIP="vosk-model-small-fr-0.22.zip"
MODEL_DIR="vosk-model-small-fr-0.22"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_DIR="$SCRIPT_DIR/app/models"

log() {
    echo "[INFO] $1"
}

command_exists() {
    command -v "$1" >/dev/null 2>&1
}

if [[ "$OSTYPE" == "linux-gnu" || "$OSTYPE" == "darwin"* ]]; then
    if ! command_exists curl; then
        if [[ "$OSTYPE" == "linux-gnu" ]]; then
            sudo apt-get update
            sudo apt-get install -y curl
        elif [[ "$OSTYPE" == "darwin"* ]]; then
            brew install curl
        fi
    fi
fi

if command_exists curl; then
    DOWNLOADER="curl"
elif command_exists wget; then
    DOWNLOADER="wget"
else
    echo "Error: Neither curl nor wget is installed. Please install one to proceed."
    exit 1
fi

TEMP_DIR=$(mktemp -d)
log "Created temporary directory at $TEMP_DIR"

cd "$TEMP_DIR"

log "Downloading Vosk model from $MODEL_URL..."
if [[ "$DOWNLOADER" == "curl" ]]; then
    curl -L "$MODEL_URL" -o "$MODEL_ZIP"
elif [[ "$DOWNLOADER" == "wget" ]]; then
    wget "$MODEL_URL" -O "$MODEL_ZIP"
fi

log "Download completed."

log "Unzipping the model..."
unzip "$MODEL_ZIP"

log "Unzipping completed."

if [[ ! -d "$APP_DIR" ]]; then
    log "Target directory '$APP_DIR' does not exist. Creating it..."
    mkdir -p "$APP_DIR"
fi

log "Moving the model to '$APP_DIR'..."
mv "$MODEL_DIR" "$APP_DIR"

log "Model has been successfully placed in '$APP_DIR'."

log "Cleaning up temporary files..."
cd /
rm -rf "$TEMP_DIR"

log "Cleanup completed. Script finished successfully."
