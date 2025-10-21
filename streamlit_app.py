import streamlit as st
from openai import OpenAI

# Titel und Beschreibung
st.title("💬 Chatbot mit OpenAI Assistant")
st.write(
    "Dieser Chatbot verwendet deinen eigenen Assistant aus der OpenAI Assistants API. "
    "Gib unten deinen OpenAI API-Key ein, um loszulegen."
)

# Nutzer nach API-Key fragen
openai_api_key = st.text_input("🔑 OpenAI API Key", type="password")

if not openai_api_key:
    st.info("Bitte gib deinen OpenAI API-Key ein, um fortzufahren.", icon="🗝️")
else:
    # Assistant-ID (dein gespeicherter Assistant)
    ASSISTANT_ID = "asst_NIVJXokSYcboqteCloJiJesL"

    # OpenAI-Client erstellen
    client = OpenAI(api_key=openai_api_key)

    # Chat-Verlauf in Session speichern
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Vorherige Nachrichten anzeigen
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Eingabefeld für neue Nachricht
    if prompt := st.chat_input("Schreib deine Nachricht..."):

        # Nutzer-Nachricht speichern und anzeigen
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Thread erstellen (für Assistant-Run)
        thread = client.beta.threads.create(
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        # Assistant-Run starten
        with st.chat_message("assistant"):
            with st.spinner("Der Assistant denkt nach... 🤔"):
                run = client.beta.threads.runs.create_and_poll(
                    thread_id=thread.id,
                    assistant_id=ASSISTANT_ID,
                )

                if run.status == "completed":
                    messages = client.beta.threads.messages.list(thread_id=thread.id)
                    response = messages.data[0].content[0].text.value
                else:
                    response = f"❌ Fehler: Assistant-Run fehlgeschlagen (Status: {run.status})"

                st.markdown(response)

        # Antwort speichern
        st.session_state.messages.append({"role": "assistant", "content": response})
