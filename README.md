# OlymptradeApi
This is the OlymptradeApi which have many options Check balance,Trade,Candles sticks data,payout For easy to interact with olymptrade



## Code Example

```python
from OlympApi.Api import Olymptradeapi
from OlympApi.cookies import fetch_cookies_uri

async def main():
    cookie, uri, check = fetch_cookies_uri()
    client = Olymptradeapi(cookie=cookie, uri=uri, check=check)
    await client.connect()
    balance = await client.get_balance('demo')
    print(f"Demo Balance is: {balance}")


```
## Rules

Rule 1-: Login on you're firefox first with any id not matter if you're not login this will not work and yes make sure firefox is completely closed..

Rule 2-: When you start this code first call check_balance function becuase it fetch the important criterias for code work if you're using it to make bot's then only call it one time on you're code.

Rule 3 -: Firstly connect this client using await client.connect()

For Getting this Contact me on telegram-:https://t.me/Arpit_tomer263
Telegram id-: @Arpit_tomer263
