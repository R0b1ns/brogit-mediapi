#!/bin/bash

# brogit (c) 2024
# Author: r0b1ns

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

PROJECT_RELATIVE_ROOT="../"
PROJECT_ROOT_PATH="$(cd "$SCRIPT_DIR/$PROJECT_RELATIVE_ROOT" && pwd)"

source "$PROJECT_ROOT_PATH/load_config.sh"

echo "${config[log_dir]}"

exit 0

sudo apt install supervisor


# /etc/supervisor/conf.d/mediapi_webapp.conf
[program:hello_world]
directory=/home/userkdo/domains/domain/public_html/bot1                ; directory to cwd to before exec (def no cwd)


command=/home/ubuntu/.env/bin/gunicorn app:app -b localhost:8000           ; the program (relative uses PATH, can take args)
process_name=%(program_name)s_%(process_num)02d ; process_name expr (default %(program_name)s)
numprocs=3                    ; number of processes copies to start (def 1)
;umask=022                     ; umask for process (default None)
;priority=999                  ; the relative start priority (default 999)
autostart=true                ; start at supervisord start (default: true)
autorestart=true        ; whether/when to restart (default: unexpected)
;startsecs=1                   ; number of secs prog must stay running (def. 1)
;startretries=3                ; max # of serial start failures (default 3)
;exitcodes=0,2                 ; 'expected' exit codes for process (default 0,2)
;stopsignal=TERM               ; signal used to kill process (default TERM)
;stopwaitsecs=10               ; max num secs to wait b4 SIGKILL (default 10)
;stopasgroup=true             ; send stop signal to the UNIX process group (default false)
;killasgroup=true             ; SIGKILL the UNIX process group (def false)

user=mediapi
;redirect_stderr=true          ; redirect proc stderr to stdout (default false)
stdout_logfile=/home/userkdo/domains/domain/public_html/bot1/log/log1.log        ; stdout log path, NONE for none; default AUTO
stdout_logfile_maxbytes=1MB   ; max # logfile bytes b4 rotation (default 50MB)
;stdout_logfile_backups=10     ; # of stdout logfile backups (default 10)
;stdout_capture_maxbytes=1MB   ; number of bytes in 'capturemode' (default 0)
;stdout_events_enabled=false   ; emit events on stdout writes (default false)
stderr_logfile=/home/userkdo/domains/domain/public_html/bot1/log/log1.err        ; stderr log path, NONE for none; default AUTO
stderr_logfile_maxbytes=1MB   ; max # logfile bytes b4 rotation (default 50MB)
;stderr_logfile_backups=10     ; # of stderr logfile backups (default 10)
;stderr_capture_maxbytes=1MB   ; number of bytes in 'capturemode' (default 0)
;stderr_events_enabled=false   ; emit events on stderr writes (default false)
;environment=A="1",B="2"       ; process environment additions (def no adds)

sudo supervisorctl reread
sudo service supervisor restart