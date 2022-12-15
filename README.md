# DOMjudge

## OS Requirment
* Debian-10.10.0-amd64

## 網站安裝可以直接參考以下網址
* https://docs.dmoj.ca/#/site/installation 
* https://sites.google.com/site/zsgititit/home/freebsd/zaiubuntu-an-zhuang-xian-shang-jie-ti-xi-tongdmoj

## Judge 安裝可以直接參考以下網址
* https://docs.dmoj.ca/#/judge/setting_up_a_judge
* https://sites.google.com/site/zsgititit/home/freebsd/zaiubuntu-an-zhuangdmoj-judge-server

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
  
