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

# Change sandbox variable to False to connect to production environment
ppi = PPI(sandbox=False)

#Listado con las cotizaciones que se van a usar
cotizaciones = {
    "MEP-AL30": 0,
    "CCL-AL30": 0,
    "MEP-AL35": 0,
    "CCL-AL35": 0,
    "MEP-GD30": 0,
    "CCL-GD30": 0,
    "AL30": 0,
    "AL30C": 0,
    "AL30D": 0,
    "AL35": 0,
    "AL35C": 0,
    "AL35D": 0,
    "GD30": 0,
    "GD30C": 0,
    "GD30D": 0
}

#Recalcula las cotizaciones y las muestra en pantalla
def calcular_y_mostrar():
    cotizaciones["MEP-AL30"] = cotizaciones["AL30"] / cotizaciones["AL30D"]
    cotizaciones["CCL-AL30"] = cotizaciones["AL30"] / cotizaciones["AL30C"]
    cotizaciones["MEP-AL35"] = cotizaciones["AL35"] / cotizaciones["AL35D"]
    cotizaciones["CCL-AL35"] = cotizaciones["AL35"] / cotizaciones["AL35C"]
    cotizaciones["MEP-GD30"] = cotizaciones["GD30"] / cotizaciones["GD30D"]
    cotizaciones["CCL-GD30"] = cotizaciones["GD30"] / cotizaciones["GD30C"]

    print("\nCotizacion a las %s" % datetime.now())
    print("Dolar MEP calculado con AL30 %.3f" % cotizaciones["MEP-AL30"])
    print("Dolar CCL calculado con AL30 %.3f" % cotizaciones["CCL-AL30"])
    print("Dolar MEP calculado con AL35 %.3f" % cotizaciones["MEP-AL35"])
    print("Dolar CCL calculado con AL35 %.3f" % cotizaciones["CCL-AL35"])
    print("Dolar MEP calculado con GD30 %.3f" % cotizaciones["MEP-GD30"])
    print("Dolar CCL calculado con GD30 %.3f" % cotizaciones["CCL-GD30"])


def main():
    try:
        ppi.account.login('<user key>', '<user secret>')

        def onconnect_marketdata():
            try:
                print("\nConnected to realtime market data")

                # Obtengo las ultimas cotizaciones de cada instrumento
                print("\nSearching Current MarketData")
                msg = ppi.marketdata.current("AL30", "BONOS", "INMEDIATA")
                cotizaciones["AL30"] = msg['price']
                msg = ppi.marketdata.current("AL30C", "BONOS", "INMEDIATA")
                cotizaciones["AL30C"] = msg['price']
                msg = ppi.marketdata.current("AL30D", "BONOS", "INMEDIATA")
                cotizaciones["AL30D"] = msg['price']
                
                msg = ppi.marketdata.current("AL35", "BONOS", "INMEDIATA")
                cotizaciones["AL35"] = msg['price']
                msg = ppi.marketdata.current("AL35C", "BONOS", "INMEDIATA")
                cotizaciones["AL35C"] = msg['price']
                msg = ppi.marketdata.current("AL35D", "BONOS", "INMEDIATA")
                cotizaciones["AL35D"] = msg['price']

                msg = ppi.marketdata.current("GD30", "BONOS", "INMEDIATA")
                cotizaciones["GD30"] = msg['price']
                msg = ppi.marketdata.current("GD30C", "BONOS", "INMEDIATA")
                cotizaciones["GD30C"] = msg['price']
                msg = ppi.marketdata.current("GD30D", "BONOS", "INMEDIATA")
                cotizaciones["GD30D"] = msg['price']

                calcular_y_mostrar()

                # Me suscribo a novedades
                ppi.realtime.subscribe_to_element(Instrument("AL30", "BONOS", "INMEDIATA"))
                ppi.realtime.subscribe_to_element(Instrument("AL30C", "BONOS", "INMEDIATA"))
                ppi.realtime.subscribe_to_element(Instrument("AL30D", "BONOS", "INMEDIATA"))
                ppi.realtime.subscribe_to_element(Instrument("AL35", "BONOS", "INMEDIATA"))
                ppi.realtime.subscribe_to_element(Instrument("AL35C", "BONOS", "INMEDIATA"))
                ppi.realtime.subscribe_to_element(Instrument("AL35D", "BONOS", "INMEDIATA"))
                ppi.realtime.subscribe_to_element(Instrument("GD30", "BONOS", "INMEDIATA"))
                ppi.realtime.subscribe_to_element(Instrument("GD30C", "BONOS", "INMEDIATA"))
                ppi.realtime.subscribe_to_element(Instrument("GD30D", "BONOS", "INMEDIATA"))

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

                #Si fue una nueva cotizacion
                if msg["Trade"]:
                    cotizaciones[msg['Ticker']] = msg['Price']

                    calcular_y_mostrar()
            except Exception as error:
                print(datetime.now())
                print("Error en marketdata: %s. Trace:\n" % error)
                traceback.print_exc()

        ppi.realtime.connect_to_market_data(onconnect_marketdata, ondisconnect_marketdata, onmarketdata)
        
        # Starts connections to real time: for example to account or market data
        ppi.realtime.start_connections()

    except Exception as message:
        print(message)


if __name__ == '__main__':
    main()
