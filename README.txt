#  'str' object has no attribute 'decode'
  -> pip install h5py==2.10.0

# momory alloc error
  -> https://inpages.tistory.com/155

# python3.5.4
./configure --with-openssl=/usr/src/openssl-1.0.2o --enable-optimizations

pip install supervisor
echo_supervisord_conf > supervisord.conf

[unix_http_server]
file=/tmp/supervisor.sock   ; the path to the socket file
chmod=0700                 ; socket file mode (default 0700)
;chown=nobody:nogroup       ; socket file uid:gid owner
username=dmnmkms           ; default is no username (open server)
password=1234               ; default is no password (open server)

[inet_http_server]         ; inet (TCP) server disabled by default
port=*:9001        ; ip_address:port specifier, *:port for all iface
username=dmnmkms              ; default is no username (open server)
password=1234               ; default is no password (open server)

[program:ES_Search_API_1]
command=/usr/bin/bash %(ENV_PROJECT_HOME)s/start_mkms_web1.sh
autostart=false
autorestart=false
stderr_logfile=%(ENV_LOG_HOME)s/svd_mkms_web1.err.log
stdout_logfile=%(ENV_LOG_HOME)s/svd_mkms_web1.out.log
