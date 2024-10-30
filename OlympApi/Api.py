import asyncio
import websockets
import json
import time
import random
import string

VALID_PAIRS = [
    # Commodities
    'ASIA_X', 'EUROPE_X', 'MOONCH_X', 'CRYPTO_X', 'MHJNTR_X', 'ASTRO_X',
    # Currency pairs
    'AUDCAD', 'AUDCHF', 'AUDJPY', 'AUDNZD', 'AUDUSD', 'CADCHF', 'CADJPY', 'CHFJPY',
    'EURAUD', 'EURCAD', 'EURCHF', 'EURGBP', 'EURJPY', 'EURNZD', 'USDJPY_OTC', 'GBPCAD', 'GBPAUD',
    'GBPCHF', 'GBPJPY', 'GBPNZD', 'GBPUSD', 'NZDCAD', 'NZDCHF', 'NZDJPY', 'NZDUSD', 'USDCAD', 'USDJPY',
    'USDNOK', 'USDMXN', 'USDTRY', 'USDSGD',
    # OTC pairs
    "AUDCAD_OTC", "AUDCHF_OTC", "AUDJPY_OTC", "AUDNZD_OTC", "AUDUSD_OTC", "CADCHF_OTC", "CADJPY_OTC",
    "CHFJPY_OTC", "EURCAD_OTC", "EURCHF_OTC", "EURGBP_OTC", "EURNZD_OTC", "USDJPY_OTC_OTC", "GBPAUD_OTC",
    "GBPUSD_OTC", "GBPCHF_OTC", "GBPNZD_OTC", "GBPJPY_OTC", "GBPCAD_OTC", "GBPAUD_OTC", "NZDUSD_OTC",
    "NZDCHF_OTC", "NZDJPY_OTC", "NZDCAD_OTC", "USDCHF_OTC", "USDJPY_OTC", "USDCAD_OTC", "Silver_OTC", "Gold_OTC"
]

periods = [
    5, 10, 15, 20, 30, 60, 120, 300, 600, 900, 1800, 3600
]


