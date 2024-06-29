import src.service.box_service as BoxService

from quart import Blueprint, request, jsonify
from src.validator.box_validator import changePasswdValidation, registerBoxValidation, claimBoxValidation, loginBoxValidation
from src.middleware.custom_error import CustomError
from src.middleware.custom_response import CustomResponse
from src.middleware.validator import do_validate

box_bp = Blueprint('secretbox', __name__)

@box_bp.route('/<box_id>/change-password', methods=['POST'])
async def changeBoxPasswdController(box_id):
    try:
        req = await request.get_json()
        data = do_validate(changePasswdValidation, req)

        auth_headers = request.headers.get('Authorization')
        if not auth_headers:
            raise CustomError(403, "unauthorized")
        
        token = auth_headers.split(" ")[1]

        result = await BoxService.changePassword(box_id, data['old_pass'], data['new_pass'], token)

        response = CustomResponse(200, 'berhasil ganti password', {})
        return jsonify(response.JSON()), response.code
    except CustomError as err:
        return jsonify(err.JSON()), err.code

@box_bp.route('/<box_id>/claim', methods=['POST'])
async def claimBoxController(box_id):
    try:
        req = await request.get_json()
        data = do_validate(claimBoxValidation, req)

        auth_headers = request.headers.get('Authorization')
        if not auth_headers:
            raise CustomError(403, "unauthorized")
        
        token = auth_headers.split(" ")[1]

        result = await BoxService.claimBox(box_id, data['password'], token)

        response = CustomResponse(200, 'box claimed', result)
        return jsonify(response.JSON()), response.code
    except CustomError as err:
        return jsonify(err.JSON()), err.code

@box_bp.route('/<box_id>/register', methods=['POST'])
async def registerBoxController(box_id):
    try:
        req = await request.get_json()
        data = do_validate(registerBoxValidation, req)

        auth_headers = request.headers.get('Authorization')
        if not auth_headers:
            raise CustomError(403, "unauthorized")
        
        token = auth_headers.split(" ")[1]

        result = await BoxService.registerBox(data['id'], data['password'], token)

        response = CustomResponse(200, 'box registered', result)
        return jsonify(response.JSON()), response.code
    except CustomError as err:
        return jsonify(err.JSON()), err.code

@box_bp.route('/<box_id>/login', methods=['POST'])
async def loginBoxController(box_id):
    try:
        req = await request.get_json()
        data = do_validate(loginBoxValidation, req)

        auth_headers = request.headers.get('Authorization')
        if not auth_headers:
            raise CustomError(403, "unauthorized")
        
        token = auth_headers.split(" ")[1]

        result = await BoxService.loginBox(data['id'], data['password'], token)

        response = CustomResponse(200, 'sukses login', result)
        return jsonify(response.JSON()), response.code
    except CustomError as err:
        return jsonify(err.JSON()), err.code

