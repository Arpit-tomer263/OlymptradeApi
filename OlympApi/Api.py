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
       """Haha Not get entire api too easily contact me on telegram i'll send you id-:@Arpit_tomer263"""
