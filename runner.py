from ppi_client.api.constants import ACCOUNTDATA_TYPE_ACCOUNT_NOTIFICATION, ACCOUNTDATA_TYPE_PUSH_NOTIFICATION, \
    ACCOUNTDATA_TYPE_ORDER_NOTIFICATION
from ppi_client.models.account_movements import AccountMovements
from ppi_client.models.bank_account_request import BankAccountRequest
from ppi_client.models.estimate_bonds import EstimateBonds
from ppi_client.models.foreign_bank_account_request import ForeignBankAccountRequest, ForeignBankAccountRequestDTO
from ppi_client.models.cancel_bank_account_request import CancelBankAccountRequest
from ppi_client.models.order import Order
from ppi_client.ppi import PPI
from ppi_client.models.order_budget import OrderBudget
from ppi_client.models.order_confirm import OrderConfirm
from ppi_client.models.transfer_budget import TransferBudget
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


def main():
    try:
        # Change login credential to connect to the API
        ppi.account.login_api('<key publica>', '<key privada>')

        # Getting accounts information
        print("Getting accounts information")
        account_numbers = ppi.account.get_accounts()
        for account in account_numbers:
            print(account)
        account_number = account_numbers[0]['accountNumber']

        # Getting bank account information
        print("\nGetting bank account information of %s" % account_number)
        bank_accounts = ppi.account.get_bank_accounts(account_number)
        for bank_account in bank_accounts:
            print(bank_account)

        # Getting available balance
        print("\nGetting available balance of %s" % account_number)
        balances = ppi.account.get_available_balance(account_number)
        for balance in balances:
            print("Currency %s - Settlement %s - Amount %s %s" % (
                balance['name'], balance['settlement'], balance['symbol'], balance['amount']))

        # Getting balance and positions
        print("\nGetting balance and positions of %s" % account_number)
        balances_positions = ppi.account.get_balance_and_positions(account_number)
        for balance in balances_positions["groupedAvailability"]:
            for currency in balance['availability']:
                print("Currency %s Settlement %s Amount %s %s" % (
                    currency['name'], currency['settlement'], currency['symbol'], currency['amount']))
        for instruments in balances_positions["groupedInstruments"]:
            print("Instrument %s " % instruments['name'])
            for instrument in instruments['instruments']:
                print("Ticker %s Price %s Amount %s" % (
                    instrument['ticker'], instrument['price'], instrument['amount']))

        # Getting movements
        print("\nGetting movements of %s" % account_number)
        movements = ppi.account.get_movements(AccountMovements(account_number, datetime(2021, 12,1),
                                                               datetime(2021, 12, 31), None))
        for mov in movements:
            print("%s %s - Currency %s Amount %s " % (
                mov['settlementDate'], mov['description'], mov['currency'], mov['amount']))

        # Getting instrument types
        print("\nGetting instrument types")
        instruments = ppi.configuration.get_instrument_types()
        for item in instruments:
            print(item)

        # Getting markets
        print("\nGetting markets")
        markets = ppi.configuration.get_markets()
        for item in markets:
            print(item)

        # Getting settlements
        print("\nGetting settlements")
        settlements = ppi.configuration.get_settlements()
        for item in settlements:
            print(item)

        # Getting quantity types
        print("\nGetting quantity types")
        quantity_types = ppi.configuration.get_quantity_types()
        for item in quantity_types:
            print(item)

        # Getting operation terms
        print("\nGetting operation terms")
        operation_terms = ppi.configuration.get_operation_terms()
        for item in operation_terms:
            print(item)

        # Getting operation types
        print("\nGetting operation types")
        operation_types = ppi.configuration.get_operation_types()
        for item in operation_types:
            print(item)

        # Getting operations
        print("\nGetting operations")
        operations = ppi.configuration.get_operations()
        for item in operations:
            print(item)
            
        # Get holidays
        print("\nGet local holidays for the current year")
        holidays = ppi.configuration.get_holidays(start_date=datetime(2022, 1, 1), end_date=datetime(2022, 12, 31))
        for holiday in holidays:
            print("%s - %s " % (holiday["date"][0:10], holiday["description"]))
        
        print("\nGet USA holidays for the current year")
        holidays = ppi.configuration.get_holidays(start_date=datetime(2022, 1, 1), end_date=datetime(2022, 12, 31),
                                                  is_usa=True)
        for holiday in holidays:
            print("%s - %s " % (holiday["date"][0:10], holiday["description"]))

        # Check holidays
        print("\nIs today a local holiday?")
        print(ppi.configuration.is_local_holiday())
        print("\nIs today a holiday in the USA?")
        print(ppi.configuration.is_usa_holiday())

        # Search Instrument
        print("\nSearching instruments")
        instruments = ppi.marketdata.search_instrument("GGAL", "", "Byma", "Acciones")
        for ins in instruments:
            print(ins)

        # Search Historic MarketData
        print("\nSearching MarketData")
        market_data = ppi.marketdata.search("GGAL", "Acciones", "A-48HS", datetime(2021, 1, 1), datetime(2021, 12, 31))
        for ins in market_data:
            print("%s - %s - Volume %s - Opening %s - Min %s - Max %s" % (
                ins['date'], ins['price'], ins['volume'], ins['openingPrice'], ins['min'], ins['max']))

        # Search Current MarketData
        print("\nSearching Current MarketData")
        current_market_data = ppi.marketdata.current("GGAL", "Acciones", "A-48HS")
        print(current_market_data)

        # Search Current Book
        print("\nSearching Current Book")
        current_book = ppi.marketdata.book("GGAL", "Acciones", "A-48HS")
        print(current_book)

        # Search Intraday MarketData
        print("\nSearching Intraday MarketData")
        intraday_market_data = ppi.marketdata.intraday("GGAL", "Acciones", "A-48HS")
        for intra in intraday_market_data:
            print(intra)

        # Get orders
        print("\nGet orders")
        orders = ppi.orders.get_orders(account_number, date_from=datetime.today() + timedelta(days=-100),
                                       date_to=datetime.today())
        for order in orders:
            print(order)

        # Get active orders
        print("\nGet active orders")
        active_orders = ppi.orders.get_active_orders(account_number)
        for order in active_orders:
            print(order)

        ''' Uncomment to create an order
        # Get budget
        print("\nGet budget for the order")
        budget_order = ppi.orders.budget(OrderBudget(account_number, 10000, 150, "GGAL", "ACCIONES", "Dinero",
                                                     "PRECIO-LIMITE", "HASTA-SU-EJECUCIÓN", None, "Compra",
                                                     "INMEDIATA"))
        print(budget_order)
        disclaimers_order = budget_order['disclaimers']

        # Confirm order
        print("\nConfirm order")
        accepted_disclaimers = []
        for disclaimer in disclaimers_order:
            accepted_disclaimers.append(Disclaimer(disclaimer['code'], True))
        confirmation = ppi.orders.confirm(OrderConfirm(account_number, 10000, 150, "GGAL", "ACCIONES", "Dinero",
                                                       "PRECIO-LIMITE", "HASTA-SU-EJECUCIÓN", None, "Compra"
                                                       , "INMEDIATA", accepted_disclaimers, None))
        print(confirmation)
        order_id = confirmation["id"]
        '''

        ''' Uncomment to create a stop order
        # Get budget
        print("\nGet budget for the stop order")
        budget_stop_order = ppi.orders.budget(OrderBudget(account_number, 1000, 3000.5, "GOOGL", "CEDEARS",
                                                          "Papeles", "PRECIO-LIMITE", "HASTA-SU-EJECUCIÓN", None,
                                                          "Stop Order", "INMEDIATA", 2998.5))
        print(budget_stop_order)
        disclaimers_stop_order = budget_stop_order['disclaimers']

        # Confirm stop order
        print("\nConfirm stop order")
        accepted_disclaimers = []
        for disclaimer in disclaimers_stop_order:
            accepted_disclaimers.append(Disclaimer(disclaimer['code'], True))
        stop_order_confirmation = ppi.orders.confirm(OrderConfirm(account_number, 1000, 3000.5, "GOOGL", "CEDEARS",
                                                                  "Papeles", "PRECIO-LIMITE", "HASTA-SU-EJECUCIÓN",
                                                                  None, "Stop Order", "INMEDIATA",
                                                                  accepted_disclaimers, None, 2998.5))
        print(stop_order_confirmation)
        stop_order_id = stop_order_confirmation["id"]
        '''

        ''' Uncomment to get the detail of an order
        # Get order detail
        print("\nGet order detail")
        detail = ppi.orders.get_order_detail(account_number, order_id, None)
        print(detail)
        '''

        ''' Uncomment to execute cancellation of an order
        # Cancel order
        print("\nCancel order")
        cancel = ppi.orders.cancel_order(Order(order_id, account_number, None))
        print(cancel)
        '''

        ''' Uncomment to execute mass cancellation of orders
        # Cancel all active orders
        print("\nMass Cancel")
        cancels = ppi.orders.mass_cancel_order(account_number)
        print(cancels)
        '''

        ''' Uncomment to create a transfer
        # Get transfer budget
        print("\nGet budget for the transfer")
        budget_transfer = ppi.orders.budget_transfer(TransferBudget(account_number, bank_account['taxHolderIdentifier'],
                                                                    "ARS", bank_account['bankIdentifier'], None, 1000))
        print(budget_transfer)

        # Confirm transfer
        print("\nConfirm transfer")
        confirmation = ppi.orders.confirm_transfer(TransferBudget(account_number, bank_account['taxHolderIdentifier'],
                                                                  "ARS", bank_account['bankIdentifier'], None, 1000))
        print(confirmation)
        '''

        ''' Uncomment to get investing profile questions
        # Get investing profile questions
        print("\nGet investing profile questions")
        investing_profile_questions = ppi.account.get_investing_profile_questions()
        for question in investing_profile_questions:
            print("%s - %s " % (question["code"], question["description"]))
            for answer in question["answers"]:
                print("%s - %s " % (answer["code"], answer["description"]))
        '''

        ''' Uncomment to get investing profile instrument types
        # Get investing profile instrument types
        print("\nGet investing profile instrument types")
        investing_profile_instrument_types = ppi.account.get_investing_profile_instrument_types()
        for instrument in investing_profile_instrument_types:
            print(instrument)
        '''

        ''' Uncomment to get investing profile result for a given account number
        # Get investing profile for an account number
        print("\nGet investing profile for account number")
        profile = ppi.account.get_investing_profile(account_number)
        print("Date: %s - Type: %s - %s" % (profile["date"], profile["type"], profile["description"]))
        '''

        ''' Uncomment to set investing profile for a given account number
        # Set investing profile
        print("\nSetting investing profile for account number")
        answers = [InvestingProfileAnswer("GRADO_CONOCIMIENTO", "A"), InvestingProfileAnswer("INVERSION_ANTERIOR", "C"),
                   InvestingProfileAnswer("PORCENTAJE_AHORRO", "A"), InvestingProfileAnswer("PLAZO_MAXIMO", "C"),
                   InvestingProfileAnswer("INVERSION_PREOCUPACION", "A"),
                   InvestingProfileAnswer("PORCENTAJE_DISMINUCION", "B"),
                   InvestingProfileAnswer("MONTO_INVERSION", "A")]
        instrument_types = ["BONOS-(RENTA-FIJA)", "ACCIONES-ARGENTINAS-(RENTA-VARIABLE-LOCAL)",
                            "FIDEICOMISOS-FINANCIEROS"]
        new_profile = ppi.account.set_investing_profile(InvestingProfile(account_number, answers, instrument_types))
        print("New investing profile - Date: %s - Type: %s - %s" % (new_profile["date"], new_profile["type"],
                                                                    new_profile["description"]))
        '''

        ''' Uncomment to register a bank account
        # Register a bank account
        print("\nRegistering bank account")
        bank_account_request = ppi.account.register_bank_account(
            BankAccountRequest(account_number, currency="ARS", cbu="", cuit="00000000000",
                               alias="ALIASCBU", bank_account_number=""))
        print(bank_account_request)
        '''

        ''' Uncomment to register a foreign bank account
        # Register a foreign bank account
        print("\nRegistering foreign bank account")
        data = ForeignBankAccountRequestDTO(account_number=account_number, cuit="00000000000", intermediary_bank="",
                                            intermediary_bank_account_number="", intermediary_bank_swift="",
                                            bank="The Bank of Tokyo-Mitsubishi, Ltd.", bank_account_number="12345678",
                                            swift="ABC", ffc="Juan Perez")
        extract_file_route = "C:\\Documents\example.pdf"
        extract_file = (os.path.basename(extract_file_route), open(extract_file_route, 'rb'))
        foreign_bank_account_request = ppi.account.register_foreign_bank_account(
            ForeignBankAccountRequest(data, extract_file))
        print(foreign_bank_account_request)
        '''

        ''' Uncomment to cancel a bank account
        # Cancel a bank account
        print("\nCanceling bank account")
        cancel_bank_account_request = ppi.account.cancel_bank_account(
            CancelBankAccountRequest(account_number, cbu="0000000000000000000000", bank_account_number=""))
        print(cancel_bank_account_request)
        '''
        
        # Estimate bond
        print("\nEstimate bond")
        estimate = ppi.marketdata.estimate_bonds(EstimateBonds(ticker="CUAP", date=datetime.today(), quantityType="PAPELES", quantity=100,
                                                               price=4555))
        print(estimate)

        # Realtime subscription to market data
        def onconnect_marketdata():
            try:
                print("\nConnected to realtime market data")
                ppi.realtime.subscribe_to_element(Instrument("GGAL", "ACCIONES", "A-48HS"))
                ppi.realtime.subscribe_to_element(Instrument("AAPL", "CEDEARS", "A-48HS"))
                ppi.realtime.subscribe_to_element(Instrument("AL30", "BONOS", "INMEDIATA"))
                ppi.realtime.subscribe_to_element(Instrument("AL30D", "BONOS", "INMEDIATA"))
                ppi.realtime.subscribe_to_element(Instrument("DLR/MAR22", "FUTUROS", "INMEDIATA"))
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

        ''' Uncomment to use realtime account data
        # Realtime subscription to account data
        def onconnect_accountdata():
            try:
                print("Connected to account data")
                ppi.realtime.subscribe_to_account_data(account_number)
            except Exception as error:
                traceback.print_exc()

        def ondisconnect_accountdata():
            try:
                print("Disconnected from account data")
            except Exception as error:
                traceback.print_exc()

        # Realtime AccountData
        def onaccountdata(data):
            try:
                msg = json.loads(data)
                if msg["Type"] == ACCOUNTDATA_TYPE_PUSH_NOTIFICATION:
                    print("%s - %s" % (msg['Title'], msg['Message']))
                if msg["Type"] == ACCOUNTDATA_TYPE_ACCOUNT_NOTIFICATION:
                    print("%s - %s" % (msg['Date'], msg['Message']))
                if msg["Type"] == ACCOUNTDATA_TYPE_ORDER_NOTIFICATION:
                    print(
                        "Ticker: %s OrderId: %s Quantity executed: %.2f Status: %s Last update: %s Operation: %s" % (
                            msg['Ticker'], msg['OrderId'], msg['QuantityExecuted'], msg['Status'],
                            msg['LastUpdateDate'], msg['Operation']))
            except Exception as error:
                traceback.print_exc()
        
        ppi.realtime.connect_to_account(onconnect_accountdata, ondisconnect_accountdata, onaccountdata)
        '''

        # Starts connections to real time: for example to account or market data
        ppi.realtime.start_connections()

    except Exception as message:
        print(datetime.now())
        print(message)


if __name__ == '__main__':
    main()
