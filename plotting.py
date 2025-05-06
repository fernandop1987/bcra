# plotting.py

import plotly.graph_objects as go
import pandas as pd

def plot_inflacion(df):
    df = df.sort_values("fecha").reset_index(drop=True)

    ultimo_valor = df["valor"].dropna().iloc[-1]
    ultimo_mes = df["fecha"].dt.strftime("%B %Y").iloc[-1]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["fecha"],
        y=df["valor"],
        fill="tozeroy",
        mode="lines",
        connectgaps=True,
        line=dict(color="#1E90FF", width=3)
    ))
    fig.update_layout(
        paper_bgcolor="#0B2C66",
        plot_bgcolor="#0B2C66",
        font=dict(family="Segoe UI", size=13, color="white"),
        height=616,
        margin=dict(l=25, r=25, t=200, b=30),

        title=dict(
            text=f"<b>Inflación mensual</b><br><span style='font-size:14px'>{ultimo_mes}</span>",
            x=0.05,
            y=0.92,
            xanchor='left',
            yanchor='top',
            font=dict(size=18, color="white")
        ),

        annotations=[
            dict(
                x=-0.05,
                y=1.3,
                xref="paper", yref="paper",
                showarrow=False,
                text=f"<span style='font-size:24px'><b>{ultimo_valor:.1f} %</b></span>",
                font=dict(color="white"),
                align="left"
            )
        ],

        xaxis=dict(
            title="",
            showgrid=False,
            tickmode="array",
            tickvals=df["fecha"],
            ticktext=[d.strftime('%b\n%Y') for d in df["fecha"]],
            tickfont=dict(color="white"),
            ticks="outside"
        ),
        yaxis=dict(
            showgrid=False,
            tickfont=dict(color="white"),
            ticks="outside"
        ),
        hovermode="x unified",
        showlegend=False
    )
    return fig

def plot_tasa_monetaria(df):
    df["fecha"] = pd.to_datetime(df["fecha"])
    df = df.sort_values("fecha")
    df["mes"] = df["fecha"].dt.to_period("M")
    df_tasa_mensual = df.groupby("mes").last().reset_index()
    df_tasa_mensual["fecha"] = df_tasa_mensual["mes"].dt.to_timestamp()
    df_tasa_mensual.drop(columns="mes", inplace=True)

    ultimo_valor = df_tasa_mensual["valor"].dropna().iloc[-1]
    ultimo_mes = df_tasa_mensual["fecha"].dt.strftime("%B %Y").iloc[-1]

    min_y = (df["valor"].min()) * 0.95
    max_y = (df["valor"].max()) * 1.05

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["fecha"],
        y=df["valor"],
        fill="tozeroy",
        mode="lines",
        connectgaps=True,
        line=dict(color="#1E90FF", width=3)
    ))
    fig.update_layout(
        paper_bgcolor="#0B2C66",
        plot_bgcolor="#0B2C66",
        font=dict(family="Segoe UI", size=13, color="white"),
        height=300,
        margin=dict(l=25, r=25, t=100, b=30),

        title=dict(
            text=f"<b>Tasa de Política Monetaria</b><br><span style='font-size:14px'>{ultimo_mes}</span>",
            x=0.05,
            y=0.92,
            xanchor='left',
            yanchor='top',
            font=dict(size=18, color="white")
        ),

        annotations=[
            dict(
                x=-0.05,
                y=1.3,
                xref="paper", yref="paper",
                showarrow=False,
                text=f"<span style='font-size:24px'><b>{ultimo_valor:.1f} %</b></span>",
                font=dict(color="white"),
                align="left"
            )
        ],

        xaxis=dict(
            showgrid=False,
            tickmode="array",
            tickvals=df_tasa_mensual["fecha"],
            ticktext=[d.strftime('%b\n%Y') for d in df_tasa_mensual["fecha"]],
            tickfont=dict(color="white"),
            ticks="outside"
        ),
        yaxis=dict(
            showgrid=False,
            range=[min_y, max_y],
            tickfont=dict(color="white"),
            ticks="outside"
        ),
        hovermode="x unified",
        showlegend=False
    )
    return fig

