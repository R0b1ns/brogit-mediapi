#!/bin/bash

# brogit (c) 2024
# Author: r0b1ns

# Install process controller
sudo apt install -y supervisor

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

PROJECT_RELATIVE_ROOT="../"
PROJECT_ROOT_PATH="$(cd "$SCRIPT_DIR/$PROJECT_RELATIVE_ROOT" && pwd)"

WEBAPP_ROOT_PATH="$SCRIPT_DIR"

# Install and deploy app
source "$WEBAPP_ROOT_PATH/deploy.sh"

# TODO: Ensure right user is configured
# source "$PROJECT_ROOT_PATH/change_user.sh"

source "$PROJECT_ROOT_PATH/load_config.sh"

PROJECT_NAME="${config[project_name]}_webapp"
PROJECT_USER="${config[project_user]}"
APP_NAME="app"
PROJECT_DIR="$WEBAPP_ROOT_PATH/$APP_NAME"
HOST="${config[host]}"
PORT="${config[port]}"
LOG_OUT_FILEPATH="${config[log_dir]}/${config[project_name]}.log"
LOG_ERR_FILEPATH="${config[log_dir]}/${config[project_name]}.err.log"

cat << EOF | sudo tee /etc/supervisor/conf.d/$PROJECT_NAME.conf > /dev/null
[program:$PROJECT_NAME]
; directory to cwd to before exec (def no cwd)
directory=$PROJECT_DIR

; the program (relative uses PATH, can take args)
command=$WEBAPP_ROOT_PATH/.venv/bin/gunicorn $APP_NAME:$APP_NAME -b $HOST:$PORT

; Execute with defined user
user=$PROJECT_USER

; process_name expr (default %(program_name)s)
process_name=%(program_name)s_%(process_num)02d

; start at supervisord start (default: true)
autostart=true

; whether/when to restart (default: unexpected)
autorestart=true

;numprocs=3                    ; number of processes copies to start (def 1)
;umask=022                     ; umask for process (default None)
;priority=999                  ; the relative start priority (default 999)
;startsecs=1                   ; number of secs prog must stay running (def. 1)
;startretries=3                ; max # of serial start failures (default 3)
;exitcodes=0,2                 ; 'expected' exit codes for process (default 0,2)
;stopsignal=TERM               ; signal used to kill process (default TERM)
;stopwaitsecs=10               ; max num secs to wait b4 SIGKILL (default 10)
;stopasgroup=true             ; send stop signal to the UNIX process group (default false)
;killasgroup=true             ; SIGKILL the UNIX process group (def false)

;redirect_stderr=true          ; redirect proc stderr to stdout (default false)

; stdout log path, NONE for none; default AUTO
stdout_logfile=$LOG_OUT_FILEPATH

; max # logfile bytes b4 rotation (default 50MB)
stdout_logfile_maxbytes=1MB

;stdout_logfile_backups=10     ; # of stdout logfile backups (default 10)
;stdout_capture_maxbytes=1MB   ; number of bytes in 'capturemode' (default 0)
;stdout_events_enabled=false   ; emit events on stdout writes (default false)


; stderr log path, NONE for none; default AUTO
stderr_logfile=$LOG_ERR_FILEPATH

; max # logfile bytes b4 rotation (default 50MB)
stderr_logfile_maxbytes=1MB


;stderr_logfile_backups=10     ; # of stderr logfile backups (default 10)
;stderr_capture_maxbytes=1MB   ; number of bytes in 'capturemode' (default 0)
;stderr_events_enabled=false   ; emit events on stderr writes (default false)
;environment=A="1",B="2"       ; process environment additions (def no adds)
EOF

sudo supervisorctl reread
sudo service supervisor restart