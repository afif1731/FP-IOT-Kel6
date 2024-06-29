from src.config.prisma_config import prisma

async def findBoxById(box_id):
    return await prisma.boxes.find_first(
        where= {
            'id': box_id
        }
    )

async def changeBoxPasswd(box_id, new_pass):
    return await prisma.boxes.update(
        where= {
            'id': box_id
        },
        data= {
            'box_psswd': new_pass
        }
    )

async def claimBox(box_id, user_id):
    return await prisma.boxes.update(
        where= {
            'id': box_id
        },
        data= {
            'user_id': user_id
        }
    )

async def adminClaimBox(box_id, admin_id, new_password):
    return await prisma.boxes.update(
        where= {
            'id': box_id
        },
        data= {
            'user_id': admin_id,
            'box_psswd': new_password
        }
    )

async def registerBox(box_id, passwd, admin_id):
    return await prisma.boxes.create({
        'id': box_id,
        'box_psswd': passwd,
        'user_id': admin_id
    })