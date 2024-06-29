from src.config.prisma_config import prisma

async def findAccountByEmail(email):
    return await prisma.accounts.find_first(
        where= {
            'email': {
                'contains': email   
            }
        }
    )

async def findAccountById(acc_id):
    return await prisma.accounts.find_first(
        where={
            'id': acc_id
        }
    )

async def registerAccount(name, email, hashed_pass):
    return await prisma.accounts.create({
        'name': name,
        'email': email,
        'password': hashed_pass
    })

async def getMe(acc_id):
    return await prisma.accounts.find_first(
        where= {
            'id': acc_id
        },
        include= {
            'boxes': True
        }
    )