class Olymptradeapi():
    def __init__(self, cokkie, uri, check):
        self.check = check
        self.cokkie = cokkie
        self.uri = uri
        self.header = {
            "Host": "ws.olymptrade.com",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0",
            "Accept": "*/*",
            "Accept-Language": "en-GB,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Sec-WebSocket-Version": "13",
            "Origin": "https://olymptrade.com",
            "Sec-WebSocket-Extensions": "permessage-deflate",
            "Sec-WebSocket-Key": "EnGc0vP7q+Mw4m9VVjuuSg==",
            "Connection": "keep-alive, Upgrade",
            "Cookie": self.cokkie,
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "websocket",
            "Sec-Fetch-Site": "same-site",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache",
            "Upgrade": "websocket"
        }
        self.websocket = None
        self.account_id_real = None
        self.account_id_demo = None

    async def connect(self):
        if self.websocket is None or self.websocket.closed:
            self.websocket = await websockets.connect(self.uri, extra_headers=self.header)

    async def close(self):
        if self.websocket is not None:
            await self.websocket.close()

    async def get_current_time_utc(self):
        """Get the current time in UTC as a Unix timestamp."""
        return int(time.time())

    def get_milliseconds(self):
        current_utc_time_millis = int(time.time() * 1000)
        return current_utc_time_millis

    async def get_candles(self, pair, timeframe):
        if self.websocket is None or self.websocket.closed:
            print("WebSocket is closed. Connect the client first.")
            return None  # Exit the function if websocket is closed

        await self.connect()  # Ensure connection is established
        current_time = await self.get_current_time_utc()
        message_to_send = None
        if pair in VALID_PAIRS and timeframe in periods:
            message_to_send = [{
                "t": 2,
                "e": 10,
                "uuid": "Y-XsI3",
                "d": [{
                    "pair": pair,
                    "size": timeframe,
                    "to": current_time,
                    "solid": True
                }]
            }]
        else:
            print("Wrong credentials; please enter valid arguments or check the GitHub README.")

        if message_to_send and self.websocket:
            await self.websocket.send(json.dumps(message_to_send))
        else:
            print("Please connect the client first.")

        try:
            if self.websocket is None or self.websocket.closed:
                print("WebSocket is closed. Cannot receive data.")
                return None  # Exit if websocket is closed
            response = await self.websocket.recv()
            return response
        except websockets.exceptions.ConnectionClosed:
            print("Connection closed")
            return None

    async def trade(self, dir, amount, period, asset, account_type):
        current_time = self.get_milliseconds()
        account_type = account_type.lower()
        trade_message = None
        if account_type == 'demo':
            trade_message = [{
                "t": 2,
                "e": 23,
                "uuid": "M1W6DOIUEZ2KZ5Z4GJD",  # Ensure this UUID is valid
                "d": [{
                    "amount": amount,
                    "dir": dir,
                    "pair": asset,
                    "cat": "digital",
                    "pos": 0,
                    "source": "platform",
                    "account_id": self.account_id_demo,
                    "group": "demo",
                    "timestamp": current_time,
                    "risk_free_id": None,  # Should be `None`, not 'null'
                    "is_flex": False,
                    "duration": period
                }]
            }]
        elif account_type == 'real':
            trade_message = [{
                "t": 2,
                "e": 23,
                "uuid": "M1W6DOIUEZ2KZ5Z4GJD",  # Ensure this UUID is valid
                "d": [{
                    "amount": amount,
                    "dir": dir,
                    "pair": asset,
                    "cat": "digital",
                    "pos": 0,
                    "source": "platform",
                    "account_id": self.account_id_real,
                    "group": "demo",
                    "timestamp": current_time,
                    "risk_free_id": None,  # Should be `None`, not 'null'
                    "is_flex": False,
                    "duration": period
                }]
            }]
        if trade_message and self.websocket:
            await self.websocket.send(json.dumps(trade_message))
        else:
            print("Unable to place trade; may be due to wrong credentials or the client is not connected. Connect it first.")

        try:
            if self.websocket is None or self.websocket.closed:
                print("WebSocket is closed. Cannot receive trade response.")
                return None  # Exit if websocket is closed
            response = await self.websocket.recv()
            return response
        except websockets.exceptions.ConnectionClosed:
            print("Connection closed")
            return None

    async def get_profitability(self, pair):
        if pair in VALID_PAIRS:
            message = [{"t": 2, "e": 182, "uuid": "r4JDEg", "d": [{"account_id": self.account_id_demo}]}]
            if self.websocket:
                await self.websocket.send(json.dumps(message))
            else:
                print("WebSocket is not connected.")
            try:
                if self.websocket is None or self.websocket.closed:
                    print("WebSocket is closed. Cannot receive profitability data.")
                    return None  # Exit if websocket is closed
                response = await self.websocket.recv()

                if response:
                    parsed_response = json.loads(response)
                    for entry in parsed_response:
                        # Ensure that 'd' exists and is iterable
                        if 'd' in entry and isinstance(entry['d'], list):
                            for payout_data in entry['d']:
                                # Check if the pair matches the specified pair
                                if 'pair' in payout_data and payout_data['pair'] == pair:
                                    # Print only the 'profitability' field
                                    if 'profitability' in payout_data:
                                        return f"Payout of {pair}: {payout_data['profitability']}"

                else:
                    print("No response found.")
            except websockets.exceptions.ConnectionClosed:
                print("Connection closed while receiving profitability data.")
                return None

    def generateUuid(self):
        return ''.join([random.choice(string.ascii_uppercase + string.digits) for n in range(18)])

    async def get_balance(self,type):
        message = [{"t": 2, "e": 98, "uuid": "r4JDEg", "d": [54]}]
        if self.websocket:
            await self.websocket.send(json.dumps(message))
        
        else:
            print("Websocket is not connected.")
        
        response = await self.websocket.recv()
        
        # Parse the JSON response
        response_data = json.loads(response)
        
         # Initialize variables for prices
        real_price = None
        demo_price = None

        # Extract account IDs and amounts from the first item in the response
        if len(response_data) > 0 and "d" in response_data[0]:
            for account in response_data[0]["d"]:
                # Ensure the account entry is a dictionary
                if isinstance(account, dict):
                    # Check for real account
                    if account.get("group") == "real":
                        self.account_id_real = account["account_id"]
                        real_price = account["amount"]  # Capture the real price
                    # Check for demo account
                    elif account.get("group") == "demo":
                        self.account_id_demo = account["account_id"]
                        demo_price = account["amount"]  # Capture the demo price

        if type.lower() == 'demo':
            return demo_price

        elif type.lower() == 'real':
            return real_price