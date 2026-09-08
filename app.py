import streamlit as st
from openai import OpenAI

st.set_page_config(
    page_title="AI-assistent",
    page_icon="💬",
    layout="centered"
)

client = OpenAI(
    api_key=st.secrets["OPENAI_API_KEY"]
)

st.title("AI-assistent")
st.caption("Ställ en fråga och få hjälp av AI.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Skriv din fråga här...")

if prompt:
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        response = client.responses.create(
            model="gpt-4o-mini",
            instructions=(
                "Du är en pedagogisk AI-assistent. "
                "Svara tydligt, konkret och på svenska."
            ),
            input=st.session_state.messages
        )

        answer = response.output_text

        with st.chat_message("assistant"):
            st.markdown(answer)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

    except Exception as e:
        st.error("Något gick fel vid kontakten med OpenAI.")
        st.code(str(e))
