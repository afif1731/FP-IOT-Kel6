import src.service.auth_service as AuthService

from quart import Blueprint, request, make_response, jsonify
from src.validator.auth_validator import registerValidation, loginValidation
from src.middleware.custom_error import CustomError
from src.middleware.custom_response import CustomResponse
from src.middleware.validator import do_validate

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
async def RegisterController():
    try:
        req = await request.get_json()
        data = do_validate(registerValidation, req)

        result = await AuthService.register(data['name'], data['email'], data['password'])

        response = CustomResponse(201, 'register sukses', {'token': result})
        return jsonify(response.JSON()), response.code
    except CustomError as err:
        return jsonify(err.JSON()),err.code

@auth_bp.route('/login', methods=['POST'])
async def LoginController():
    try:
        req = await request.get_json()
        data = do_validate(loginValidation, req)

        result = await AuthService.login(data['email'], data['password'])

        response = CustomResponse(200, 'login sukses', {'token': result})
        return jsonify(response.JSON()), response.code
    except CustomError as err:
        return jsonify(err.JSON()),err.code

@auth_bp.route('/me', methods=['GET'])
async def MeController():
    try:
        auth_headers = request.headers.get('Authorization')
        if not auth_headers:
            raise CustomError(403, "unauthorized")
        
        token = auth_headers.split(" ")[1]

        result = await AuthService.me(token)

        response = CustomResponse(200, 'get me', result)
        return jsonify(response.JSON()), response.code
    except CustomError as err:
        return jsonify(err.JSON()),err.code