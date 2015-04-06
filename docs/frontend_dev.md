# Подготовка dev-окружения frontend

## 1. Инсталляция _node.js_ с использованием _brew_ на Mac OS X

    brew install node

## 2. Инсталляция зависимостей development окружения

    cd bl-scoreboard
    
    npm cache clear
    npm cache clean
    
    npm install
    
    export PATH=`pwd`/node_modules/.bin:$PATH

## 3. Инсталляция runtime-development зависимостей (_angular_, _bootstrap_)

    grunt build-dev

## 4. Подготовка deployment окружения (uglify, less compilation, css minify) в директории _dist_

    grunt build-dist

## 5. Очистка dev и deployment окружений

Очистка `deployment`-окружения
    
    grunt clean-dist

Очистка `devel`-окружения
    
    grunt clean-dev

Не очищает _requirejs_ зависимости в `bl_scoreboard/static/js/main.js`. По необходимости, их нужно очищать вручную.

