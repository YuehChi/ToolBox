chcp 65001
::設定中文相容性

@Echo On
::設定接下來的程式碼都要顯示在視窗裡(@表示不顯示這一行的命令)


python manage.py migrate

::執行後會開啟命令提示字元 
::(::表示註解，註解無論Echo off還是on都不會顯示)
::此程式僅適用於windows系統

pause
::這是為了不要讓視窗一執行完就關掉
