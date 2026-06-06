#!/bin/bash
EVENT=$1
TOOL=$2
FILE=$3
RESULT=$4
NOTE=$5

TIMESTAMP=$(date +%Y-%m-%dT%H:%M:%S+0530)
LOG_FILE="/Users/AayushShukla/Desktop/seo-command-center/.claude/audit.jsonl"

printf '{"timestamp": "%s", "event": "%s", "tool": "%s", "file": "%s", "result": "%s", "note": "%s"}\n' \
"$TIMESTAMP" "$EVENT" "$TOOL" "$FILE" "$RESULT" "$NOTE" >> "$LOG_FILE"