def plot_reservas(df):
    df["reservas"] = df["valor"] 
    df["fecha"] = pd.to_datetime(df["fecha"])
    df = df.sort_values("fecha").reset_index(drop=True)
    tickvals = df["fecha"].dt.to_period("M").drop_duplicates().dt.to_timestamp()
    ultimo_valor = df["reservas"].dropna().iloc[-1]
    ultimo_mes = df["fecha"].dt.strftime("%B %Y").iloc[-1]
    min_y = (df["reservas"].min() / 1000) * 0.95
    max_y = (df["reservas"].max() / 1000) * 1.05


    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["fecha"],
        y=df["reservas"] / 1000,
        fill="tozeroy",
        mode="lines",
        connectgaps=True,
        line=dict(color="#2ECC71", width=3)
    ))
    fig.update_layout(
        paper_bgcolor="#0B2C66",
        plot_bgcolor="#0B2C66",
        font=dict(family="Segoe UI", size=13, color="white"),
        height=300,
        margin=dict(l=25, r=25, t=100, b=30),

        title=dict(
            text=f"<b>Reservas Internacionales (000's M USD)</b><br><span style='font-size:14px'>{ultimo_mes}</span>",
            x=0.05,
            y=0.92,
            xanchor='left',
            yanchor='top',
            font=dict(size=18, color="white")
        ),

        annotations=[
            dict(
                x=-0.05,
                y=1.3,
                xref="paper", yref="paper",
                showarrow=False,
                text=f"<span style='font-size:24px'><b>{ultimo_valor/1000:,.1f} M</b></span>",
                font=dict(color="white"),
                align="left"
            )
        ],

        xaxis=dict(
            showgrid=False,
            tickvals=tickvals,
            ticktext=[d.strftime('%b\n%Y') for d in tickvals],
            tickfont=dict(color="white"),
            ticks="outside"
        ),
        yaxis=dict(
            range=[min_y, max_y],
            showgrid=False,
            tickfont=dict(color="white"),
            ticks="outside"
        ),
        hovermode="x unified",
        showlegend=False
    )

    return fig

def plot_tipo_cambio(df):
    tickvals = df["fecha"].dt.to_period("M").drop_duplicates().dt.to_timestamp()
    ultimo_usd_oficial = df["usd_oficial"].dropna().iloc[-1]
    ultimo_usd_blue = df["usd_blue"].dropna().iloc[-1]
    ultimo_mes = df["fecha"].dt.strftime("%B %Y").iloc[-1]

    min_y = df[["usd_oficial", "usd_blue"]].min().min() * 0.95
    max_y = df[["usd_oficial", "usd_blue"]].max().max() * 1.05

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["fecha"],
        y=df["usd_oficial"],
        fill="tozeroy",
        mode="lines",
        connectgaps=True,
        line=dict(color="#2ECC71", width=3),
        name="USD Oficial"
    ))
    fig.add_trace(go.Scatter(
        x=df["fecha"],
        y=df["usd_blue"],
        mode="lines",
        connectgaps=True,
        line=dict(color="#2ECC71", width=3, dash="dot"),
        name="USD Blue"
    ))
    fig.update_layout(
        paper_bgcolor="#0B2C66",
        plot_bgcolor="#0B2C66",
        font=dict(family="Segoe UI", size=13, color="white"),
        height=300,
        margin=dict(l=25, r=25, t=100, b=30),

        title=dict(
            text=f"<b>Tipo de Cambio (USD Oficial y Blue)</b><br><span style='font-size:14px'>{ultimo_mes}</span>",
            x=0.05,
            y=0.92,
            xanchor='left',
            yanchor='top',
            font=dict(size=18, color="white")
        ),

        annotations=[
            dict(
                x=-0.09,
                y=1.52,
                xref="paper", yref="paper",
                showarrow=False,
                text=f"<span style='font-size:20px'><b>Oficial: {ultimo_usd_oficial:,.0f} | Blue: {ultimo_usd_blue:,.0f}</b></span>",
                font=dict(color="white"),
                align="left"
            )
        ],

        xaxis=dict(
            title="",
            showgrid=False,
            tickvals=tickvals,
            ticktext=[d.strftime('%b\n%Y') for d in tickvals],
            tickfont=dict(color="white"),
            ticks="outside"
        ),
        yaxis=dict(
            range=[min_y, max_y],
            showgrid=False,
            tickfont=dict(color="white"),
            ticks="outside"
        ),
        hovermode="x unified",
        showlegend=True,
        legend=dict(
            orientation="h",
            y=-0.9,
            x=0.5,
            xanchor='center',
            font=dict(size=11, color="white")
        )
    )
    return fig

