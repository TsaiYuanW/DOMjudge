1. 將檔案放入 ./site/judge 資料夾
2. 啟動虛擬環境 dmojsite
3. 執行以下指令
```
(dmojsite) $ python manage.py makemigrations
```
如果不行，將 ./site/judge/migrations 內除了 __init__.py 的檔案刪除，並在執行一次 makemigrations

再來遷移資料
```
(dmojsite) $ python manage.py migrate
```
重新啟動網站，並確認狀態
```
(dmojsite) $ supervisorctl restart all
(dmojsite) $ supervisorctl status
```
