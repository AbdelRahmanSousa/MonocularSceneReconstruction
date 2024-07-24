import sys
import os
from src.GLOBAL import GLOBAL
sys.path.append(os.path.join(GLOBAL.instant_ngp, 'build'))
from flask import Flask
from views import *


app = Flask(__name__, static_url_path='', static_folder='./src/static', template_folder='./src/templates')
app.register_blueprint(core_bp)

if __name__ == '__main__':
    app.run(debug=True, host=GLOBAL.host, port=GLOBAL.port)

