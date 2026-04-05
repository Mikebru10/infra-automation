#!/usr/bin/env bash
set -e

TARGET_DIR="/mnt/docker_nfs/docker/vUbtDoc-Infra-Crt-Prod-N01/prompt-optimizer/repo"

if [ ! -d "$TARGET_DIR" ]; then
  git clone https://github.com/Mikebru10/Export_Prompt.git "$TARGET_DIR"
else
  cd "$TARGET_DIR"
  git pull
fi
