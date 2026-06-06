#!/bin/bash
echo "{\"event\":\"$1\",\"ts\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\"}" >> .claude/audit.jsonl
