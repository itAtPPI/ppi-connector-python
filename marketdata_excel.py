# Codigo propio de ppi, siempre obligatorio
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
from openpyxl import Workbook

# Change sandbox variable to False to connect to production environment
ppi = PPI(sandbox=False)


def main():
    try:
        # Change login credential to connect to the API
        ppi.account.login('<user key>', '<user secret>')

        # Obtengo las cotizaciones historicas
        print("\nSearching MarketData")
        market_data = ppi.marketdata.search(SearchDateMarketData("GGAL", "Acciones", "A-48HS",
                                                                 "2021-01-01", "2021-12-31"))

        # Creo el excel
        workbook = Workbook()
        sheet = workbook.active

        # Completo los encabezados
        sheet.cell(row=1, column=1).value = "Fecha"
        sheet.cell(row=1, column=2).value = "Cotizacion"
        sheet.cell(row=1, column=3).value = "Volumen"
        sheet.cell(row=1, column=4).value = "Apertura"
        sheet.cell(row=1, column=5).value = "Minimo"
        sheet.cell(row=1, column=6).value = "Maximo"

        r = 1
        # LLeno el excel
        for ins in market_data:
            r = r + 1
            sheet.cell(row=r, column=1).value = ins['date']
            sheet.cell(row=r, column=2).value = ins['price']
            sheet.cell(row=r, column=3).value = ins['volume']
            sheet.cell(row=r, column=4).value = ins['openingPrice']
            sheet.cell(row=r, column=5).value = ins['min']
            sheet.cell(row=r, column=6).value = ins['max']

        #Guardo el excel
        workbook.save(filename="marketdata.xlsx")
        print("\nExportacion realizada con exito")

    except Exception as message:
        print(datetime.now())
        print(message)

    input('\nPress Enter to exit')

if __name__ == '__main__':
    main()

