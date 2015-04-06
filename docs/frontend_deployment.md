# Deployment of frontendc 

Assume that running user is _olegvg_.

## 1. Install _node.js_ 

Mac OS X, _brew_

    brew install node
    
Debian Wheezy

    sudo echo '# backports' >> /etc/apt/sources.list
    sudo echo 'deb http://_mirror_/debian wheezy-backports main' >> /etc/apt/sources.list
    sudo echo 'deb-src http://_mirror_/debian wheezy-backports main' >> /etc/apt/sources.list
    sudo apt-get update
    sudo apt-get install nodejs
    sudo apt-get install nodejs-legacy
    curl https://www.npmjs.org/install.sh | sudo sh
    sudo setfacl -R -m u:olegvg:rwx /usr/lib/node_modules/

## 2. Install development _node.js_ dependencies

    cd /opt/production/apps/beeline-scoreboard
    
    npm cache clear
    npm cache clean
    
    npm install
    
    export PATH=`pwd`/node_modules/.bin:$PATH

## 3. Install development environment of frontend application (_angular_, _bootstrap_, etc.)

    grunt build-dev

## 4. Build production bundle 

Take development environment and frontend application sources, then do uglify, .less compilation, .css minify 
Result is in dir /opt/production/apps/beeline-scoreboard/bl_scoreboard/dist

    grunt build-dist


