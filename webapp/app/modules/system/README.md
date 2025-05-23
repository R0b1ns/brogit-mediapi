# Requirements

crontab

# Config

SCRIPT_PATH = "/usr/local/bin/auto_apt_update.sh"
CRON_JOB = f"0 3 * * * sudo {SCRIPT_PATH}"