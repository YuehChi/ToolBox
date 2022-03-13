# ToolBox
## Django Toolfamily
welcome to this project~

## Quick Start
To get this project up and running locally on your computer:

Set up the Python development environment. We recommend using a Python virtual environment.
Note: This has been tested against Django 4.0.3 (and may not work or be "optimal" for other versions).

Assuming you have Python setup, run the following commands (if you're on Windows you may use py or py -3 instead of python to start Python):

Remember manage.py in the toolcase folder ， so you need to cd toolcase
1. pip3 install -r requirements.txt
2. python3 manage.py makemigrations
3. python3 manage.py migrate
4. python3 manage.py collectstatic
5. python3 manage.py createsuperuser # Create a superuser
6. python3 manage.py runserver

Open a browser to http://127.0.0.1:8000/admin/ to open the admin site
Create a few test objects of each type.
Open tab to http://127.0.0.1:8000 to see the main site, with your new objects.

## Clone
### clone的指令
`git clone https://github.com/YuehChi/ToolBox.git/`

### Possible error
如果遇到以下error...  
Cloning into 'ToolBox'...
remote: Support for password authentication was removed on August 13, 2021. Please use a personal access token instead.
remote: Please see https://github.blog/2020-12-15-token-authentication-requirements-for-git-operations/ for more information.
fatal: Authentication failed for 'https://github.com/YuehChi/ToolBox.git/'

##### 解決方法：
1. 到 GitHub>>個人頭像>>Settings>>(左下)Developer Settings>>Personal access tokens>>Generate new token
2. Expiration可以設長一點，下面要勾repo，然後就可以Generate token，之後就會得到一串token
3. 再執行一次指令，會被要求輸入使用者名稱跟token：  
`git clone https://github.com/YuehChi/ToolBox.git/`  
Username: your_username //輸入使用者名稱  
Password: your_token //輸入token