def plot_cny(df):
    tickvals = df["fecha"].dt.to_period("M").drop_duplicates().dt.to_timestamp()
    ultimo_valor = df["cny_oficial"].dropna().iloc[-1]
    ultimo_mes = df["fecha"].dt.strftime("%B %Y").iloc[-1]
    min_y = df["cny_oficial"].min() * 0.95
    max_y = df["cny_oficial"].max() * 1.05

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["fecha"],
        y=df["cny_oficial"],
        fill="tozeroy",
        mode="lines",
        connectgaps=True,
        line=dict(color="#2ECC71", width=3)
    ))
    fig.update_layout(
        paper_bgcolor="#0B2C66",
        plot_bgcolor="#0B2C66",
        font=dict(family="Segoe UI", size=13, color="white"),
        height=300,
        margin=dict(l=25, r=25, t=100, b=30),

        title=dict(
            text=f"<b>Tipo de Cambio (CNY/ARS)</b><br><span style='font-size:14px'>{ultimo_mes}</span>",
            x=0.05,
            y=0.92,
            xanchor='left',
            yanchor='top',
            font=dict(size=18, color="white")
        ),

        annotations=[
            dict(
                x=-0.07,
                y=1.3,
                xref="paper", yref="paper",
                showarrow=False,
                text=f"<span style='font-size:24px'><b>{ultimo_valor:,.1f}</b></span>",
                font=dict(color="white"),
                align="left"
            )
        ],

        xaxis=dict(
            showgrid=False,
            tickvals=tickvals,
            ticktext=[d.strftime('%b\n%Y') for d in tickvals],
            tickfont=dict(color="white"),
            ticks="outside"
        ),
        yaxis=dict(
            range=[min_y, max_y],
            showgrid=False,
            tickfont=dict(color="white"),
            ticks="outside"
        ),
        hovermode="x unified",
        showlegend=False
    )
    return fig

def plot_merval(df):
    tickvals = df["fecha"].dt.to_period("M").drop_duplicates().dt.to_timestamp()
    ultimo_valor_merval = df["merval_usd"].dropna().iloc[-1]
    ultimo_mes_merval = df["fecha"].dt.strftime("%B %Y").iloc[-1]
    min_y = df["merval_usd"].min() * 0.95
    max_y = df["merval_usd"].max() * 1.05
    
    if df.empty or "fecha" not in df.columns or "merval_usd" not in df.columns:
        return go.Figure()
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df["fecha"],
        y=df["merval_usd"],
        fill="tozeroy",
        mode="lines",
        connectgaps=True,
        line=dict(color="#FF5733", width=3)
    ))
    fig.update_layout(
        paper_bgcolor="#0B2C66",
        plot_bgcolor="#0B2C66",
        font=dict(family="Segoe UI", size=13, color="white"),
        height=300,
        margin=dict(l=25, r=25, t=100, b=30),

        title=dict(
            text=f"<b>Merval en USD</b><br><span style='font-size:14px'>{ultimo_mes_merval}</span>",
            x=0.05,
            y=0.92,
            xanchor='left',
            yanchor='top',
            font=dict(size=18, color="white")
        ),

        annotations=[
            dict(
                x=-0.08,
                y=1.3,
                xref="paper", yref="paper",
                showarrow=False,
                text=f"<span style='font-size:24px'><b>{ultimo_valor_merval:,.0f}</b></span>",
                font=dict(color="white"),
                align="left"
            )
        ],

        xaxis=dict(
            showgrid=False,
            tickvals=tickvals,
            ticktext=[d.strftime('%b\n%Y') for d in tickvals],
            tickfont=dict(color="white"),
            ticks="outside"
        ),
        yaxis=dict(
            range=[min_y, max_y],
            showgrid=False,
            tickfont=dict(color="white"),
            ticks="outside"
        ),
        hovermode="x unified",
        showlegend=False
    )
    return fig

def plot_cedears(df):
    cedears = {"YPFD.BA": "YPF", "GGAL.BA": "Galicia", "BMA.BA": "Banco Macro", "MELI.BA": "MercadoLibre"}
    colors = ["#FF5733", "#1E90FF", "#2ECC71", "#7FDBFF"]
    primer_mes = df["fecha"].dt.strftime("%B %Y").iloc[0]

    fig = go.Figure()
    for i, (ticker, name) in enumerate(cedears.items()):
        fig.add_trace(go.Scatter(
            x=df["fecha"],
            y=df[ticker],
            mode="lines",
            connectgaps=True,
            name=name,
            line=dict(width=2, color=colors[i % len(colors)])
        ))
    fig.update_layout(
        paper_bgcolor="#0B2C66",
        plot_bgcolor="#0B2C66",
        font=dict(family="Segoe UI", size=13, color="white"),
        height=616,
        margin=dict(l=25, r=25, t=150, b=30),
        title=dict(
            text=f"<b>Evolución principales acciones</b><br><span style='font-size:14px'>Indice 100 - {primer_mes}</span>",
            x=0.05,
            y=0.92,
            xanchor='left',
            yanchor='top',
            font=dict(size=18, color="white")
        ),
        xaxis=dict(
            title="",
            showgrid=False,
            tickfont=dict(color="white"),
            ticks="outside"
        ),
        yaxis=dict(
            showgrid=False,
            tickfont=dict(color="white"),
            ticks="outside"
        ),
        hovermode="x unified",
        legend=dict(
            orientation="h",
            y=-0.25,
            x=0.5,
            xanchor='center',
            font=dict(size=11, color="white")
        )
    )
    return fig

