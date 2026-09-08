import streamlit as st
from openai import OpenAI

st.set_page_config(
    page_title="Cybertrack - Intervjusimulator",
    page_icon="💬",
    layout="centered"
)

# OpenAI-klient med nyckeln från Streamlit Secrets
client = OpenAI(
    api_key=st.secrets["OPENAI_API_KEY"]
)

st.title("Cybertrack - Fas 1")
st.subheader("Intervjusimulator")

st.write(
    "Ni kan nu genomföra era intervjuer på Cybertrack. "
    "Välj person och börja sedan ställa era frågor."
)

# Intervjupersoner
characters = [
    "Harriet - VD och grundare",
    "Erik - CTO",
    "Anna - HR-chef",
    "Maria - Supportansvarig",
    "Lars - Senior utvecklare",
    "Sofia - Microsoft representant"
]

selected_character = st.selectbox(
    "Vem vill ni intervjua?",
    characters
)

st.info(f"Ni intervjuar nu: **{selected_character}**")

# En separat chatthistorik för varje person
history_key = f"messages_{selected_character}"

if history_key not in st.session_state:
    st.session_state[history_key] = []

messages = st.session_state[history_key]

# Visa tidigare meddelanden
for message in messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input(
    f"Ställ en fråga till {selected_character.split(' - ')[0]}..."
)

if prompt:

    messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        with st.chat_message("assistant"):
            with st.spinner("Svarar..."):

                # Lägg till vald intervjuperson i frågan
                api_input = []

                api_input.append(
                    {
                        "role": "user",
                        "content": (
                            f"Den valda intervjupersonen är "
                            f"{selected_character}. "
                            f"Gå nu in i den personens roll och stanna i rollen."
                        )
                    }
                )

                # Lägg till hela intervjuhistoriken
                for message in messages:
                    api_input.append(
                        {
                            "role": message["role"],
                            "content": message["content"]
                        }
                    )

                response = client.responses.create(
                    prompt={
                        "id": "pmpt_6aa00a7b6d048196b91c2db47b807b13079fd38462b57511",
                        "version": "2"
                    },
                    input=api_input,
                    tools=[
                        {
                            "type": "file_search",
                            "vector_store_ids": [
                                "vs_6aa014cf41c88191a26837f7e0c26dc0"
                            ]
                        }
                    ],
                    max_output_tokens=2048,
                    store=True
                )

                answer = response.output_text

                st.markdown(answer)

        messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

    except Exception as e:
        st.error("Något gick fel vid kontakten med OpenAI.")
        st.code(str(e))

st.divider()

if st.button("Rensa intervjun med denna person"):
    st.session_state[history_key] = []
    st.rerun()
