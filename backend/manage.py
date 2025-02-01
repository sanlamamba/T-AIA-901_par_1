import sys

sys.path.append('./API')
sys.path.append('./model')

import os

from API.app import create_app

config_name = os.getenv('FLASK_CONFIG') or 'default'
app = create_app(config_name)

if __name__ == '__main__':
    app.run()
