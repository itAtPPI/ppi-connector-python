from ppi_client.api.constants import ACCOUNTDATA_TYPE_ACCOUNT_NOTIFICATION, ACCOUNTDATA_TYPE_PUSH_NOTIFICATION, \
    ACCOUNTDATA_TYPE_ORDER_NOTIFICATION
from ppi_client.models.account_movements import AccountMovements
from ppi_client.models.bank_account_request import BankAccountRequest
from ppi_client.models.foreign_bank_account_request import ForeignBankAccountRequest, ForeignBankAccountRequestDTO
from ppi_client.models.cancel_bank_account_request import CancelBankAccountRequest
from ppi_client.models.order import Order
from ppi_client.ppi import PPI
from ppi_client.models.order_budget import OrderBudget
from ppi_client.models.order_confirm import OrderConfirm
from ppi_client.models.disclaimer import Disclaimer
from ppi_client.models.investing_profile import InvestingProfile
from ppi_client.models.investing_profile_answer import InvestingProfileAnswer
from ppi_client.models.instrument import Instrument
from datetime import datetime, timedelta
import asyncio
import json
import traceback
import os

# Change sandbox variable to True to connect to sandbox environment
ppi = PPI(sandbox=False)


def main():
    try:
        # Change login credential to connect to the API
        ppi.account.login_api('<API Key>', '<API Secret>')

        # Realtime subscription to market data
        def onconnect_marketdata():
            try:
                print("\nConnected to realtime market data")
                ppi.realtime.subscribe_to_element(Instrument("GGAL", "ACCIONES", "A-48HS"))
            except Exception as error:
                traceback.print_exc()

        def ondisconnect_marketdata():
            try:
                print("\nDisconnected from realtime market data")
            except Exception as error:
                traceback.print_exc()

        # Realtime MarketData
        def onmarketdata(data):
            try:
                msg = json.loads(data)
                if msg["Trade"]:
                    print("%s [%s-%s] Price %.2f Volume %.2f" % (
                        msg['Date'], msg['Ticker'], msg['Settlement'], msg['Price'], msg['VolumeAmount']))
                else:
                    if len(msg['Bids']) > 0:
                        bid = msg['Bids'][0]['Price']
                    else:
                        bid = 0

                    if len(msg['Offers']) > 0:
                        offer = msg['Offers'][0]['Price']
                    else:
                        offer = 0

                    print(
                        "%s [%s-%s] Offers: %.2f-%.2f Opening: %.2f MaxDay: %.2f MinDay: %.2f Accumulated Volume %.2f" %
                        (
                            msg['Date'], msg['Ticker'], msg['Settlement'], bid, offer,
                            msg['OpeningPrice'], msg['MaxDay'], msg['MinDay'], msg['VolumeTotalAmount']))
            except Exception as error:
                print(datetime.now())
                traceback.print_exc()
                
        ppi.realtime.connect_to_market_data(onconnect_marketdata, ondisconnect_marketdata, onmarketdata)

        # Starts connections to real time: for example to account or market data
        ppi.realtime.start_connections()

    except Exception as message:
        print(message)


if __name__ == '__main__':
    main()
