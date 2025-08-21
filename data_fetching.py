# data_fetching.py

import requests
import pandas as pd
import yfinance as yf
import streamlit as st
import datetime

# --- Funciones para obtención de datos ---

def get_bcra_variable(id_variable, start_date, end_date):
    import requests, pandas as pd
    from datetime import datetime

    def _norm(d: str) -> str:
        # acepta 'YYYY-MM-DD' o datetime/date y normaliza a 'YYYY-MM-DD'
        if hasattr(d, "strftime"):
            return d.strftime("%Y-%m-%d")
        d = str(d).strip()
        # corta si venía con 'YYYY-MM-DDTHH...' u otros
        return d[:10]

    desde = _norm(start_date)
    hasta = _norm(end_date)

    # validación rápida de formato y orden (requisito v3.0)
    try:
        d_desde = datetime.strptime(desde, "%Y-%m-%d")
        d_hasta = datetime.strptime(hasta, "%Y-%m-%d")
    except ValueError:
        st.error(f"Fechas inválidas (usa YYYY-MM-DD). Recibí desde='{desde}', hasta='{hasta}'.")
        return pd.DataFrame()
    if d_desde > d_hasta:
        st.warning("Intercambié las fechas porque 'desde' > 'hasta'.")
        desde, hasta = hasta, desde

    base = "https://api.bcra.gob.ar/estadisticas/v3.0/monetarias"
    url = f"{base}/{id_variable}"
    params = {"desde": desde, "hasta": hasta, "limit": 3000, "offset": 0}

    rows = []
    try:
        while True:
            r = requests.get(url, params=params, verify=False, timeout=15)
            # Si el servidor responde 400/404/500, intento extraer el mensaje de error de la API
            if r.status_code != 200:
                try:
                    payload = r.json()
                    msgs = payload.get("errorMessages") or []
                    msg = "; ".join(msgs) if msgs else r.text
                except Exception:
                    msg = r.text
                if r.status_code == 400:
                    st.error(f"Error 400 BCRA: {msg}")
                elif r.status_code == 404:
                    st.error(f"Error 404 BCRA (idVariable={id_variable}): {msg}")
                else:
                    st.error(f"Error {r.status_code} BCRA: {msg}")
                return pd.DataFrame()

            data = r.json()
            chunk = data.get("results", [])
            if not isinstance(chunk, list):
                chunk = []
            rows.extend(chunk)

            # cortar si no hay más páginas
            got = len(chunk)
            lim = params["limit"]
            meta = (data.get("metadata") or {}).get("resultset") or {}
            total = meta.get("count", None)
            if got < lim or (total is not None and params["offset"] + got >= total):
                break
            params["offset"] += lim

        df = pd.DataFrame(rows)
        if df.empty:
            st.warning(f"No se encontraron datos para la variable {id_variable} entre {desde} y {hasta}.")
            return df

        if "fecha" in df.columns:
            df["fecha"] = pd.to_datetime(df["fecha"], errors="coerce")
        if "valor" in df.columns:
            df["valor"] = pd.to_numeric(df["valor"], errors="coerce")
        return df

    except Exception as e:
        st.error(f"Error al conectar con la API del BCRA: {e}")
        return pd.DataFrame()





def get_usd_oficial(fecha_inicio, fecha_fin):
    url = "https://api.bcra.gob.ar/estadisticascambiarias/v1.0/Cotizaciones/USD"
    params = {"fechadesde": fecha_inicio, "fechahasta": fecha_fin, "limit": 1000}
    r = requests.get(url, params=params, verify=False)
    data = r.json()["results"]
    registros = []
    for d in data:
        fecha = d["fecha"]
        for cot in d["detalle"]:
            registros.append({"fecha": fecha, "usd_oficial": cot["tipoCotizacion"]})

    df = pd.DataFrame(registros)
    df["fecha"] = pd.to_datetime(df["fecha"])
    df = df.groupby("fecha").mean(numeric_only=True).reset_index()
    df = df.dropna(subset=["fecha", "usd_oficial"]).drop_duplicates(subset=["fecha"])
    return df

