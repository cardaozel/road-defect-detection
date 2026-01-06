#!/bin/bash
# Start the automatic training monitor
# This script will:
# 1. Wait for current training to complete
# 2. Check results against targets
# 3. Auto-start high-performance training if needed
# 4. Auto-resume if training gets killed

cd "$(dirname "$0")/.."

# Activate virtual environment
if [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
fi

# Create logs directory
mkdir -p logs

# Start the monitor (runs continuously)
echo "Starting automatic training monitor..."
echo "This will run continuously and auto-restart training if needed"
echo "Press Ctrl+C to stop"
echo ""

python3 scripts/auto_monitor_and_train.py

