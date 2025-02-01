#!/usr/bin/env bash
#
# download_vosk_model.sh

set -euo pipefail

############################################################
# Configuration
############################################################
MODEL_URL="https://alphacephei.com/vosk/models/vosk-model-small-fr-0.22.zip"
MODEL_ZIP="vosk-model-small-fr-0.22.zip"
MODEL_DIR="vosk-model-small-fr-0.22"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_DIR="$SCRIPT_DIR/app/models"

############################################################
# Helpers
############################################################
log_info() {
    echo -e "[\033[1;34mINFO\033[0m] $*"
}

log_error() {
    echo -e "[\033[1;31mERROR\033[0m] $*" >&2
}

############################################################
# Clean up function
############################################################
TEMP_DIR=""
cleanup() {
    if [[ -n "$TEMP_DIR" && -d "$TEMP_DIR" ]]; then
        log_info "Cleaning up temporary directory: $TEMP_DIR"
        rm -rf "$TEMP_DIR"
    fi
}

trap cleanup EXIT

############################################################
# Check if a command exists
############################################################
command_exists() {
    command -v "$1" &>/dev/null
}

############################################################
# Attempt to install a command if it is missing
############################################################
try_install_command() {
    local cmd_name="$1"

    if command_exists "$cmd_name"; then
        return
    fi

    if [[ "$OSTYPE" == "linux-gnu"* || "$OSTYPE" == "linux"* ]]; then
        if command_exists apt-get; then
            log_info "'$cmd_name' not found. Installing via apt-get..."
            sudo apt-get update && sudo apt-get install -y "$cmd_name" && sudo apt-get install ffmpeg
        else
            log_error "Could not install '$cmd_name': 'apt-get' is not available on this system."
            exit 1
        fi
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        if command_exists brew; then
            log_info "'$cmd_name' not found. Installing via Homebrew..."
            brew install "$cmd_name"
            brew install ffmpeg
        else
            log_error "Could not install '$cmd_name': Homebrew is not installed."
            exit 1
        fi
    else
        log_error "Automatic installation not supported on this OS ($OSTYPE). Please install '$cmd_name' manually."
        exit 1
    fi
}

############################################################
# Main script flow
############################################################

try_install_command curl
if command_exists curl; then
    DOWNLOADER="curl"
elif command_exists wget; then
    DOWNLOADER="wget"
else
    log_error "Neither 'curl' nor 'wget' is installed and cannot be auto-installed. Please install one and re-run."
    exit 1
fi

try_install_command unzip
if ! command_exists unzip; then
    log_error "'unzip' is required but could not be installed automatically. Please install 'unzip' manually."
    exit 1
fi

TEMP_DIR="$(mktemp -d)"
log_info "Created temporary directory at: $TEMP_DIR"

log_info "Downloading Vosk model from $MODEL_URL..."
pushd "$TEMP_DIR" &>/dev/null

case "$DOWNLOADER" in
  "curl")
    curl -L "$MODEL_URL" -o "$MODEL_ZIP"
    ;;
  "wget")
    wget "$MODEL_URL" -O "$MODEL_ZIP"
    ;;
esac

log_info "Download completed."

log_info "Unzipping the model..."
unzip -q "$MODEL_ZIP"
log_info "Unzipping completed."

if [[ ! -d "$APP_DIR" ]]; then
    log_info "Target directory '$APP_DIR' does not exist. Creating it..."
    mkdir -p "$APP_DIR"
fi

log_info "Moving the model '$MODEL_DIR' to '$APP_DIR'..."
mv "$MODEL_DIR" "$APP_DIR"
log_info "Model has been successfully placed in '$APP_DIR/$MODEL_DIR'."

popd &>/dev/null

log_info "Script finished successfully."
