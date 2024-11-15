import asyncio
import csv
import os

from data.config import CHECK_PROXY, USE_PROXY, hello
from utils.agent import Agent
from utils.core import create_sessions
from utils.telegram import Accounts


async def main():
    print(hello)
    # action = int(input('Выберите действие:\n1. Начать сбор монет\n2. Создать сессию\n3. Сохранить авторизации\n4. Использовать сохраненные авторизации\n5. Собрать статистику\n\n>'))
    
    action = 1
    if not os.path.exists('sessions'):
        os.mkdir('sessions')
    
    if not os.path.exists('authorization.txt'):
        with open('authorization.txt', 'w') as file:
            pass
        
    
    if action == 2:
        await create_sessions()

    if action == 1:
        accounts = await Accounts().get_accounts()
                
        tasks = []
        if USE_PROXY:
            proxy_dict = {}
            with open('proxy.txt','r',encoding='utf-8') as file:
                proxy = [i.strip().split() for i in file.readlines() if len(i.strip().split()) == 2]
                for prox,name in proxy:
                    proxy_dict[name] = prox
            for thread, account in enumerate(accounts):
                if account in proxy_dict:
                    tasks.append(asyncio.create_task(Agent(account=account, thread=thread, proxy=proxy_dict[account]).main()))
                else:
                    tasks.append(asyncio.create_task(Agent(account=account, thread=thread,proxy = None).main()))
        else:
            for thread, account in enumerate(accounts):
                tasks.append(asyncio.create_task(Agent(account=account, thread=thread,proxy = None).main()))
        await asyncio.gather(*tasks)
    
    if action == 3:
        accounts = await Accounts().get_accounts()
                
        tasks = []
        if USE_PROXY:
            proxy_dict = {}
            with open('proxy.txt','r',encoding='utf-8') as file:
                list = [i.strip().split() for i in file.readlines()]
                proxy = []
                for info in list:
                    if info!=[]:
                        proxy.append((info[0],''.join(info[1:]).replace('.session','')))
                for prox,name in proxy:
                    proxy_dict[name] = prox
            for thread, account in enumerate(accounts):
                if account in proxy_dict:
                    tasks.append(asyncio.create_task(Agent(account=account, thread=thread, proxy=proxy_dict[account]).save_authorization()))
                else:
                    tasks.append(asyncio.create_task(Agent(account=account, thread=thread,proxy = None).save_authorization()))
        else:
            for thread, account in enumerate(accounts):
                tasks.append(asyncio.create_task(Agent(account=account, thread=thread,proxy = None).save_authorization()))
        await asyncio.gather(*tasks)
    
    if action == 4:
                
        tasks = []
        if USE_PROXY:
            proxy_dict = {}
            with open('proxy.txt','r',encoding='utf-8') as file:
                proxy = [i.strip().split() for i in file.readlines() if len(i.strip().split()) == 2]
                for prox,name in proxy:
                    proxy_dict[name] = prox
                    
            with open('authorization.txt','r') as file:
                accounts = [i.split()[0] for i in file.readlines()]
                    
            for thread, account in enumerate(accounts):
                if account in proxy_dict:
                    tasks.append(asyncio.create_task(Agent(account=account, thread=thread, proxy=proxy_dict[account],authozire=True).main()))
                else:
                    if CHECK_PROXY:
                        continue
                    tasks.append(asyncio.create_task(Agent(account=account, thread=thread,proxy = None,authozire=True).main()))
        else:
            for thread, account in enumerate(accounts):
                tasks.append(asyncio.create_task(Agent(account=account, thread=thread,proxy = None,authozire=True).main()))
        await asyncio.gather(*tasks)
    if action == 5:
        accounts = await Accounts().get_accounts()
                
        tasks = []
        if USE_PROXY:
            proxy_dict = {}
            with open('proxy.txt','r',encoding='utf-8') as file:
                list = [i.strip().split() for i in file.readlines()]
                proxy = []
                for info in list:
                    if info!=[]:
                        proxy.append((info[0],''.join(info[1:]).replace('.session','')))
                for prox,name in proxy:
                    proxy_dict[name] = prox
            for thread, account in enumerate(accounts):
                if account in proxy_dict:
                    tasks.append(asyncio.create_task(Agent(account=account, thread=thread, proxy=proxy_dict[account]).stats()))
                else:
                    tasks.append(asyncio.create_task(Agent(account=account, thread=thread,proxy = None).stats()))
        else:
            for thread, account in enumerate(accounts):
                tasks.append(asyncio.create_task(Agent(account=account, thread=thread,proxy = None).stats()))
        results = await asyncio.gather(*tasks)
        
        with open('stats.csv', 'w', newline='') as csvfile:
            fieldnames = ['session','balance', 'tickets', 'toncoin','notcoin']
        
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
        
            for row in results:
                if row!=None:
                    writer.writerow(row)
if __name__ == '__main__':
    asyncio.run(main())
