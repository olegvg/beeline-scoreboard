# Deployment of backend onto single server

Assume that running user is _olegvg_.

Under the `olegvg` user:

## 1. Create directory tree

        sudo mkdir /opt/production
        sudo setfacl -m u:olegvg:rwx /opt/production
        mkdir /opt/production/{apps,log,virtual_envs}
        mkdir /opt/production/log/beeline-scoreboard
        mkdir /opt/production/virtual_envs/beeline-scoreboard

## 2. Prepare login environment for git+ssh access to repository as mentioned [here](ssh_to_git.md)

## 3. Clone the last version

        git clone git@bitbucket.org:olegvg/beeline-scoreboard.git /opt/production/apps/beeline-scoreboard

## 4. Install `virtualenv` in Debian way

        apt-get install python-virtualenv

## 5. Create virtual environment

        virtualenv /opt/production/virtual_envs/beeline-scoreboard
        ln -s /opt/production/apps/beeline-scoreboard/requirements.txt /opt/production/virtual_envs/beeline-scoreboard/requirements.txt

## 6. Install devel `.deb`-s which are needed to build `psycopg2`

        apt-get install build-essential python-dev libpq-dev

## 7. Install backend's requirements into virtual environment 

        source /opt/production/virtual_envs/beeline-scoreboard/bin/activate
        pip install -r /opt/production/virtual_envs/beeline-scoreboard/requirements.txt

## 8. Prepare frontend application

Instructions [here](frontend_deployment.md)
 
## 9. Create symbolic link to `supervisord` config

        sudo ln -s /opt/production/apps/beeline-scoreboard/production/beeline_scoreboard_supervisord.conf /etc/supervisor/conf.d/beeline_scoreboard_supervisord.conf

## 10. Initialize DB

        cd /opt/production/apps/beeline-scoreboard/production
        PYTHONPATH=$PYTHONPATH:/opt/production/apps/beeline-scoreboard python ./sqlalchemy_initdb.py
        
9. Create symbolic links to Nginx configs

        sudo ln -s /opt/production/apps/beeline-scoreboard/production/beeline_scoreboard_nginx.conf /etc/nginx/sites-enabled/beeline_scoreboard

9. Create symbolic link to Syslog-ng config

        -- sudo ln -s /opt/production/apps/me-advert/production/me-advert_syslog.conf /etc/syslog-ng/conf.d/010me-advert.conf

10. Restart the services

        service syslog-ng restart
        supervisorctl
            >stop all
            >reread
            >start all
        service nginx restart
