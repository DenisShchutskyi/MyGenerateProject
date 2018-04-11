'''
sudo touch /etc/nginx/sites-available/name_for_nginx
sudo ln -s /etc/nginx/sites-available/name_for_nginx /etc/nginx/sites-enabled/name_for_nginx
sudo nano /etc/nginx/sites-enabled/name_for_nginx

'''

import os
# import sys
# import traceback

TITLE_DIR_FOR_DB = 'init_db'
TITLE_DIR_FOR_DATA = 'public'
TITLE_DOCKER_FILE = 'docker_compose.yml'
TITLE_FILE_FOR_VIEWS = 'views'
TITLE_FILE_FOR_API_IN_VIEWS = 'api.py'
TITLE_FILE_FOR_URL_VIEW_IN_VIEWS = 'url.py'
TITLE_INIT_FILE_FLASK_VIEW = '__init__'
TITLE_INIT_FILE_FLASK_API = '__init__'
TITLE_INIT_FILE_AIOHTTP_API = '__init__'
TITLE_FILE_FOR_INIT_API_FLASK = 'api'

PATH_TO_DIR = os.getcwd()


def ensure_dir(directory):
    try:
        os.stat(directory)
    except FileNotFoundError:
        # traceback.print_exc()
        os.mkdir(directory)


def create_docker_compose(data_for_docker,
                          path_to_dir,
                          title_project_):
    try:
        with open('{}/{}/{}'.format(path_to_dir,
                                    title_project_,
                                    TITLE_DOCKER_FILE), 'w') as docker:
            docker.write("version: '3'\n")
            docker.write("services:")
            for dfd in data_for_docker.keys():
                if dfd == 'postgre':
                    docker.write('\n\tpostrgres:')
                    docker.write('\n\t\timage: postgres')
                    docker.write('\n\t\tenvironment:')
                    docker.write('\n\t\t\t- POSTGRES_PASSWORD={}'.format(data_docker['postgre']['password']))
                    docker.write('\n\t\t\t- POSTGRES_USER={}'.format(data_docker['postgre']['user']))
                    docker.write('\n\t\t\t- POSTGRES_DB={}'.format(data_docker['postgre']['db']))
                    docker.write('\n\t\tports:')
                    docker.write('\n\t\t\t- \'{}:5432\''.format(data_docker['postgre']['port']))
                    docker.write('\n\t\tvolumes:')
                    docker.write('\n\t\t\t- \'./db_data:/var/lib/postgresql/data\'')
                if dfd == 'redis':
                    docker.write('\n\tredis:')
                    docker.write('\n\t\timage: redis')
                    docker.write('\n\t\tports:')
                    docker.write('\n\t\t\t- \'{}:6379\''.format(data_docker['redis']['port']))
                if dfd == 'memcached':
                    docker.write('\n\tmemcached:')
                    docker.write('\n\t\timage: memcached:1.5.6')
                    docker.write('\n\t\tports:')
                    docker.write('\n\t\t\t- \'{}:11211\''.format(data_docker['memcached']['port']))
                if dfd == 'rabbit':
                    docker.write('\n\trabbitmq:')
                    docker.write('\n\t\timage: "rabbitmq:3-management"')
                    docker.write('\n\t\tports:')
                    docker.write('\n\t\t\t- "{}:5672"'.format(data_docker['rabbit']['port']))
                    docker.write('\n\t\t\t- "{}:15672"'.format(data_docker['rabbit']['port']+10000))
                    docker.write('\n\t\tenvironment:')
                    docker.write('\n\t\t\t- RABBITMQ_DEFAULT_PASS={}'.format(data_docker['rabbit']['password']))
                    docker.write('\n\t\t\t- RABBITMQ_DEFAULT_USER={}'.format(data_docker['rabbit']['user']))
                    docker.write('\n\t\thostname: "rabbit_mnesia"')
                    docker.write('\n\t\tvolumes:')
                    docker.write('\n\t\t\t- ~/docker_compose/d/rabbitdb:/var/lib/rabbitmq/mnesia')

    except FileNotFoundError:
        print('к сожалению не вышло создать файл docker-compose')


