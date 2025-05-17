import os 
from dotenv import load_dotenv
from google import genai
from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.tools import google_search
from google.genai import types  # Para criar conteúdos (Content e Part)
import warnings
import streamlit as st # Para interface 

warnings.filterwarnings("ignore")

# Carrega a chave da API do arquivo .env
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

client = genai.Client()
MODEL_ID = "gemini-2.0-flash"


def call_agent(agent: Agent, message_text: str) -> str:
    
    session_service = InMemorySessionService()
    session = session_service.create_session(app_name=agent.name, user_id="user1", session_id="session1")
    runner = Runner(agent=agent, app_name=agent.name, session_service=session_service)
    content = types.Content(role="user", parts=[types.Part(text=message_text)])
    final_response = ""
    
    for event in runner.run(user_id="user1", session_id="session1", new_message=content):
        if event.is_final_response():
          for part in event.content.parts:
            if part.text is not None:
              final_response += part.text
              final_response += "\n"
    return final_response


## Agente 

def marIA_service(assunto):
    pesquisadora_marIA = Agent(
        name="agente_pesquisador",
        model=MODEL_ID,
        description="Agente para facilitar o acesso a informações e serviços públicos",
        tools=[google_search],
        instruction="""
            Você é uma assistente virtual criada para ajudar pessoas mais velhas a entender e acessar serviços públicos do governo brasileiro. Muitas dessas pessoas não têm familiaridade com a internet, nem com tecnologia, nem com termos jurídicos complexos.
            Sua missão é explicar tudo de forma simples, direta e respeitosa, usando uma linguagem acessível, com exemplos práticos e, sempre que possível, guiando passo a passo. Evite siglas, jargões técnicos ou respostas muito curtas.
            Seja sempre paciente, educado e encorajador. Seu papel é facilitar a vida dessas pessoas, promovendo confiança, autonomia e clareza.
        """
    )

    entrada_marIA = f"Assunto: {assunto}\n"
    pesquisas = call_agent(pesquisadora_marIA, entrada_marIA)
    return pesquisas   


st.set_page_config(page_title="marIA - Assistente Pública", page_icon="🤖")

st.markdown(
    '''
    <a href="https://github.com/eduardaguardiao" target="_blank" style="text-decoration: none;">
        <img src="https://img.icons8.com/ios11/512/FFFFFF/github.png" width="30" />
    </a>

    <a href="https://www.linkedin.com/in/maria-eduarda-guardi%C3%A3o-504761286/" target="_blank">
        <img src="https://static.vecteezy.com/system/resources/previews/018/930/480/non_2x/linkedin-logo-linkedin-icon-transparent-free-png.png" width="45" />
    </a>
    ''',
    unsafe_allow_html=True
)

st.markdown("""
# 🤖 marIA — Sua assistente de serviços públicos

Olá! Sou a marIA, uma ajudante virtual feita especialmente para te ajudar a entender documentos, direitos e serviços públicos do Brasil com clareza e simplicidade. ✨
""")

pergunta = st.text_input("Digite sua dúvida aqui:")

if pergunta:
    with st.spinner("Buscando resposta..."):
        resposta = marIA_service(pergunta)
        st.markdown("### 📝 Resposta da marIA:")
        st.write(resposta)