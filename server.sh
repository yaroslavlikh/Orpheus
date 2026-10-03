#!/usr/bin/env bash

set -euo pipefail

cd "$(dirname "$0")"

NEMO="$HOME/.local/bin/nemo-speech"
PYTHON="/usr/local/bin/python3"
"$NEMO" serve --asr-model nvidia/nemotron-3.5-asr-streaming-0.6b --no-ui --endpointing > server.log 2>&1 &
SERVER_PID=$!
trap 'kill "$SERVER_PID" 2>/dev/null' EXIT

"$NEMO" health --wait 120 --quiet

"$PYTHON" src/main.py