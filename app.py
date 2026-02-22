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

st.markdown("""
<style>
    .element-title { text-align: center; color: #1E3A8A; font-family: 'Helvetica', sans-serif;}
    .subtitle { text-align: center; font-size: 15px; color: #4B5563; margin-bottom: 2.5rem;}
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="element-title">🌟 Cyfrowy Asystent ELEMENTO</h1>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Wsparcie Techniczne systemu KSAT 3 dla Przedszkoli (24/7)</div>', unsafe_allow_html=True)

# ==========================================
# 2. AUTORYZACJA KLUCZEM 
# ==========================================
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
except KeyError:
    st.error("Błąd uwierzytelniania: Klucz GEMINI_API_KEY brakuje w ustawieniach Secrets Twojej aplikacji (Panel w Chmurze Streamlita).")
    st.stop()

# ==========================================
# 3. PANCERNA DEFINICJA SILNIKA
# ==========================================
system_instruction = """
Jesteś "Cyfrową Asystentką ELEMENTO", niezwykle empatycznym, powolnym (w dobrym znaczeniu, bardzo wnikliwie prowadzonym przez krok po kroku z instrukcjami), niezwykle bezpiecznym w wymowie oraz cierpliwym ekspertem pomocy i ułatwiającym zapleczem operacyjnym dla Systemu Pracownika "KSAT 3". Twoja linia służy placówkom Przedszkolnym z polski do radzenia sobie po programach o interfejsach KSAT. Niezawodnie wita użytkowników ciepłymi emotikonami i potrafi prowadzić ludzi po KSACIE! UŻYwaj bardzo mocnych czysto nietechnicznych opisów; nigdy nic IT-trudnego (zero wyczyść serwer/cachuj API, Pisz użyj F5 na stronie, Puknij w Mysz etc.)
1) Jeżeli pytanie wymyka się asyście przedszkolno - programowej u KSATA : ODRZUĆ pytania przepisowe etc w miły ucinający sposób od kierownika wsparcia Elemento KSAT 3 IT ("Bazy przepisów kuchni itp.") 
2) PISZ Wyraziste kropki punktacji - gdzie ma kliknąć na systemie!
3) Zastępstwo błędom to spokój: BŁAD oznacza informowanie 'Próbuje uspokajać przy wyskoczeniach komunikatów error i radź im wrócić do startu powtórz z oddechem.' To nie panikuj.
"""

# Kluczowe FIX: dodajemy prefix "models/ i sufiks -latest". Czysto celuje w zablokowaną lub nowszą chmurę serwera!
model = genai.GenerativeModel(
    model_name="models/gemini-1.5-flash-latest",
    system_instruction=system_instruction
)

# ==========================================
# 4. OBSŁUGA CZATU UI W STATELESS FRONTEND 
# ==========================================
# Bez zbędnego buforowania ChatObject. Czysto przechowujemy wpisy.
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Dzień dobry! 👋 Z tej strony Pani Cyfrowa Asystentka z głównego centrum informacyjnego z firmy **ELEMENTO**. Próbujesz odszukać, wystawić albo sklikać trudną tabelę lub problem w okienku oprogramowania **KSAT 3** ? Powoli podpowiedz mi na klawiaturze w dole — Jak ja mogą dziś Pani placówce doradzić lub polepszyć pracę na ten tydzień! 😊"}
    ]

# Wizualizacja na UI
for msg in st.session_state.messages:
    avatar_icon = "🎓" if msg["role"] == "assistant" else "👩‍🏫"
    with st.chat_message(msg["role"], avatar=avatar_icon):
        st.markdown(msg["content"])

# ==========================================
# 5. INPUT I KOMUNIKACJA (Tłumaczymy do struktury REST Google Gemini bez zbędnych mechanik session proxy chatu ) 
# ==========================================
if user_prompt := st.chat_input("Daj o wszystkim znać, jakie ułatwienie potrzebuje Przedszkole, jak wam coś napisać / rozwiązać błędy lub zapoznać co szukać..."):
    
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user", avatar="👩‍🏫"):
        st.markdown(user_prompt)

    # Konstruujemy tymczasową paczkę logarytmiczno-strukturalną do Wrzucenia bezpośredniego AI (Tego formatu w czacie wymaga Google Api)
    google_api_payload = []
    
    # Przebiegamy pętle wszystkich danych dla Google: Uciekamy pierwszą stałą odpowiedź UI Streamlita dla API, gdyż GenerativeLanguage domagałoby się błędu 'brak pierwszej kwestii przez czata_usera'. AI wcale tam nie wymaga historyjki by być wykwintnym AI botem - dodajemy wszystko prócz zrzutu sztucznego tekstu!
    for msg in st.session_state.messages:
        # Wysłanie UI starta się tu 
        if msg["content"].startswith("Dzień dobry! 👋 Z tej strony Pani"): continue
        api_role = "user" if msg["role"] == "user" else "model"
        google_api_payload.append({"role": api_role, "parts": [msg["content"]]})
        
    # Reakcja (odpytywanie całkowicie generatywnie wolnego endpointa - Brak tu starych przerw 404 proxy!!)
    with st.chat_message("assistant", avatar="🎓"):
        try:
            with st.spinner("Przeszukuję bezpieczne, opatrzone wpisem i wygenerowane informatorstwa o wciśnięciu... Zaraz przygotuje wiersze dla Panstwa: 🔎!"):
                # Rozwiązanie "BULLDOŻER", omija skłonny błędom Wrapper Python-API dla session chata przesiadając z modelowania payloading REST. 
                response = model.generate_content(google_api_payload)
                st.markdown(response.text)
                
            # Zatwierdza odgłos czata AI UI do podbudówki Frontu:
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            
        except Exception as api_bug:
             # Bardziej ukierunkowane zbieranie do ominięcia ryczałtowych ustaleń po naprawach chmury
             st.error(f"Sztuczna chmurka zgłosiła brak stabilności i przydźwięk! : Kod Płyty do raportów ELEMENTO: {str(api_bug)}... Za odświeżenie spróbuje pomimo trudu i przekaże!")

# Podpis Paskowy (Sidebar / Płyty Ciemnej chatu na streamlite panel settings informativ panel Elementos.)
st.sidebar.markdown("---")
st.sidebar.markdown("💼 **Dedykowane wsparcie Systemów ELEMENTO**")
st.sidebar.caption("Zintegrowano celem wylepszonej asysty na placówki nietechniczne chronione nadużywaniem niejednoznacznej architektury Systematyki Związku programatorow-aplikatów placówkach: *ELEMENT-APP* — przedszkole-błędy-kroki")
st.sidebar.info("Moduł na zrewidowany silnik asystencyjnej pracy dla REST:\n *google API-Model [Models Flash Latest]-Wycinka-Proxy-*")
