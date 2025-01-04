# Monitoring module

This is the monitoring module to detect vm/host failure.

## Steps

- Configure each VM and host,

  - Replace VM1 with VM/Host name
  - Replace the ip address with the ip address of the host running the monitoring module

  ```bash
  # View cron jobs
  crontab -l
  # Edit cron jobs
  crontab -e
  ```

  ```bash
  * * * * * curl http://10.22.196.123:5000/notify/VM1
  * * * * * (sleep 30 ; curl http://10.22.196.123:5000/notify/VM1)
  ```

- Start the monitoring module

  ```bash
  export FLASK_ENV=development
  export FLASK_APP=./monitoring-module/heartbeat-service.py
  flask run --host=0.0.0.0
  ```