def create_git_ignore(path_to_dir,
                      title_project_):
    with open('{}/{}/.gitignore'.format(path_to_dir,
                                        title_project_), 'w') as git_ignore:
        data_git_ignore = '''
# Compiled source #
###################
*.com
*.class
*.dll
*.exe
*.o
*.so
*.pyc
.idea

#ignore dir#
############
public/uploads/
public/images/
tests/
manage/

# Packages #
############
# it's better to unpack these files and commit the raw source
# git has its own built in compression methods
*.7z
*.dmg
*.gz
*.iso
*.rar
*.tar
*.zip

/test?.py


# Logs and databases #
######################
*.log
*.sqlite
*.xls
*.xml
cd
# OS generated files #
######################
.DS_Store
ehthumbs.db
Icon
Thumbs.db
.tmtags
.idea
tags
vendor.tags
tmtagsHistory
*.sublime-project
*.sublime-workspace
.bundle
        '''
        git_ignore.write(data_git_ignore)


def create_readme_for_git(path_to_dir,
                          title_project_):
    with open('{}/{}/README.md'.format(path_to_dir,
                                       title_project_), 'w') as read_me:
        read_me.write('# {}  v.1.0 #'.format(title_project_))


def create_api_flask_module(path_to_module_,
                            title_module_,
                            title_project_):
    # создание папки для api
    ensure_dir('{}/{}/api'.format(path_to_module_,
                                  title_module_))
    open('{}/{}/{}.py'.format(path_to_module_,
                              title_module,
                              TITLE_FILE_FOR_INIT_API_FLASK), 'w+')

    # создание __init__
    with open('{}/{}/{}.py'.format(path_to_module_,
                                   title_module_,
                                   TITLE_INIT_FILE_FLASK_API),
              'w+') as init_:
        init_data = '''
from flask import Flask
from flask import render_template
import traceback

app = Flask(__name__)
from {}.{}.views import {}
        '''.format(title_project_,
                   title_module,
                   TITLE_FILE_FOR_INIT_API_FLASK)
        init_.write(init_data)

    # wsgi создание
    with open('{}/wsgi_{}.py'.format(path_to_module_, title_module), 'w+') as wsgi_:
        wsgi__text = '''
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from {}.{}.{} import app
if __name__ == "__main__":
        app.run()
'''.format(title_project,
           title_module_,
           TITLE_INIT_FILE_FLASK_API)
        wsgi_.write(wsgi__text)


def create_api_aiohttp_module(path_to_module_,
                              title_module_,
                              title_project_):
    print('введите порт на котором хотите подымать приложение ')
    port = input()
    try:
        port = int(port)
    except ValueError:
        port = 8080

    # создание файла с роутами
    with open('{}/{}/routes.py'.format(path_to_module_,
                                       title_module_), 'w+') as routes:
        routes_text = '''
routes = [
    # ('HTTP_METHOD', 'URL_API', function_for_api, 'name_route'),
]
'''
        routes.write(routes_text)

    # создание инит файла aiohttp
    with open('{}/{}/{}.py'.format(path_to_module_,
                                   title_module,
                                   TITLE_INIT_FILE_AIOHTTP_API), 'w+') as init_:
        init_text = '''
import asyncio
from aiohttp import web
from {}.{} import routes


async def init_app(loop):
    app = web.Application()
    for route in routes:
        app.router.add_route(route[0],
                             route[1],
                             route[2],
                             name=route[3])

    return app
    
if __name__ == '__main__':
    loop_ = asyncio.get_event_loop()
    app_ = loop_.run_until_complete(init_app(loop_))
    web.run_app(app_, port={})
'''.format(title_project_,
           title_module_,
           port)
        init_.write(init_text)

    # wsgi создание
