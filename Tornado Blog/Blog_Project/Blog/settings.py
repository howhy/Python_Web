#-*- coding:utf-8 -*-
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.append(BASE_DIR)
# from common import uimethods,uimodules
setting=dict(
            template_path=os.path.join(BASE_DIR,'templates'),
            static_path=os.path.join(BASE_DIR,'static'),
            login_url='/login',
            cookie_secret="234sdfwer534sdf234gyuy5u567werw",
            xsrf_cookies=True,
            # ui_modules=uimodules,
            # ui_methods=uimethods,
            pycket={
                'engine': 'redis',
                'storage': {
                'host': '127.0.0.1',
                'port': 6379,
                'db_sessions': 1,
                'db_notifications': 11,
                'max_connections': 2 ** 31,
                },
                'cookies': {
                    'expires_days': 30,
                    'max_age': 600,
                },
            },
        )
DATABASES = {
    'default': {
            'ENGINE': 'mysql+pymysql',
            'NAME':'blog',
            'USER': 'blog',
            'PASSWORD': '123@howhy',
            'HOST': '127.0.0.1',
            'PORT': '3306',
    }
}

