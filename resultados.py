import streamlit as st
import requests
import pandas as pd
import altair as alt
import os
from datetime import datetime
from twilio.rest import Client
from zoneinfo import ZoneInfo
import pytz

st.set_page_config(page_title="Previsão de Jogos", layout="wide")

#Credenciais
account_sid = "ACb42d5dd87bca5ad47e794146cfe5da15"
auth_token = "0acc24dc6aafd38deea3d6c84cd6de0b"
# from_whatsapp_number = 
# to_whatsapp_number =


client = Client(account_sid, auth_token)

br_tz = pytz.timezone('America/Sao_Paulo')
data_hoje = datetime.now(br_tz).strftime('%Y-%m-%d')

#IDs de times no Sofascore
team_ids = {
    "Athletico Paranaense": 1967, "Atlético Mineiro": 1977, "Atlético Nacional (COL)": 6106, 
    "Bahia": 1955, "Botafogo": 1958, "Bragantino": 1999, "Ceará": 2001, "Cerro Porteño (PAR)": 5991, 
    "Corinthians": 1957, "Cruzeiro": 1954, "CSA": 2010,
    "CRB": 22032, "Estudiantes (ARG)": 3206,
    "Flamengo": 5981, "Fluminense": 1961, 
    "Fortaleza": 2020, "Grêmio": 5926, 
    "Internacional": 1966, "Juventude": 1980, "Libertad (PAR)": 5996, "LDU (EQU)": 5257,
    "Mirassol": 21982, "Palmeiras": 1963, 
    "Peñarol (URU)": 3227, "River Plate (ARG)": 3211,
    "Santos": 1968,
    "São Paulo": 1981, "Sport": 1959, "Universitario (PER)": 2305,
    "Vasco": 1974, "Vélez Sarsfield (ARG)": 3208,"Vitória": 1962,
    
}

#IDs de campeonatos no Sofascore
campeonatos = {
    "Copa Betano do Brasil": 373,
    "Campeonato Brasileiro": 325,
    "CONMEBOL Libertadores": 70083,
}

#Divisão de colunas
col1, col2 = st.columns([1,4])

with col1:
    #Interface Streamlit
    #st.set_page_config(page_title="Previsão de Jogos", layout="wide")
    st.title("🔮 Previsão de Resultado de Jogos de Futebol")
    st.markdown("Usando dados do SofaScore em tempo real.")

    
    time_a_nome = st.selectbox("Time Mandante", list(team_ids.keys()))
    time_b_nome = st.selectbox("Time Visitante", [t for t in team_ids if t != time_a_nome])
    st.markdown(" ")



# Buscar últimos jogos via SofaScore
def buscar_ultimos_jogos_sofascore(team_id, num_jogos=5):
        url = f"https://api.sofascore.com/api/v1/team/{team_id}/events/last/0"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            st.error("Erro ao acessar dados do SofaScore.")
            return pd.DataFrame()

        eventos = response.json().get("events", [])[:num_jogos]
        jogos = []

        for evento in eventos:
            try:
                time_casa = evento["homeTeam"]["name"]
                time_fora = evento["awayTeam"]["name"]
                gols_casa = evento["homeScore"]["current"]
                gols_fora = evento["awayScore"]["current"]
                data = datetime.fromtimestamp(evento["startTimestamp"]).strftime("%d/%m/%Y")
                campeonato = evento["tournament"]["name"]

                local = "Casa" if evento["homeTeam"]["id"] == team_id else "Fora"
                adversario = time_fora if local == "Casa" else time_casa
                gols_pro = gols_casa if local == "Casa" else gols_fora
                gols_contra = gols_fora if local == "Casa" else gols_casa

                if gols_pro > gols_contra:
                    resultado = "Vitória"
                elif gols_pro < gols_contra:
                    resultado = "Derrota"
                else:
                    resultado = "Empate"

                jogos.append({
                    "Data": data,
                    "Adversário": adversario,
                    "Casa/Fora": local,
                    "Gols Pró": gols_pro,
                    "Gols Contra": gols_contra,
                    "Resultado": resultado,
                    "Campeonato": campeonato
                })
            except:
                continue

        return pd.DataFrame(jogos)

