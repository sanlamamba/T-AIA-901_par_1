#!/bin/bash

# download_vosk_model.sh
# Script to download the Vosk French model and place it inside the app's models directory.

set -e  # Exit immediately if a command exits with a non-zero status.

# Variables
MODEL_URL="https://alphacephei.com/vosk/models/vosk-model-small-fr-0.22.zip"
MODEL_ZIP="vosk-model-small-fr-0.22.zip"
MODEL_DIR="vosk-model-small-fr-0.22"

# Get the absolute path to the script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_DIR="$SCRIPT_DIR/app/models"

log() {
    echo "[INFO] $1"
}

command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Ensure curl is available
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

# Temporary directory for download
TEMP_DIR=$(mktemp -d)
log "Created temporary directory at $TEMP_DIR"

cd "$TEMP_DIR"

# Download Vosk model
log "Downloading Vosk model from $MODEL_URL..."
if [[ "$DOWNLOADER" == "curl" ]]; then
    curl -L "$MODEL_URL" -o "$MODEL_ZIP"
elif [[ "$DOWNLOADER" == "wget" ]]; then
    wget "$MODEL_URL" -O "$MODEL_ZIP"
fi

log "Download completed."

# Unzip the model
log "Unzipping the model..."
unzip "$MODEL_ZIP"

log "Unzipping completed."

# Ensure the target directory exists
if [[ ! -d "$APP_DIR" ]]; then
    log "Target directory '$APP_DIR' does not exist. Creating it..."
    mkdir -p "$APP_DIR"
fi

# Move the model to the target directory
log "Moving the model to '$APP_DIR'..."
mv "$MODEL_DIR" "$APP_DIR"

log "Model has been successfully placed in '$APP_DIR'."

# Cleanup
log "Cleaning up temporary files..."
cd /
rm -rf "$TEMP_DIR"

log "Cleanup completed. Script finished successfully."
