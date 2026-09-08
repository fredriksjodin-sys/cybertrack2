import streamlit as st
from openai import OpenAI

st.set_page_config(
    page_title="AI-assistent",
    page_icon="💬",
    layout="centered"
)

# Hämta API-nyckeln från Streamlit Secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Sidans rubrik
st.title("AI-assistent")
st.caption("Ställ en fråga och få hjälp av AI.")

# Initiera chatthistorik
if "messages" not in st.session_state:
    st.session_state.messages = []

# Visa tidigare meddelanden
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat-input
prompt = st.chat_input("Skriv din fråga här...")

if prompt:
    # Spara och visa användarens fråga
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    # Bygg konversationen som text till modellen
    conversation = []

    for message in st.session_state.messages:
        conversation.append(
            {
                "role": message["role"],
                "content": message["content"]
            }
        )

    try:
        with st.chat_message("assistant"):
            with st.spinner("AI:n tänker..."):

                response = client.responses.create(
                    model="gpt-5",
                    instructions="""
                    Du är en pedagogisk AI-assistent.
                    Svara tydligt, konkret och på svenska.
                    Anpassa nivån efter användarens fråga.
                    """,
                    input=conversation
                )

                answer = response.output_text

                st.markdown(answer)

        # Spara svaret
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

    except Exception as e:
        st.error("Något gick fel vid kontakten med AI-tjänsten.")
        st.code(str(e))
