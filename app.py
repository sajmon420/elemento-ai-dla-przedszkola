import streamlit as st
pip install -q -U google-genai
from google import genai

# The client gets the API key from the environment variable `GEMINI_API_KEY`.
client = genai.Client()

response = client.models.generate_content(
    model="gemini-3-flash-preview", contents="Explain how AI works in a few words"
)
print(response.text)
import google.generativeai as genai
from google.api_core.exceptions import NotFound, InvalidArgument

# ==========================================
# 1. KONFIGURACJA STRONY I BRANDINGU
# ==========================================
st.set_page_config(
    page_title="Asystent ELEMENTO | Wsparcie KSAT 3",
    page_icon="🎓",
    layout="centered"
)

st.markdown("""
<style>
    .element-title { text-align: center; color: #1E3A8A; font-family: 'Helvetica', sans-serif;}
    .subtitle { text-align: center; font-size: 15px; color: #4B5563; margin-bottom: 2.5rem;}
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="element-title">🌟 Cyfrowy Asystent ELEMENTO</h1>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Wsparcie Techniczne systemu KSAT 3 dla Przedszkoli (24/7)</div>', unsafe_allow_html=True)

# ==========================================
# 2. AUTORYZACJA BARDZO BEZPIECZNA
# ==========================================
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
except KeyError:
    st.error("Błąd: Nie znaleziono klucza API w środowisku chmurowym. Sprawdź opcje (Streamlit settings > Secrets).")
    st.stop()

# ==========================================
# 3. SYSTEM PROMPT (Logika / Rola AI)
# ==========================================
system_instruction = """
Jesteś "Cyfrową Asystentką ELEMENTO", cierpliwym wsparciem technicznym dla placówek przedszkolnych obsługujących system KSAT 3. 
ZASADY:
1. Bądź empatyczna, uprzejma ("Cierpliwa Ekspertka") i niezwykle ciepła.
2. ZAWSZE Uspokajaj w razie błędów w oprogramowaniu i zapewniaj z uśmiechem, że zaraz naprawimy ten mały problem.
3. Absolutny brak żargonu IT. Bądź wyrazista: podawaj jasne krok 1., krok 2., krok 3. zamiast np. potoku trudnych technicznych zdań.
4. Używaj Pogrubień (**Opcja X**) do nazw funkcji i elementów interfejsu (żeby było je wyraźnie widać na ekranie programu ksat 3).
5. POMAGASZ TYLKO W ZAKRESIE ELEMENTO / KSAT 3!
"""

# Zainicjalizowanie najstabilniejszej opcji Modelu API dla Streamlit w Europie / wersji AI Studio 
# Dodajemy model jako funkcję ładowaną po wywołaniu. (gemini-1.5-flash)
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=system_instruction
)

# ==========================================
# 4. START i STATE CZATU Z RĘCZNYM ZAPISEM (Ominięcie Problemów ze zgubieniem Modelu przez RAM streamlita)
# ==========================================
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "model", "content": "Dzień dobry! 👋 Z tej strony Pani Cyfrowa Asystentka wsparcia systemu przedszkolnego **ELEMENTO**.\nJak mogę dzisiaj pomóc, by ułatwić Pani dzień na KSAT 3?"}
    ]

# Mechanizm Streamlit do malowania całego okna rozmowy. 
for msg in st.session_state.messages:
    avatar_icon = "🎓" if msg["role"] == "model" else "👩‍🏫"
    with st.chat_message(msg["role"], avatar=avatar_icon):
        st.markdown(msg["content"])

# ==========================================
# 5. POLE PYTANIA: INPUT FRONTEND-Backend.
# ==========================================
if user_prompt := st.chat_input("Proszę wpisać treść lub zadanie (W czym doradzić)..."):
    
    # Krok a) pokazanie użytkownikowi swojego wysłanego textu z dymkiem człowieka "Kluczowym Frontend"
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user", avatar="👩‍🏫"):
        st.markdown(user_prompt)

    # Krok b) Model procesujący + Pancerne Przechwytywanie ERROR-logów by w ostateczności pomóc debuggowi:
    with st.chat_message("model", avatar="🎓"):
        try:
            with st.spinner("Cyfrowa asystentka Elemento analizuje odpowiedź dla Pani placówki, prosimy sekundę odczekać..."):
                response = st.session_state.chat.send_message(user_prompt)
                st.markdown(response.text)
                
            st.session_state.messages.append({"role": "model", "content": response.text})

        # ZŁAPANIE TYPOWEGO BŁĘDU, BY NIE POPSUĆ KLIENTOWI PROGRAMU CHMURY A PODRZUCIĆ WYJAŚNIENIE: 
        except NotFound:
            # Reaguje jeśli dany Region Projektu Google AI nie miał dostępu do gemini-1.5 i rzucił log "404 Not Found API route".
            st.error("""
            **Komunikat wewnętrzny - Tryb Diagnozy IT**
            Nasz Model poinformował chmurę o błędzie *BrakDostępuDoEndpointu/NotFound*. W systemie Gemini API Studio mogły zaciąć się parametry `generate_content`. 
            Upewnij się czy Twój wygenerowany *Klucz Google API Studio (w settings cloudach Streamlit > Secrets)*, faktycznie wspiera model: `gemini-1.5-flash` w udostępnionych Regionach i czy podłączyłeś go poprawnie do rachunków w "Platform Console Google". 
            Wróć po restarcie lub spróbuj za parę minut ponownie odświeżając system przyciskiem w panelu "Clear cache" albo F5.
            """)
        except Exception as general_err:
             st.error(f"⚠️ Asystentka z zamyśleniem odrzuciła podane pakiety bazy danych! Kod błędu: \n`{str(general_err)}`\n(Dajcie mu sekundę i napiszcie swoje pytani raz jeszcze)")

# Prawa sekcja (Estetyczny panel z informacją wspierania przedszkola 02 - opcja z usunięciem wbudowanego sidebar na biało dla lżejszego view)
st.sidebar.markdown("---")
st.sidebar.markdown("💼 **Dedykowane wsparcie Systemów ELEMENTO**")
st.sidebar.caption("💡 Z myślą o nietechnicznej ochronie i ulepszonym bezpieczeństwu wszystkich zgromadzonych pracowniczek opartych i korzystających ze śladów **oprogramowania placówek KSAT3**!")
st.sidebar.info("Moduł bazujący silnik API: *Google Generative v-1.5Flash-Stable-Tech*.")
