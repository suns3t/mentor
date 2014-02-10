# MAPS Mentor Webform 
## Install
Install neccessary softwares for the project

    virtualenv-2.6 --no-site-packages .env
    source .env/bin/activate
    pip install -r requirements.txt
    
    
Create a local copy of the example settings, and configure the SECRET_KEY and DB config

    cp mentor/settings/local.py.example aol/settings/local.py
    vi mentor/settings/local.py
    
Change some settings for the website in base.py such as EMAIL_LIST

    vi mentor/settings/base.py

