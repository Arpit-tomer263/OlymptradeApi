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
