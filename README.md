# DOMjudge

## OS Requirment
* Debian-10.10.0-amd64

## 網站安裝可以直接參考以下網址
* https://docs.dmoj.ca/#/site/installation 

## Judge 安裝可以直接參考以下網址
* https://docs.dmoj.ca/#/judge/setting_up_a_judge

## 網站安裝
### Installing the prerequisites
```
$ apt update
$ apt install git gcc g++ make python3-dev python3-pip libxml2-dev libxslt1-dev zlib1g-dev gettext curl redis-server
$ curl -sL https://deb.nodesource.com/setup_12.x | sudo -E bash -
$ apt install nodejs
$ npm install -g sass postcss-cli postcss autoprefixer
```
### Creating the database
 首先要到網站下載 MariaDB https://mariadb.org/download/?t=repo-config&d=Arch+Linux
 ```
 $ apt update
 $ apt install mariadb-server libmysqlclient-dev
 ```
 再來是設定資料庫

 設定 mysql 資料庫，預設 root 密碼為空白，直接按下 Enter，資料庫帳號為 dmoj

 需修改 \<mariadb user password\> 為資料庫密碼
 ```
 $ sudo mysql
 mariadb> CREATE DATABASE dmoj DEFAULT CHARACTER SET utf8mb4 DEFAULT COLLATE utf8mb4_general_ci;
 mariadb> GRANT ALL PRIVILEGES ON dmoj.* TO 'dmoj'@'localhost' IDENTIFIED BY '<mariadb user password>';
 mariadb> exit
 ```
### Installing prerequisites
 建立與啟動 Python3 虛擬環境
 ```
 $ python3 -m venv dmojsite
 $ . dmojsite/bin/activate  
 ```
 下載程式與資源檔案
 ```
 (dmojsite) $ git clone https://github.com/DMOJ/site.git
 (dmojsite) $ cd site
 (dmojsite) $ git checkout v1.4.0   # only if planning to install a judge from PyPI, otherwise skip this step
 (dmojsite) $ git submodule init
 (dmojsite) $ git submodule update
 ```
 在虛擬環境下安裝 python3 所需套件
 ```
 (dmojsite) $ pip3 install -r requirements.txt
 (dmojsite) $ pip3 install mysqlclient websocket-client
 ```
 在 dmoj 資料夾下新增 local_settings.py

 自 https://github.com/DMOJ/docs/blob/master/sample_files/local_settings.py 進行修改

 檢查網站是否正常運作
 ```
 (dmojsite) $ python3 manage.py check
 ```
### Compiling assets
 收集 static 檔案
 ```
 (dmojsite) $ ./make_style.sh
 (dmojsite) $ python3 manage.py collectstatic
 ```
 建立語言檔
 ```
 (dmojsite) $ python3 manage.py compilemessages
 (dmojsite) $ python3 manage.py compilejsi18n
 ```
### Setting up database tables
 建立資料庫內的資料表
 ```
 (dmojsite) $ python3 manage.py migrate
 ```
 載入測試資料
 ```
 (dmojsite) $ python3 manage.py loaddata navbar
 (dmojsite) $ python3 manage.py loaddata language_small
 (dmojsite) $ python3 manage.py loaddata demo
 ```
 `Keep in mind that the demo fixture creates a superuser account with a username and password of admin.`

 `留意 demo 會產生 帳號 、 密碼為 admin 的使用者，記得之後要更改密碼`

 新增 Superuser 帳號
 ```
 (dmojsite) $ python3 manage.py createsuperuser
 ```
### Setting up Celery
 啟用 redis
 ```
 (dmojsite) $ service redis-server start
 ```
 從 local_settings.py 取消註解 CELERY_BROKER_URL 和 CELERY_RESULT_BACKEND. 

### Running the server
 在 dmoj/settings.py 的 ALLOWED_HOSTS 新增主機IP，如右，ALLOWED_HOSTS = ['140.138.145.203']
 ```
 (dmojsite) $ python3 manage.py runserver 0.0.0.0:8000
 ```
 到 http://140.138.145.203:8000 確認網站是否運行，能運行就按 Ctrl-C 離開
 ```
 (dmojsite) $ python3 manage.py runbridged
 ```
 啟用 Bridge，沒出現錯誤就 Ctrl+C 離開

 在 local_settings.py 取消註解 CELERY_BROKER_URL 與 CELERY_RESULT_BACKEND
 ```
 (dmojsite) $ celery -A dmoj_celery worker
 ```
 沒出現錯誤就 Ctrl+C 離開
