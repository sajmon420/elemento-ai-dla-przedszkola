import streamlit as st
import google.generativeai as genai

# ==========================================
# 1. KONFIGURACJA STRONY I BRANDINGU
# ==========================================
st.set_page_config(
    page_title="Asystent ELEMENTO | Wsparcie KSAT 3",
    page_icon="🎓",
    layout="centered"
)

# Customowy CSS (drobny lifting, aby aplikacja wyglądała jeszcze bardziej profesjonalnie)
st.markdown("""
<style>
    .element-title { text-align: center; color: #1E3A8A; }
    .subtitle { text-align: center; font-size: 14px; color: #4B5563; margin-bottom: 2rem;}
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="element-title">🌟 Cyfrowy Asystent ELEMENTO</h1>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Wsparcie Techniczne systemu KSAT 3 dla Przedszkoli (24/7)</div>', unsafe_allow_html=True)

# ==========================================
# 2. AUTORYZACJA BARDZO BEZPIECZNA (ST.SECRETS)
# ==========================================
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
except KeyError:
    st.error("Błąd: Nie znaleziono klucza API. Upewnij się, że dodałeś sekrety (st.secrets).")
    st.stop()

# ==========================================
# 3. SYSTEM PROMPT - PERSONALITY & LOGIC
# ==========================================
system_instruction = """
Jesteś "Cyfrową Asystentką ELEMENTO", cierpliwym wsparciem technicznym dla placówek przedszkolnych obsługujących system KSAT 3. 
ZASADY:
1. Bądź empatyczna i wyrozumiała ("Cierpliwa Ekspertka"). Uspokajaj w razie błędów.
2. Zero żargonu IT (np. zamiast 'wyczyść cache' -> 'odśwież stronę przyciskiem F5').
3. Dawaj instrukcje w krótkich krokach 1, 2, 3...
4. Pogrubiaj ważne zakładki, w które należy kliknąć.
5. Służysz TYLKO do pomocy przy KSAT 3. Grzecznie odmawiaj (guardrails), gdy ktoś prosi o inne rzeczy np. przepisy, żarty.
"""

# Konfiguracja modelu gemini-1.5-flash z instrukcją systemową
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=system_instruction
)

# ==========================================
# 4. OBSŁUGA CZATU (STATE MANAGEMENT)
# ==========================================
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

if "messages" not in st.session_state:
    # Pierwsza wiadomość, która jest zachętą do używania czatu
    st.session_state.messages = [
        {"role": "model", "content": "Dzień dobry! Z tej strony Pani Cyfrowa Asystentka z zespołu ELEMENTO. Jak mogę dzisiaj Pani pomóc w systemie KSAT 3? Proszę pytać śmiało, chętnie odpowiem na każde pytanie!"}
    ]

# Renderowanie dotychczasowej rozmowy na ekranie (Chat Elements)
for msg in st.session_state.messages:
    # Zmieniamy ikonę w zależności od tego kto mówi (Użytkownik - Człowiek, Model - Elemento)
    avatar_icon = "🎓" if msg["role"] == "model" else "👩‍🏫"
    with st.chat_message(msg["role"], avatar=avatar_icon):
        st.markdown(msg["content"])

# ==========================================
# 5. POLE TEKSTOWE NA PYTANIE (USER INPUT)
# ==========================================
if user_prompt := st.chat_input("Wpisz swoje pytanie dotyczące KSAT 3 tutaj..."):
    # Zapis i wyświetlenie wiadomości użytkowniczki
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user", avatar="👩‍🏫"):
        st.markdown(user_prompt)

    # Reakcja modelu (streaming, żeby aplikacja wydawała się szybsza)
    with st.chat_message("model", avatar="🎓"):
        with st.spinner("Szukam odpowiedzi..."):
            response = st.session_state.chat.send_message(user_prompt)
            st.markdown(response.text)
    
    # Zapisanie wiadomości zwrotnej od AI
    st.session_state.messages.append({"role": "model", "content": response.text})

# Podpis firmowy
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/c/ca/1x1.png", width=1) # Usunięto błędy - używamy st.markdown z logo lub pustą przestrzeń w sidebar.
st.sidebar.markdown("---")
st.sidebar.markdown("💼 **Cyfrowe Wsparcie ELEMENTO**")
st.sidebar.markdown("💡 Projekt prototypowy na wyłączność przedszkoli używających systemu **KSAT 3**.")
st.sidebar.info("Model: Gemini-1.5-Flash \n (Fast & Secure Text Gen)")