#!/usr/bin/env bash
# shellcheck disable=SC2006
PID=`ps -ef|grep RestController.py |grep -v "grep"|awk '{print $2}'`;
echo "查出RestController.py相关的进程PID: $PID"
if [ -z "$PID" ]; then
    p=`nohup python3 /home/pythonWork/devicesSendMsg/RestController.py >> /home/pythonWork/ims.log 2>&1&`
    else
      # shellcheck disable=SC2086
      killId=`kill -9 ${PID}`;
      echo "杀死进程：$killId";
      # shellcheck disable=SC2006
      p=`nohup python3 /home/pythonWork/devicesSendMsg/RestController.py >> /home/pythonWork/ims.log 2>&1&`
      echo "${p}";
fi
exit;