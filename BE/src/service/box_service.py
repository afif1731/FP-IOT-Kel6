import src.repository.box_repository as BoxRepository
import src.repository.auth_repository as AuthRepository

from src.middleware.custom_error import CustomError
from src.utils import hashing, jwt_utils

async def registerBox(box_id, password, token):
    data_decode = jwt_utils.jwt_verify(token)

    if data_decode is None:
        raise CustomError(403, 'invalid token')
    
    user_role = data_decode['data']['role']
    user_id = data_decode['data']['user_id']

    if user_role != 'ADMIN':
        raise CustomError(403, 'you cant do this')
    
    box = await BoxRepository.findBoxById(box_id)

    if box is not None:
        raise CustomError(400, 'id already registered')
    
    hashedpass = await hashing.hash_pass(str(password))

    new_box = await BoxRepository.registerBox(box_id, hashedpass.decode('utf-8'), user_id)

    if new_box is None:
        raise CustomError(500, 'failed to register box')
    
    return {
        'box_id': new_box.id
    }

async def changePassword(box_id, old_pass, new_pass, token):
    data_decode = jwt_utils.jwt_verify(token)

    if data_decode is None:
        raise CustomError(403, 'invalid token')
    
    user_id = data_decode['data']['user_id']
    
    box = await BoxRepository.findBoxById(box_id)

    if box is None:
        raise CustomError(400, 'invalid box id')

    if box.user_id != user_id:
        raise CustomError(403, 'you have no access to this box')
    
    isPasswdTrue = await hashing.compare(old_pass, box.box_psswd)

    if not isPasswdTrue:
        raise CustomError(403, 'invalid cred')
    
    hashedpass = await hashing.hash_pass(str(new_pass))
    
    new_box = await BoxRepository.changeBoxPasswd(box_id, hashedpass.decode('utf-8'))

    if new_box is None:
        raise CustomError(500, 'failed to update password')
    
    return True
    
async def claimBox(box_id, password, token):
    data_decode = jwt_utils.jwt_verify(token)

    if data_decode is None:
        raise CustomError(403, 'invalid token')
    
    user_id = data_decode['data']['user_id']
    
    box = await BoxRepository.findBoxById(box_id)

    if box is None:
        raise CustomError(400, 'invalid box id')

    if box.user_id == user_id:
        raise CustomError(400, 'you already claimed this box')
    
    isUserAdmin = await AuthRepository.findAccountById(user_id)
    if isUserAdmin is None:
        raise CustomError(404, 'invalid user')
    
    isBoxAdmin = await AuthRepository.findAccountById(box.user_id)

    if isBoxAdmin.role != 'ADMIN' and isUserAdmin.role != 'ADMIN':
        raise CustomError(403, 'this box is already claimed')
    elif isBoxAdmin.role != 'ADMIN' and isUserAdmin.role == 'ADMIN':
        hashedpass = await hashing.hash_pass(str(password))
        new_box = await BoxRepository.adminClaimBox(box_id, user_id, hashedpass.decode('utf-8'))

        if new_box is None:
            raise CustomError(500, 'failed to claim box')
        
        return {
            'id': new_box.id,
            'user_id': new_box.user_id
        }
    
    isPasswdTrue = await hashing.compare(password, box.box_psswd)

    if not isPasswdTrue:
        raise CustomError(403, 'invalid cred')
    
    new_box = await BoxRepository.claimBox(box_id, user_id)

    if new_box is None:
        raise CustomError(500, 'failed to claim box')
    
    return {
        'id': new_box.id,
        'user_id': new_box.user_id
    }

async def loginBox(box_id, password):
    box = await BoxRepository.findBoxById(box_id)

    if box is None:
        raise CustomError(400, 'invalid box id')

    isPasswdTrue = await hashing.compare(password, box.box_psswd)

    if not isPasswdTrue:
        raise CustomError(403, 'invalid cred')
    
    return True