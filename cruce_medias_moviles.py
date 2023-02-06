# Imports
from ppi_client.ppi import PPI
from datetime import datetime, timedelta
import pandas as pd
import matplotlib.pyplot as plt


def get_dataframe_from_marketdata(marketdata):
    return pd.DataFrame.from_dict(marketdata)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    ppi = PPI(sandbox=False)

    # Change login credential to connect to the API
    ppi.account.login_api('<key publica>', '<key privada>')

    ticker = "GGAL"
    tipo_instrumento = "Acciones"

    # Search Historic MarketData
    print(f"Bajando MarketData de {ticker}")

    market_data = ppi.marketdata.search(ticker, tipo_instrumento, "A-48HS", datetime(2015, 1, 1),
                                        datetime(2023, 12, 31))
    df_marketdata = get_dataframe_from_marketdata(market_data)

    medias = [20, 50, 90, 200]

    for media in medias:
        df_marketdata[f"sma{media}"] = df_marketdata["price"].rolling(media).mean()

    df_marketdata.dropna(inplace=True)

    media1 = 20
    media2 = 200

    print(f"Calculando cruce de medias moviles {media1} y {media2}")
    cruces_arriba = df_marketdata[f"sma{media1}"].shift().lt(df_marketdata[f"sma{media2}"]) & df_marketdata[f"sma{media1}"].ge(
        df_marketdata[f"sma{media2}"])
    cruces_abajo = df_marketdata[f"sma{media1}"].shift().gt(df_marketdata[f"sma{media2}"]) & df_marketdata[f"sma{media1}"].le(
        df_marketdata[f"sma{media2}"])

    plt.figure(figsize=(20, 10))

    plt.ylabel("Precio")
    plt.xlabel("Tiempo")

    plt.plot(df_marketdata["date"], df_marketdata[f"price"], label=ticker, linewidth=1.5)
    for media in medias:
        plt.plot(df_marketdata["date"], df_marketdata[f"sma{media}"], label=f"SMA {media}")
    plt.legend()
    plt.scatter(df_marketdata[cruces_abajo]["date"], df_marketdata[cruces_abajo]["price"], c="#ff0000", marker="v", s=200)
    plt.scatter(df_marketdata[cruces_arriba]["date"], df_marketdata[cruces_arriba]["price"], c="#008900", marker="^", s=200)

    plt.savefig(f"GraficoMedias{ticker}ConCruces.png")



