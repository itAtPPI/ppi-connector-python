# Imports
from ppi_client.ppi import PPI
from ppi_client.models.instrument import Instrument
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import norm


def get_dataframe_from_marketdata(marketdata):
    return pd.DataFrame.from_dict(marketdata).reset_index(drop = False)


def simulacion_montecarlo(ppi, ticker, tipo_instrumento, dias_a_proyectar, cantidad_simulaciones, precio_a_evaluar):
    # Search Historic MarketData
    print(f"Bajando MarketData de {ticker}")

    market_data = ppi.marketdata.search(ticker, tipo_instrumento, "A-24HS", datetime(2015, 1, 1), datetime(2023, 12, 31))
    df_marketdata = get_dataframe_from_marketdata(market_data)

    df_marketdata_instrumento = df_marketdata[["date", "price"]]

    ult_fecha_dato = df_marketdata_instrumento["date"].max()

    log_returns = np.log(1 + df_marketdata_instrumento["price"].pct_change())

    print("Graficando distribucion de volatilidad")
    sns.displot(log_returns.iloc[1:] * 100)
    plt.xlabel("Volatilidad Diaria")
    plt.ylabel("Frecuencia")
    plt.savefig(f"DistribucionVariaciones_{ticker}.png")

    print("Configurando parametros")
    t = np.arange(1, int(dias_a_proyectar) + 1)

    media = np.mean(log_returns)
    std = np.std(log_returns)

    b = {str(scen): np.random.normal(0, 1, int(dias_a_proyectar)) for scen in range(1, cantidad_simulaciones + 1)}
    W = {str(scen): b[str(scen)].cumsum() for scen in range(1, cantidad_simulaciones + 1)}

    drift = (media - 0.5 * std ** 2) * t
    diffusion = {str(scen): std * W[str(scen)] for scen in range(1, cantidad_simulaciones + 1)}

    print("Iniciando simulacion")
    precios_iniciales = df_marketdata_instrumento.loc[df_marketdata_instrumento.shape[0] - 1, "price"]
    simulaciones = np.array(
        [precios_iniciales * np.exp(drift + diffusion[str(scen)]) for scen in range(1, cantidad_simulaciones + 1)])
    simulaciones = np.hstack((np.array([[precios_iniciales] for scen in range(cantidad_simulaciones)]), simulaciones))

    plt.figure(figsize=(20, 10))

    for i in range(cantidad_simulaciones):
        plt.title(f"Volatilidad Diaria {std * 100:.2f}")
        plt.plot(np.append(df_marketdata_instrumento["price"].to_numpy(), simulaciones[i, :]))
        plt.ylabel("Precio")
        plt.xlabel("Tiempo")

    plt.savefig("Predicciones.png")    

    valores_a_cierre = simulaciones[:, -1]
    probabilidad_ganar = valores_a_cierre[valores_a_cierre > precio_a_evaluar].shape[0] / valores_a_cierre.shape[0]
    print(f"Probabilidad de que el precio de {ticker} sea mayor a ${precio_a_evaluar} dentro de {dias_a_proyectar} ruedas: "
          f"{probabilidad_ganar * 100:.2f}% (tras {cantidad_simulaciones} simulaciones)")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    ppi = PPI(sandbox=False)

    ppi.account.login_api('<key publica>', '<key privada>')

    ticker = "GGAL"

    simulacion_montecarlo(ppi, ticker, "Acciones", dias_a_proyectar = 90, cantidad_simulaciones = 10000, precio_a_evaluar = 500)


