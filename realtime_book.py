from ppi_client.models.account_movements import AccountMovements
from ppi_client.ppi import PPI
from ppi_client.models.orders_filter import OrdersFilter
from ppi_client.models.order_budget import OrderBudget
from ppi_client.models.order_confirm import OrderConfirm
from ppi_client.models.disclaimer import Disclaimer
from ppi_client.models.search_instrument import SearchInstrument
from ppi_client.models.search_marketdata import SearchMarketData
from ppi_client.models.search_datemarketdata import SearchDateMarketData
from ppi_client.models.order import Order
from ppi_client.models.instrument import Instrument
from datetime import datetime, timedelta
import asyncio
import json
import traceback

# Change sandbox variable to True to connect to sandbox environment
ppi = PPI(sandbox=False)


def main():
    try:
        # Change login credential to connect to the API
        ppi.account.login('<user key>', '<user secret>')

        # Realtime subscription to market data
        def onconnect():
            try:
                print("\nConnected to realtime")
                ppi.realtime.subscribe_to_element(Instrument("GGAL", "ACCIONES", "A-48HS"))
            except Exception as error:
                traceback.print_exc()

        def ondisconnect():
            try:
                print("\nDisconnected from realtime")
            except Exception as error:
                traceback.print_exc()

        # Realtime broadcast market data
        def onmarketdata(data):
            try:
                msg = json.loads(data)
                if msg["Trade"] == False:
                    if len(msg['Bids']) > 0:
                        bid_price = msg['Bids'][0]['Price']
                        bid_amount = msg['Bids'][0]['Quantity']
                    else:
                        bid_price = 0
                        bid_amount = 0

                    if len(msg['Offers']) > 0:
                        offer_price = msg['Offers'][0]['Price']
                        offer_amount = msg['Offers'][0]['Quantity']
                    else:
                        offer_price = 0
                        offer_amount = 0

                    print(
                        "%s [%s-%s] Puntas: %s %.2f - %.2f %s" %
                        (
                            msg['Date'], msg['Ticker'], msg['Settlement'], bid_amount, bid_price, offer_price, offer_amount))
            except Exception as error:
                traceback.print_exc()

        ppi.realtime.connect_to_market_data(onconnect, ondisconnect, onmarketdata)

    except Exception as message:
        print(message)


if __name__ == '__main__':
    main()

