#!/bin/sh
# Download the default TissueNet checkpoint, or pass filenames/--all/--list.
set -eu
SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
exec python3 "$SCRIPT_DIR/../download.py" "$@"
