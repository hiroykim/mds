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
username=dmnmds              ; default is no username (open server)
password=mds!@34               ; default is no password (open server)

[inet_http_server]         ; inet (TCP) server disabled by default
port=*:8000                ; ip_address:port specifier, *:port for all iface
username=dmnmds              ; default is no username (open server)
password=mds!@34               ; default is no password (open server)

[supervisorctl]
serverurl=unix:///tmp/supervisor.sock ; use a unix:// URL  for a unix socket
serverurl=http://127.0.0.1:8000 ; use an http:// url to specify an inet socket
username=dmnmds              ; should be same as in [*_http_server] if set
password=mds!@34                ; should be same as in [*_http_server] if set
;prompt=mysupervisor         ; cmd line prompt (default "supervisor")
;history_file=~/.sc_history  ; use readline history if available


[program:AA_KMS_API]
command=/usr/bin/bash /application/mds/dssrc/python/start_kmv_8888.sh
autostart=true
autorestart=true
stderr_logfile=/tmp/svd_mkms_web1.err.log
stdout_logfile=/tmp/svd_mkms_web1.out.log
------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------
#계정정보
	meritz_admin/DeepLearning2@21
	dmnmds/mds!@34
	메리츠!@34

#python3.6설치
	yum update -y
	yum search python36
	yum install python36 -y

#git 설치
	yum install git -y

#dmnmds 설정
	su - dmnmds
	python3 -m venv venv
	.bashrc ----> . ~/venv/bin/activate
	pip install --upgrade pip
	pip install tensorflow-gpu==2.0.0

	git clone https://github.com/hiroykim/mds.git mds
	pip install h5py==2.10.0
	pip install gunicorn flask flask_restful flask_cors supervisor
	pip install APScheduler beautifulsoup4 elastic-apm elasticsearch flashtext locust

#tensorflow2.4 설치
	deactivate
	python3 -m venv venv24
	. venv24/bin/activate
	pip install --upgrade pip
	pip install tensorflow==2.4.0
	pip install h5py==2.10.0
	pip install gunicorn flask flask_restful flask_cors supervisor
	pip install APScheduler beautifulsoup4 elastic-apm elasticsearch flashtext locust

#cuda설정
	yum install gcc -y
	yum install kernel-devel -y
	.bash_rc ----> export LD_LIBRARY_PATH=/usr/local/cuda/lib64
            MS에서 cuda 11.2.2 설치 후 10도 가능함(?)
		bash cuda_10.0.130_410.48_linux.run
		bash cuda_10.0.130.1_linux.run
                        'cp' -f include/* /usr/local/cuda/include/
		'cp' -f lib64/* /usr/local/cuda/lib64/
            rm /etc/ld.so.conf.d/000_cuda.conf; ldconfig -v

	bash cuda_11.2.2_460.32.03_linux.run

#cuda download
	wget https://developer.download.nvidia.com/compute/cuda/11.3.0/local_installers/cuda_11.3.0_465.19.01_linux.run
	wget https://developer.download.nvidia.com/compute/cuda/11.2.2/local_installers/cuda_11.2.2_460.32.03_linux.run
------------------------------------------------------------------------------------------------
ElasticSearch APM Server
------------------------------------------------------------------------------------------------
#python3.6설치
	yum update -y
	yum search python36
	yum install python36 -y

#git 설치
	yum install git -y

#dmnmds 설정
	su - dmnmds
	python3 -m venv venv
	.bashrc ----> . ~/venv/bin/activate
	pip install --upgrade pip
	pip install tensorflow-gpu==2.0.0

	git clone https://github.com/hiroykim/mds.git mds
	pip install h5py==2.10.0
	pip install gunicorn flask flask_restful flask_cors supervisor
	pip install APScheduler beautifulsoup4 elastic-apm elasticsearch flashtext locust