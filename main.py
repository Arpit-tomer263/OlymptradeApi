from OlympApi.Api import Olymptradeapi
from OlympApi.cookies import fetch_cookies_uri
import asyncio

#-----------------------------------------------------------------#
# BEFORE USING THIS MAKE SURE YOU ARE LOGGED INTO OLYMPTRADE IN   #
# FIREFOX OTHERWISE IT WILL NOT WORK.                             #
#-----------------------------------------------------------------#


cookie, uri, check = fetch_cookies_uri()
client = Olymptradeapi(cokkie=cookie, uri=uri, check=check)

async def get_candle(pair, timeframe):
    Candle = await client.get_candles(pair, timeframe)  # Make sure timeframe is in seconds
    print(Candle)

async def trade(pair, dir, amount, period,type):
    trade = await client.trade(dir, amount, period, pair,type)
    # dir = "up"/"down", amount = 1, period = "60", pair = "EURGBP" period should be in seconds
    if trade:
        print("Trade placed.",trade)

async def get_profitability(pair):  # Period should be in seconds
    profitability = await client.get_profitability(pair)
    print(profitability)

async def check_balance(type):#demo or real
    balance = await client.get_balance(type)
    print(f"{type} Balance is: {balance}") 

async def main():
    await client.connect()
    await check_balance('demo') 
    # await get_candle("EURGBP", 60)                                
    # await trade("EURGBP", "up", 1, 60,'demo')
    # await get_profitability("EURGBP")
    await client.close()



# Correctly call the main coroutine
asyncio.run(main())


"""So the code's end Here Now some rules to use this code

Rule 1-: Login on you're firefox first with any id not matter if you're not login this will not work and yes make sure firefox is completely closed..

Rule 2-: When you start this code first call check_balance function becuase it fetch the important criterias for code work if you're using it to make bot's then only call it one time on you're code.

Rule 3 -: Firstly connect this client using await client.connect()

"""