def get_usd_blue():
    url = "https://api.bluelytics.com.ar/v2/evolution.json"
    r = requests.get(url)
    if r.status_code == 200:
        data = r.json()
        blue_data = [entry for entry in data if entry["source"] == "Blue"]
        df = pd.DataFrame(blue_data)
        df["fecha"] = pd.to_datetime(df["date"])
        df["usd_blue"] = (df["value_buy"] + df["value_sell"]) / 2
        df = df.dropna(subset=["fecha", "usd_blue"]).drop_duplicates(subset=["fecha"])
        return df[["fecha", "usd_blue"]]
    else:
        raise Exception("Error al obtener USD Blue")

def get_cny_oficial(start_date, end_date):
    url = "https://api.bcra.gob.ar/estadisticascambiarias/v1.0/Cotizaciones/CNY"
    params = {"fechadesde": start_date, "fechahasta": end_date, "limit": 1000}
    r = requests.get(url, params=params, verify=False)
    if r.status_code == 200:
        data = r.json()['results']
        registros = []
        for d in data:
            fecha = d['fecha']
            for cot in d['detalle']:
                registros.append({"fecha": fecha, "cny_oficial": cot['tipoCotizacion']})
        df = pd.DataFrame(registros)
        df['fecha'] = pd.to_datetime(df['fecha'])
        return df.groupby('fecha').mean().reset_index()
    else:
        raise Exception("Error al obtener CNY Oficial")

def get_inflacion(start_date, end_date):
    return get_bcra_variable(27, start_date, end_date)

def get_tasa_monetaria(start_date, end_date):
    return get_bcra_variable(6, start_date, end_date)

def get_reservas(start_date, end_date):
    return get_bcra_variable(1, start_date, end_date)

def get_tipo_cambio(start_date, end_date):
    df_usd_oficial = get_usd_oficial(start_date, end_date)
    df_usd_blue = get_usd_blue()
    df_usd_blue = df_usd_blue[df_usd_blue['fecha'].between(start_date, end_date)]
    df = pd.merge(df_usd_oficial, df_usd_blue, on='fecha', how='outer')
    df = df.sort_values('fecha').reset_index(drop=True)
    return df

def get_cny(start_date, end_date):
    df_cny = get_cny_oficial(start_date, end_date)
    df_cny = df_cny[df_cny['fecha'].between(start_date, end_date)].reset_index(drop=True)
    return df_cny

def get_merval(start_date, end_date):
    merval = yf.download("^MERV", start=start_date, end=end_date)
    merval_close = merval.xs("Close", axis=1, level="Price")
    merval = merval_close.rename(columns={"^MERV": "merval_ars"}).reset_index()
    merval = merval.rename(columns={"Date": "fecha"})

    df_usd_blue = get_usd_blue()
    df_usd_blue = df_usd_blue[df_usd_blue["fecha"].between(start_date, end_date)]

    df = pd.merge(merval, df_usd_blue, on="fecha", how="inner")
    df["merval_usd"] = df["merval_ars"] / df["usd_blue"]
    df = df.sort_values("fecha").reset_index(drop=True)
    return df




def get_cedears(start_date, end_date):
    cedears = {
    "YPFD.BA": "YPF",
    "GGAL.BA": "Galicia",
    "BMA.BA": "Banco Macro",
    "MELI.BA": "MercadoLibre"
}
    data = yf.download(list(cedears.keys()), start=start_date, end=end_date)["Close"]
    df_cedears = data.reset_index()
    df_cedears = df_cedears.rename(columns={"Date": "fecha"})
    for ticker in cedears.keys():
        if ticker in df_cedears.columns and not df_cedears[ticker].dropna().empty:
            df_cedears[ticker] = (df_cedears[ticker] / df_cedears[ticker].iloc[0]) * 100
    df_cedears = df_cedears.dropna(how="all", subset=list(cedears.keys())).sort_values("fecha").reset_index(drop=True)
    return df_cedears
