#!/bin/sh
#
# Install Python dependencies according the
# environment.
#
REQUIREMENTS_PATH="requirements.txt"
EXPORT_CMD="poetry export --format requirements.txt --output $REQUIREMENTS_PATH"

if [ "$ENV" = "dev" ]; then
    eval "$EXPORT_CMD"
else
    eval "$EXPORT_CMD --only main"
fi

pip install --no-cache-dir --user --requirement $REQUIREMENTS_PATH