with col2:
    #Previsão de placar com base em médias
    def prever_resultado(historico_a, historico_b):
        media_gols_a = historico_a["Gols Pró"].mean()
        media_gols_b = historico_b["Gols Contra"].mean()
        media_gols_b_inv = historico_b["Gols Pró"].mean()
        media_gols_a_inv = historico_a["Gols Contra"].mean()

        gols_time_a = int(round((media_gols_a + media_gols_b_inv) / 2))
        gols_time_b = int(round((media_gols_b + media_gols_a_inv) / 2))

        if gols_time_a > gols_time_b:
            resultado = "Vitória do Mandante"
        elif gols_time_b > gols_time_a:
            resultado = "Vitória do Visitante"
        else:
            resultado = "Empate"

        return resultado, gols_time_a, gols_time_b

    #Estatísticas avançadas com gráfico Altair
    def exibir_grafico_estatisticas_avancadas(historico, nome_time):
        total_jogos = len(historico)

        mandante = historico[historico["Casa/Fora"] == "Casa"]
        visitante = historico[historico["Casa/Fora"] == "Fora"]

        def calcular_aproveitamento(df):
            vitorias = df[df["Resultado"] == "Vitória"]
            empates = df[df["Resultado"] == "Empate"]
            return round(((len(vitorias) * 3 + len(empates)) / (len(df) * 3)) * 100, 1) if len(df) > 0 else 0.0

        aproveitamento_casa = calcular_aproveitamento(mandante)
        aproveitamento_fora = calcular_aproveitamento(visitante)

        historico["Diferença de Gols"] = historico["Gols Pró"] - historico["Gols Contra"]
        media_diferenca_gols = round(historico["Diferença de Gols"].mean(), 2)

        jogos_sem_sofrer = len(historico[historico["Gols Contra"] == 0])
        jogos_sem_marcar = len(historico[historico["Gols Pró"] == 0])

        perc_sem_sofrer = round((jogos_sem_sofrer / total_jogos) * 100, 1)
        perc_sem_marcar = round((jogos_sem_marcar / total_jogos) * 100, 1)

        dados = pd.DataFrame({
            "Estatística": [
                "Aproveitamento Casa", 
                "Aproveitamento Fora", 
                "Dif. Média de Gols",
                "Sem Sofrer Gols (%)",
                "Sem Marcar Gols (%)"
            ],
            "Valor": [
                aproveitamento_casa,
                aproveitamento_fora,
                media_diferenca_gols,
                perc_sem_sofrer,
                perc_sem_marcar
            ]
        })
        
        #Legenda dos gráficos
        chart = alt.Chart(dados).mark_bar().encode(
                x=alt.X('Estatística:N', sort=None, title="Indicador"),
                y=alt.Y('Valor:Q', title="Valor (%) ou Média"),
                tooltip=["Estatística", "Valor"],
                color=alt.Color('Estatística:N', title='Estatística')
            ).properties(
                title=f"📊 Aproveitamento - {nome_time}",
                #width=600,
                height=400
            ).interactive()

        st.altair_chart(chart, use_container_width=True)

    num_jogos = st.number_input("Quantidade de jogos analisados", min_value=3, max_value=30, value=5, step=1)

    
    if time_a_nome and time_b_nome:
        with st.spinner("Buscando dados..."):
            historico_a = buscar_ultimos_jogos_sofascore(team_ids[time_a_nome], num_jogos)
            historico_b = buscar_ultimos_jogos_sofascore(team_ids[time_b_nome], num_jogos)

        
            if not historico_a.empty and not historico_b.empty:
                st.subheader("📊 Últimos jogos do Mandante")
                st.dataframe(historico_a)

                st.subheader("📊 Últimos jogos do Visitante")
                st.dataframe(historico_b)

                resultado, gols_a, gols_b = prever_resultado(historico_a, historico_b)

                st.success(f"🔮 Previsão: {resultado}")
                st.markdown(f"**Placar provável:** `{time_a_nome} {gols_a} x {gols_b} {time_b_nome}`")
            subcol1, subcol2 = st.columns(2)
            with subcol1: 
                    # Exibe gráficos avançados
                    st.subheader("📈 Estatísticas Avançadas")
                    exibir_grafico_estatisticas_avancadas(historico_a, time_a_nome)
                
            with subcol2:
                # Exibe gráficos avançados
                    st.subheader("📈 Estatísticas Avançadas")
                    exibir_grafico_estatisticas_avancadas(historico_b, time_b_nome)

#Verifica se há jogos no dia atual
def verificar_jogos_no_dia(campeonato):
    data_hoje = datetime.now(ZoneInfo("America/Sao_Paulo")).strftime('%Y-%m-%d')
    url = f"https://api.sofascore.com/api/v1/sport/football/scheduled-events/{data_hoje}"
    response = requests.get(url)

    if response.status_code != 200:
        print("Erro ao acessar a API.")
        return []

    eventos = response.json().get("events", [])
    jogos_encontrados = []

    for evento in eventos:
        liga_id = evento["tournament"]["uniqueTournament"]["id"]
        # print("ID encontrado:", evento["tournament"]["uniqueTournament"]["id"], "-", evento["tournament"]["name"])
        if liga_id == campeonato:
            time_a = evento["homeTeam"]["name"]
            time_b = evento["awayTeam"]["name"]
            horario = datetime.fromtimestamp(evento["startTimestamp"]).strftime("%H:%M")
            jogos_encontrados.append(f"{time_a} x {time_b} às {horario}")
            

    return jogos_encontrados

#Usando a API do Twilio, envia mensagem para o WhatsApp, 
#informando se há algum jogo dos campeonatos monitorados no dia atual
def enviar_mensagem_whatsapp(mensagem):
    for numero in to_whatsapp_number:
        try:
            message = client.messages.create(
                body=mensagem,
                from_=from_whatsapp_number,
                to=numero
                
            )
            print("✅ Mensagem enviada com sucesso. SID:", message.sid)
        except Exception as e:
            print("❌ Erro ao enviar mensagem:", e)

        

def main():
    mensagens = []

    for nome, id_campeonato in campeonatos.items():
        jogos = verificar_jogos_no_dia(id_campeonato)
        if jogos:
            msg = f"⚽ Hoje tem jogo(s) pelo campeonato {nome}:\n" + "\n".join(jogos)
            mensagens.append(msg)

    if mensagens:
        mensagem_final = "\n\n".join(mensagens)
        enviar_mensagem_whatsapp(mensagem_final)
    else:
        print("Nenhum jogo encontrado para os campeonatos monitorados hoje.")


if __name__ == "__main__":
    main()