### Setting up uWSGI
 安裝 uwsgi
 ```
 (dmojsite) $ pip3 install uwsgi
 ```
 複製 https://github.com/DMOJ/docs/blob/master/sample_files/uwsgi.ini 的檔案，並更改網站檔案路徑，虛擬環境檔案路徑
 ```
 (dmojsite) $ uwsgi --ini uwsgi.ini
 ```
 出現 spawned 表示正常，使用 Ctrl+C 離開
 ### Setting up supervisord
 ```
 $ apt install supervisor
 ```
 在 /etc/supervisor/conf.d/ 下建立設定檔 site.conf 、 bridged.conf 和 celery.conf
 * https://github.com/DMOJ/docs/blob/master/sample_files/site.conf
 * https://github.com/DMOJ/docs/blob/master/sample_files/bridged.conf
 * https://github.com/DMOJ/docs/blob/master/sample_files/celery.conf
 記得更改設定檔內的檔案路徑，celery 的設定檔 user 和 group 設為 `root`
 ```
 $ supervisorctl update
 $ supervisorctl status
 ```
### Setting up nginx
 ```
 $ apt install nginx
 ```
 在 /etc/nginx/conf.d/ 下建立設定檔 nginx.conf
 * https://github.com/DMOJ/docs/blob/master/sample_files/nginx.conf

 <hostname> 和 port 記得要更改 `140.138.145.203` 和 `8080` port

 再來測試
 ```
 $ nginx -t
 ```

 啟動 nginx
 ```
 $ service nginx start
 ```
 使用瀏覽器打開 http:/140.138.145.203:8080 就可以看到 nginx 所啟動的 DOMjudge

### Configuration of event server
 新增 /home/DOMjudge/site/websocket/config.js 如下
 ```
 (dmojsite) $ cat > websocket/config.js
 module.exports = {
     get_host: '127.0.0.1',
     get_port: 15100,
     post_host: '127.0.0.1',
     post_port: 15101,
     http_host: '127.0.0.1',
     http_port: 15102,
     long_poll_timeout: 29000,
 };
 ```
 在 local_settings.py 的 EVENT_DAEMON_POST 、 EVENT_DAEMON_GET 與 EVENT_DAEMON_POLL 需設定，在前面 local_settings.py 中已經加上。

 再來安裝套件
 ```
 (dmojsite) $ npm install qu ws simplesets
 (dmojsite) $ pip3 install websocket-client 
 ```
 在 /etc/supervisor/conf.d/ 下建立設定檔 wsevent.conf
 * https://github.com/DMOJ/docs/blob/master/sample_files/wsevent.conf
 
 最後重新啟動服務
 ```
$ supervisorctl update
$ supervisorctl restart all
$ service nginx restart
 ```
 

## Judge server 安裝
### Site-side setup
 登入DMOJ的管理者，點選「Submmissions -> Judge」，新增 Judge 主機的 Name 與產生 authentication key
 
 ![github](https://github.com/TsaiYuanW/DOMjudge/blob/main/judge.png)
 
將 Judge 主機的 Name 與 key 填入 judge.yml 的 id 與 key ，如下範例。
```
id: pc2
key: "uB3ehed:g+q#;LYa;-rN<z#Cxxxxxxxxxxxxxxxxxxxxxxxx"
```
### Installing the prerequisites
```
$ apt install python3-dev python3-pip build-essential libseccomp-dev
$ pip3 install dmoj
```
### Configuring the judge
使用 dmoj-autoconf 產生 runtime 的設定，貼到 /home/domjudge/site/judge.yml

使用 problem_storage_root 設定測資資料夾，建立資料夾 /home/domjudge/site/problems，資料夾下需要有該題測資，該題目才會有此 judge server，出題時題目測資會上傳到此資料夾
```
id: pc2
key: v{2$X`8Hk)dg.j&3vNo7ZzkN0c+.J9ZS!6>Nj0!*1.NtJOp^o%c;qUYvzb7:[TC-6aA_Zw#2%4<%-ybUe^tOc7/b9]X#-4g*5EsP
problem_storage_root:
  - /home/domjudge/problems
runtime:
  g++14: /usr/bin/g++
```
使用 Supervisor 啟動 Judge Server
 
編輯 /etc/supervisor/conf.d/judge.conf
* https://github.com/TsaiYuanW/DOMjudge/blob/main/supervisor/conf.d/judge.conf
```
$ supervisorctl update
$ supervisorctl restart all
$ supervisorctl status
```
