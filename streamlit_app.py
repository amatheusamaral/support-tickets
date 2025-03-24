import datetime
import random
import altair as alt
import numpy as np
import pandas as pd
import streamlit as st

# Configuração do título e descrição do app.
st.set_page_config(page_title="Tickets de Suporte", page_icon="🎫")
st.title("🎫 Tickets de Suporte")
st.write(
    """
Bem-vindo ao Sistema de Tickets de Suporte de TI!

Registre problemas, acompanhe solicitações e ajude a equipe de TI a resolver demandas com mais agilidade.
    """
)

# Inicializando dataframe vazio para armazenar os tickets.
if "df" not in st.session_state:
    df = pd.DataFrame(columns=["ID", "Problema", "Status", "Prioridade", "Data de Submissão"])
    st.session_state.df = df

# Exibindo a seção para adicionar um novo ticket.
st.header("Adicionar um ticket")

# Formulário para adicionar tickets.
with st.form("form_add_ticket"):
    problema = st.text_area("Descreva o problema")
    prioridade = st.selectbox("Prioridade", ["Alta", "Média", "Baixa"])
    enviado = st.form_submit_button("Enviar")

if enviado:
    # Criando um novo ID de ticket.
    numero_ticket_recente = 1001 if st.session_state.df.empty else int(max(st.session_state.df.ID).split("-")[1]) + 1
    hoje = datetime.datetime.now().strftime("%d-%m-%Y")
    df_novo = pd.DataFrame(
        [
            {
                "ID": f"TICKET-{numero_ticket_recente}",
                "Problema": problema,
                "Status": "Aberto",
                "Prioridade": prioridade,
                "Data de Submissão": hoje,
            }
        ]
    )

    # Atualizando o dataframe da sessão.
    st.session_state.df = pd.concat([df_novo, st.session_state.df], axis=0, ignore_index=True)
    st.write("Ticket enviado! Aqui estão os detalhes do ticket:")
    st.dataframe(df_novo, use_container_width=True, hide_index=True)

# Lógica de autenticação para visualizar gráficos e editar tickets.
senha = st.text_input("Digite a senha para visualizar as estatísticas e editar tickets", type="password")
if senha == "Seca3993":  # Senha definida como Seca3993
    # Exibindo a seção para visualizar e editar os tickets existentes.
    st.header("Tickets Existentes")
    st.write(f"Número de tickets: `{len(st.session_state.df)}`")

    st.info(
        "Você pode editar os tickets clicando duas vezes em uma célula. Observe como os gráficos abaixo "
        "são atualizados automaticamente! Você também pode classificar a tabela clicando nos cabeçalhos das colunas.",
        icon="✍️",
    )

    # Exibindo os tickets em uma tabela editável.
    df_editado = st.data_editor(
        st.session_state.df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Status": st.column_config.SelectboxColumn(
                "Status",
                help="Status do ticket",
                options=["Aberto", "Em Progresso", "Fechado"],
                required=True,
            ),
            "Prioridade": st.column_config.SelectboxColumn(
                "Prioridade",
                help="Prioridade",
                options=["Alta", "Média", "Baixa"],
                required=True,
            ),
        },
        disabled=["ID", "Data de Submissão"],
    )

    # Exibindo métricas e gráficos sobre os tickets.
    st.header("Estatísticas")

    col1, col2, col3 = st.columns(3)
    num_tickets_abertos = len(st.session_state.df[st.session_state.df.Status == "Aberto"])
    col1.metric(label="Número de tickets abertos", value=num_tickets_abertos, delta=10)
    col2.metric(label="Tempo de primeira resposta (horas)", value=5.2, delta=-1.5)
    col3.metric(label="Tempo médio de resolução (horas)", value=16, delta=2)

    # Exibindo gráficos do Altair.
    st.write("##### Status dos tickets por mês")
    grafico_status = (
        alt.Chart(df_editado)
        .mark_bar()
        .encode(
            x="month(Data de Submissão):O",
            y="count():Q",
            xOffset="Status:N",
            color="Status:N",
        )
        .configure_legend(
            orient="bottom", titleFontSize=14, labelFontSize=14, titlePadding=5
        )
    )
    st.altair_chart(grafico_status, use_container_width=True, theme="streamlit")

    st.write("##### Prioridades dos tickets atuais")
    grafico_prioridade = (
        alt.Chart(df_editado)
        .mark_arc()
        .encode(theta="count():Q", color="Prioridade:N")
        .properties(height=300)
        .configure_legend(
            orient="bottom", titleFontSize=14, labelFontSize=14, titlePadding=5
        )
    )
    st.altair_chart(grafico_prioridade, use_container_width=True, theme="streamlit")

else:
    st.write("Digite a senha para acessar as seções restritas.")
