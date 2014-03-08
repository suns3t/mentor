# MAPS Mentor Webform 
## Install
Go to mentor directory, install neccessary softwares for the project

    virtualenv-2.6 --no-site-packages .env
    source .env/bin/activate
    pip install -r requirements.txt
    
Install freetype-devel in order to use captcha package

    yum install freetype-devel
    
Create a local copy of the example settings, and configure the SECRET_KEY and DB config

    cp mentor/settings/local.py.example mentor/settings/local.py
    vi mentor/settings/local.py
    
Change some settings for the website in base.py such as EMAIL_LIST

    vi mentor/settings/base.py

