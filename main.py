
from src.client import Client
import asyncio
import random
from aiomultiprocess import Pool
import time
from asyncio.exceptions import TimeoutError
from colorama import Fore, init
import requests
import json
init()
PU = []

def data_base():
    with open('config.json', 'r', encoding='utf-8') as config:
        data = json.load(config)
        return data

with open('username.txt', 'r', encoding='utf-8', errors='ignore') as f:
    x =1
    for line in f:
        PU.append(f'{x}:{line.strip()}')
        x +=1
        
        
async def main(u):
        try:
            username = u.split(':')[1]
            count = u.split(':')[0]
            client = Client(username,c = count,use_proxy=True)
            await client.get_proxy()
            res = await client.login()
            await client.close()
        except Exception as e:
            print(e)
            pass

async def x():
        count =1
        thread = data_base()['THREAD']
        n = thread
        final = [PU[i * n:(i + 1) * n] for i in range((len(PU) + n - 1) // n )]
        for x in final:

            count+=1
            async with Pool() as pool:
                async for result in pool.map(main,x):
                    continue 


if __name__ == '__main__':
    try:
        asyncio.run(x())
    except Exception as e:
        print(e)
    except:
        pass
# https://www.myexternalip.com/raw
