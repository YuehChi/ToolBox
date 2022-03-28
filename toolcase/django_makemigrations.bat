chcp 65001
::設定中文相容性

@Echo On
::設定接下來的程式碼都要顯示在視窗裡(@表示不顯示這一行的命令)

python manage.py makemigrations

pause
::這是為了不要讓視窗一執行完就關掉
