from src.config.prisma_config import prisma
from src.utils.hashing import hash_pass
import asyncio
import csv

async def users():
    with open('./prisma/seeder_data/accounts.csv', mode='r') as infile:
        reader = csv.DictReader(infile)
        mydict = [row for row in reader]
        for user in mydict:
            user_pass = await hash_pass(user['password'])

            await prisma.accounts.upsert(
                where={'id': user['id']},
                data={
                    'create': {
                        'id': user['id'],
                        'email': user['email'],
                        'name': user['name'],
                        'password': user_pass.decode('utf-8'),
                        'role': user['role'],
                    },
                    'update': {
                        'email': user['email'],
                        'name': user['name'],
                        'password': user_pass.decode('utf-8'),
                        'role': user['role'],
                    }
                }
            )

async def boxes():
    with open('./prisma/seeder_data/boxes.csv', mode='r') as infile:
        reader = csv.DictReader(infile)
        mydict = [row for row in reader]
        for box in mydict:
            box_pass = await hash_pass(box['password'])

            await prisma.boxes.upsert(
                where={'id': box['id']},
                data={
                    'create': {
                        'id': box['id'],
                        'box_psswd': box_pass.decode('utf-8'),
                        'user_id' : box['user_id']
                    },
                    'update': {
                        'box_psswd': box_pass.decode('utf-8'),
                        'user_id' : box['user_id']
                    }
                }
            )

async def main():
    await prisma.connect()
    await users()
    await boxes()
    await prisma.disconnect()

if __name__ == '__main__':
    asyncio.run(main())