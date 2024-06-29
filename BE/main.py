from quart import Quart, jsonify
from quart_cors import cors
from src.config.prisma_config import prisma
from src.controller.auth.routes import auth_bp
from src.controller.secretbox.routes import box_bp
from src.middleware.custom_error import CustomError
from dotenv import load_dotenv

import os

load_dotenv()

PORT = os.getenv('PORT')

app = Quart(__name__)
app = cors(app, allow_origin="*")

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(box_bp, url_prefix='/secretbox')

@app.before_serving
async def startup():
    await prisma.connect()

@app.after_serving
async def shutdown():
    await prisma.disconnect()

@app.errorhandler(CustomError)
async def handle_custom_error(error):
    response = jsonify(error.JSON())
    response.status_code = error.code
    return response

@app.route('/')
def home():
    return 'runnin wild...'

if __name__ == '__main__':
    app.run(port=PORT)