#     with open('{}/wsgi_{}.py'.format(path_to_module_, title_module), 'w') as wsgi:
#         wsgi_text = '''
# import os
# import sys
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
#
#
# from {}.{}.{} import init_app
# import asyncio
# from aiohttp import web
#
#
# loop = asyncio.get_event_loop()
# app = loop.run_until_complete(init_app(loop))
# web.run_app(app, port=5007)
#
# '''
#         wsgi.write(wsgi_text)


def create_view_flask(path_to_modules_,
                      title_module_,
                      title_project_):
    # пока что только для flask
    print('пока что view только для flask-а')
    # формирование директории для статики модуля
    ensure_dir('{}/{}/static'.format(path_to_modules_,
                                     title_module_))

    # формирование директории для шаблонов модуля
    ensure_dir('{}/{}/templates'.format(path_to_modules_,
                                        title_module_))

    # формирование файла с отображениями
    ensure_dir('{}/{}/views'.format(path_to_modules_,
                                    title_module_))
    open('{}/{}/views/{}.py'.format(path_to_modules_,
                                    title_module_,
                                    TITLE_FILE_FOR_VIEWS), 'w+')

    # формирование файла с отображениями
    ensure_dir('{}/{}/urls'.format(path_to_modules_,
                                   title_module_))
    open('{}/{}/urls/{}'.format(path_to_modules_,
                                title_module_,
                                TITLE_FILE_FOR_API_IN_VIEWS), 'w+')
    open('{}/{}/urls/{}'.format(path_to_modules_,
                                title_module_,
                                TITLE_FILE_FOR_URL_VIEW_IN_VIEWS), 'w+')
    with open('{}/{}/{}.py'.format(path_to_modules_,
                                   title_module_,
                                   TITLE_INIT_FILE_FLASK_VIEW), 'w+') as init:
        ini = '''
from flask import Flask
from flask import render_template
import traceback

app = Flask(__name__)
from {}.{}.views import {}
                '''.format(title_project_,
                           title_module_,
                           TITLE_FILE_FOR_VIEWS)
        init.write(ini)
    with open('{}/wsgi_{}.py'.format(path_to_modules_,
                                     title_module_), 'w+') as wsgi:
        wsgi_text = '''
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from {}.{}.{} import app
if __name__ == "__main__":
    app.run()
                '''.format(title_project_,
                           title_module_,
                           TITLE_INIT_FILE_FLASK_VIEW)
        wsgi.write(wsgi_text)


def create_logger_for_module():
    pass


def create_config_apps(path_to_dir_,
                       title_project_,
                       data_docker_):
    data_docker_for_set = ''
    for dfd in data_docker_.keys():
        if dfd == 'postgre':
            data_docker_for_set += "\n\tuser = '{}'" \
                                   "\n\tdatabase = '{}'" \
                                   "\n\tpassword = '{}'" \
                                   "\n\thost = 'localhost'" \
                                   "\n\tport = '{}'".format(data_docker_['postgre']['user'],
                                                            data_docker_['postgre']['db'],
                                                            data_docker_['postgre']['password'],
                                                            data_docker_['postgre']['port'])
            data_docker_for_set += '''\n\tstr_connect_to_db = "dbname='{}' user='{}' host='{}' password='{}' port='{}'".format(database,
                                                                                         user,
                                                                                         host,
                                                                                         password,
                                                                                         port)'''

        if dfd == 'redis':
            data_docker_for_set += '\n\tredis_port = {}'.format(data_docker_['redis']['port'])
        if dfd == 'memcached':
            data_docker_for_set += '\n\tmemcached_port = {}'.format(data_docker_['memcached']['port'])
        if dfd == 'rabbit':
            data_docker_for_set += '\n\trabbit_mq_port = {}'.format(data_docker_['rabbit']['port'])
            data_docker_for_set += '\n\trabbit_mq_password = \'{}\''.format(data_docker_['rabbit']['password'])
            data_docker_for_set += '\n\trabbit_mq_user = \'{}\''.format(data_docker_['rabbit']['user'])

    text = 'type_work = 1\n' \
           'if type_work == 1:  # local server' \
           '\n\t# for api and web' \
           '\n\tdomain_url = \'/\'' \
           '\n\tdomain_api_admin = \'/\'' \
           '\n\tdomain_api_mobile = \'/\'' \
           '\n\tbase_url = \'http://127.0.0.1:5000\''
    text += data_docker_for_set
    text += '\n\tMEDIA_FOLDER = \'{}/{}\''.format(path_to_dir_,
                                                  title_project_)
    with open('{}/{}/config_app.py'.format(path_to_dir_, title_project_), 'w') as config:
        config.write(text)


