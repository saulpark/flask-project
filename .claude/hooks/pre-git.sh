#!/bin/bash
# Pre-git hook: runs pytest before git commit or push
# Receives tool input as JSON on stdin

INPUT=$(cat)
COMMAND=$(echo "$INPUT" | python -c "import sys,json; d=json.load(sys.stdin); print(d.get('tool_input',{}).get('command',''))" 2>/dev/null)

# Only act on git commit or git push
if [[ "$COMMAND" != *"git commit"* && "$COMMAND" != *"git push"* ]]; then
  exit 0
fi

echo "--- Pre-git hook: running tests ---" >&2

cd "$(git rev-parse --show-toplevel)" || exit 1

python -m pytest tests/ -v 2>&1
RESULT=$?

if [ $RESULT -ne 0 ]; then
  echo "--- Tests failed. Blocking git operation. ---" >&2
  exit 2  # exit 2 blocks the tool and sends output to Claude
fi

echo "--- Tests passed. Proceeding. ---" >&2
exit 0
