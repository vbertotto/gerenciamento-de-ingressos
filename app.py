import streamlit as st
import qrcode
import pandas as pd
import uuid
from PIL import Image
from io import BytesIO

st.set_page_config(page_title="Sistema de Emissão de Tickets com QR Code", layout="centered")
st.title("Sistema de Emissão de Tickets com QR Code")
st.write("Preencha o formulário abaixo para emitir um ticket.")

with st.form("form_ticket"):
    nome = st.text_input("Nome Completo", max_chars=50, placeholder="Digite seu nome completo")
    email = st.text_input("E-mail", max_chars=50, placeholder="Digite seu e-mail")
    evento = st.text_input("Evento", max_chars=100, placeholder="Nome do evento")
    quantidade = st.number_input("Quantidade de Tickets", min_value=1, max_value=10, value=1, step=1)
    submit = st.form_submit_button("Emitir Ticket")

if submit:
    if nome and email and evento:
        for _ in range(int(quantidade)):
            ticket_id = str(uuid.uuid4())
            ticket_data = {
                "ID": ticket_id,
                "Nome": nome,
                "E-mail": email,
                "Evento": evento
            }
            
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(ticket_id)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            
            buf = BytesIO()
            img.save(buf, format="PNG")
            byte_im = buf.getvalue()
            
            st.success("Ticket emitido com sucesso!")
            st.markdown(f"**Nome:** {nome}")
            st.markdown(f"**E-mail:** {email}")
            st.markdown(f"**Evento:** {evento}")
            st.markdown(f"**ID do Ticket:** {ticket_id}")
            st.image(byte_im, caption='QR Code do Ticket', use_column_width=True)
            
            st.download_button(
                label="Baixar QR Code",
                data=byte_im,
                file_name=f"ticket_{ticket_id}.png",
                mime="image/png",
            )
            
            try:
                df = pd.read_csv("tickets_emitidos.csv")
            except FileNotFoundError:
                df = pd.DataFrame(columns=["ID", "Nome", "E-mail", "Evento"])
            
            df = df.append(ticket_data, ignore_index=True)
            df.to_csv("tickets_emitidos.csv", index=False)
    else:
        st.error("Por favor, preencha todos os campos.")

st.header("Tickets Emitidos")

try:
    df = pd.read_csv("tickets_emitidos.csv")
    st.dataframe(df)
except FileNotFoundError:
    st.write("Nenhum ticket emitido ainda.")