def create_nginx_file_for_flask(port_,
                                path_to_modules_,
                                title_module_,
                                title_project_,
                                path_to_dir):
    data_nginx = '''
server {   
    listen '''+port_+''';
    underscores_in_headers on;
    client_body_buffer_size 32K;
    client_max_body_size 300M;

    sendfile on;
    send_timeout 300s;
    keepalive_timeout 7200;
    tcp_nopush on;
    tcp_nodelay on;
    directio 10m;
    server_tokens off;
    gzip             on;
    gzip_min_length  2000;
    gzip_proxied     any;
    gzip_types       text/html application/json, text/xml;

    proxy_read_timeout 60s;
    client_max_body_size 64M;

    charset UTF-8;
    location / {
        proxy_pass http://unix:'''+path_to_modules_+'''/'''+title_module_+'''.sock;
        proxy_set_header Host $host:'''+port_+''';
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-NginX-Proxy true;
    }
    location /'''+'_'.join(title_project_.split())+'''/files{
            alias '''+path_to_dir+'''/'''+title_project_+'''/'''+TITLE_DIR_FOR_DATA+''';
    }
}
'''
    with open('{}/{}.txt'.format(path_to_modules,
                                 title_module_), 'w+') as nginx:
        nginx.write(data_nginx)


data_docker = {}
print("Введите название проекта: ")
title_project = input()

# создание папки проекта
ensure_dir('{}/{}'.format(PATH_TO_DIR,
                          title_project))

# создание папки с сервисами
ensure_dir('{}/{}/{}'.format(PATH_TO_DIR,
                             title_project,
                             title_project))

# создание папки для скриптов db
ensure_dir('{}/{}/{}'.format(PATH_TO_DIR,
                             title_project,
                             TITLE_DIR_FOR_DB))

print('Создавать папку для файлов?(+да иное нет)')
IS_CREATE_DIR_FOR_DATA = True if input() == '+' else False
if IS_CREATE_DIR_FOR_DATA:
    # создание директории для файлов отдачи
    ensure_dir('{}/{}/{}'.format(PATH_TO_DIR,
                                 title_project,
                                 TITLE_DIR_FOR_DATA))


print('В вашем проекте будет необходим docker-compose?(+да иное нет)')
is_create_docker = True if input() == '+' else False
if is_create_docker:
    print('В вашем проекте нужна PostgreSQL')
    is_postgre_sql = True if input() == '+' else False
    if is_postgre_sql:
        print('выберите порт для использования postgresql(5432)')
        port_postgre = input()
        try:
            port_postgre = int(port_postgre)
        except ValueError:
            print('вы ввели не правильное значение поэтому порт бдет задан по умолчанию')
            port_postgre = 5432
        print('введите пароль к базе данных')
        password = input()
        print('введите пользователя под которым хотите войти')
        user = input()
        print('введите название базы даннх')
        db = input()
        data_postgresql = {
            'port': port_postgre,
            'db': db,
            'password': password,
            'user': user,
        }
        data_docker['postgre'] = data_postgresql
    print('В вашем проекте нужен Redis')
    is_redis = True if input() == '+' else False
    if is_redis:
        print('выберите порт для использования redis(6379)')
        port_redis = input()
        try:
            port_redis = int(port_redis)
        except ValueError:
            print('вы ввели не правильное значение поэтому порт бдет задан по умолчанию')
            port_redis = 6379
        data_docker['redis'] = {'port': port_redis}
    print('В вашем проекте нужна Memcached')
    is_memcached = True if input() == '+' else False
    if is_memcached:
        print('выберите порт для использования memcached(11211)')
        port_memcached = input()
        try:
            port_memcached = int(port_memcached)
        except ValueError:
            print('вы ввели не правильное значение поэтому порт бдет задан по умолчанию')
            port_memcached = 11211
        data_docker['memcached'] = {'port': port_memcached}
    print('В вашем проекте нужен RabbitMQ')
    is_rabbit = True if input() == '+' else False
    if is_rabbit:
        print('выберите порт для использования rabbit(5672)')
        port_rabbit = input()
        try:
            port_rabbit = int(port_rabbit)
        except ValueError:
            print('вы ввели не правильное значение поэтому порт бдет задан по умолчанию')
            port_postgre = 5672
        print('введите пароль')
        password = input()
        print('введите пользователя')
        user = input()
        data_rabbit = {
            'port': port_rabbit,
            'password': password,
            'user': user

        }
        data_docker['rabbit'] = data_rabbit

    # создание докера
    create_docker_compose(data_docker,
                          PATH_TO_DIR,
                          title_project)

# создание гит игнора для проекта
create_git_ignore(PATH_TO_DIR,
                  title_project)

# создание README
create_readme_for_git(PATH_TO_DIR,
                      title_project)

path_to_modules = '{}/{}/{}'.format(PATH_TO_DIR,
                                    title_project,
                                    title_project)
print('Давайте приступим к созданию модулей проекта\nдля прекращения ввода на начале итерации введите -')
while True:
    print('введите название модуля')
    title_module = input()
    if title_module == '-':
        print('вы закончили создавать модули')
        break
    title_module = '_'.join(title_module.lower().split())
    # создание директории для модуля
    ensure_dir('{}/{}'.format(path_to_modules,
                              title_module))
    print('этот сервис будет отвечать за отображение или api(+view , api other)')
    is_view = True if input() == '+' else False
    if is_view:
        create_view_flask(path_to_modules,
                          title_module,
                          title_project)
        print('Введите порт для nginx')
        port_for_nginx = input()
        create_nginx_file_for_flask(port_for_nginx,
                                    path_to_modules,
                                    title_module,
                                    title_project,
                                    PATH_TO_DIR)
    else:
        print('выберите framework на котором будет написано API \n\t 1 - flask\n\t2 - aiohttp\n\tпо умочанию flask')
        type_frame = input()
        try:
            type_frame = int(type_frame)
        except ValueError:
            type_frame = 1
        if type_frame == 1:
            # flask
            create_api_flask_module(path_to_modules,
                                    title_module,
                                    title_project)
            print('Введите порт для nginx')
            port_for_nginx = input()
            create_nginx_file_for_flask(port_for_nginx,
                                        path_to_modules,
                                        title_module,
                                        title_project,
                                        PATH_TO_DIR)
        elif type_frame == 2:
            # aiohttp
            create_api_aiohttp_module(path_to_modules,
                                      title_module,
                                      title_project)
        else:
            # flask
            create_api_flask_module(path_to_modules,
                                    title_module,
                                    title_project)
            print('Введите порт для nginx')
            port_for_nginx = input()
            create_nginx_file_for_flask(port_for_nginx,
                                        path_to_modules,
                                        title_module,
                                        title_project,
                                        PATH_TO_DIR)
    print("____________")

create_config_apps(PATH_TO_DIR,
                   title_project,
                   data_docker)

print('вы создали проект\nнастоятельно рекомендуем перепроверить данные')
