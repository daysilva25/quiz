import streamlit as st
import time
import threading
from io import BytesIO
from urllib.parse import quote

# ==============================================================================
# QUIZ DE FIXAÇÃO: SERIGRAFIA & ROTOGRAVURA (SENAI)
# Desenvolvido por Daiane Silva
# Estilo Kahoot: telão com QR Code, perguntas sincronizadas e pontos por agilidade
#
# COMO USAR:
#   Alunos (celular):  https://SEU-APP.streamlit.app
#   Telão (apresentador): https://SEU-APP.streamlit.app/?modo=telao   (pede o PIN)
# Requer: streamlit >= 1.37   (opcional: qrcode[pil] para gerar o QR localmente)
# ==============================================================================

PIN_APRESENTADOR = "2026"          # PIN para abrir o telão (não aparece mais na tela)
TEMPO_LIMITE = 25                  # segundos por pergunta
BONUS_PRIMEIROS = [300, 200, 100]  # bônus para o 1º, 2º e 3º que acertarem (use [] para desligar)

IS_TELAO = st.query_params.get("modo") == "telao"

st.set_page_config(
    page_title="Quiz de Fixação • Serigrafia & Rotogravura",
    page_icon="🎨",
    layout="wide" if IS_TELAO else "centered",
    initial_sidebar_state="collapsed",
)

# --- TEMA CLARO E LEGÍVEL ---
st.markdown("""
<style>
    html, body, [data-testid="stAppViewContainer"], .stApp, main {
        background-color: #F8FAFC !important;
        color: #0F172A !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
    }
    [data-testid="stHeader"] { background-color: #F8FAFC !important; }
    [data-testid="stSidebar"], [data-testid="collapsedControl"] { display: none !important; }

    h1, h2, h3, h4, [data-testid="stMarkdownContainer"] h1, [data-testid="stMarkdownContainer"] h2,
    [data-testid="stMarkdownContainer"] h3 {
        color: #0F172A !important; font-weight: 800 !important; letter-spacing: -0.5px !important;
    }
    p, label, [data-testid="stMarkdownContainer"] p { color: #1E293B !important; }

    .white-card {
        background-color: #FFFFFF !important; border: 2px solid #E2E8F0 !important;
        border-radius: 18px !important; padding: 1.5rem !important; margin-bottom: 1.25rem !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.04) !important;
    }
    .theme-badge {
        background-color: #EDE9FE !important; border: 1px solid #DDD6FE !important; color: #6D28D9 !important;
        padding: 0.35rem 0.9rem !important; border-radius: 9999px !important; font-size: 0.85rem !important;
        font-weight: 700 !important; display: inline-block !important; margin-bottom: 0.5rem !important;
    }

    .stButton > button, [data-testid="stFormSubmitButton"] > button {
        background-color: #FFFFFF !important; border: 2px solid #CBD5E1 !important; border-radius: 14px !important;
        padding: 1rem 1.25rem !important; min-height: 58px !important; text-align: left !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04) !important; transition: all 0.2s ease !important; width: 100% !important;
    }
    .stButton > button:hover, [data-testid="stFormSubmitButton"] > button:hover {
        background-color: #F1F5F9 !important; border-color: #7C3AED !important; transform: translateY(-2px) !important;
    }
    .stButton > button p, .stButton > button div, .stButton > button span,
    [data-testid="stFormSubmitButton"] > button p {
        color: #0F172A !important; font-size: 1.15rem !important; font-weight: 700 !important;
        line-height: 1.4 !important; text-align: left !important;
    }
    .stButton > button[kind="primary"], [data-testid="stFormSubmitButton"] > button[kind="primaryFormSubmit"],
    [data-testid="stFormSubmitButton"] > button[kind="primary"] {
        background: linear-gradient(135deg, #7C3AED 0%, #6D28D9 100%) !important; border: none !important;
        box-shadow: 0 4px 15px rgba(124, 58, 237, 0.3) !important;
    }
    .stButton > button[kind="primary"] p, [data-testid="stFormSubmitButton"] > button[kind="primaryFormSubmit"] p,
    [data-testid="stFormSubmitButton"] > button[kind="primary"] p {
        color: #FFFFFF !important; font-weight: 800 !important; text-align: center !important;
    }

    [data-baseweb="input"], input {
        background-color: #FFFFFF !important; color: #0F172A !important; border: 2px solid #CBD5E1 !important;
        border-radius: 12px !important; font-size: 1.1rem !important; font-weight: 600 !important;
    }

    .podium-box {
        background: #FFFFFF !important; border: 2px solid #E2E8F0 !important; border-radius: 16px !important;
        padding: 1.2rem !important; text-align: center !important; box-shadow: 0 6px 18px rgba(0,0,0,0.06) !important;
    }
    .podium-gold { border-top: 8px solid #F59E0B !important; }
    .podium-silver { border-top: 8px solid #94A3B8 !important; }
    .podium-bronze { border-top: 8px solid #FB923C !important; }

    .dev-signature {
        text-align: center !important; font-size: 0.82rem !important; color: #94A3B8 !important;
        margin-top: 2.5rem !important; padding-top: 1rem !important; border-top: 1px solid #E2E8F0 !important;
        font-weight: 600 !important;
    }
</style>
""", unsafe_allow_html=True)

# --- 5 PERGUNTAS OFICIAIS (SENAI) ---
QUESTIONS = [
    {
        "theme": "Serigrafia",
        "question": "Como funciona o processo de impressão serigráfica?",
        "options": [
            "A tinta é transferida por meio de um cilindro com cavidades gravadas.",
            "A tinta atravessa as áreas abertas de uma tela por meio de um rodo.",
            "A imagem é impressa exclusivamente por jatos de tinta.",
            "A impressão acontece por meio de chapas de metal aquecidas.",
        ],
        "correct": 1,
        "explanation": "Na serigrafia, a tinta atravessa as aberturas da tela tensionada pela pressão do rodo, transferindo a imagem para o material!",
    },
    {
        "theme": "Serigrafia",
        "question": "Qual dos materiais abaixo pode receber impressão por serigrafia?",
        "options": [
            "Apenas papel.",
            "Apenas tecidos.",
            "Tecidos, papel, vidro e plástico.",
            "Somente materiais metálicos.",
        ],
        "correct": 2,
        "explanation": "A serigrafia é muito versátil e permite estampar tecidos, papéis, plásticos, vidros, madeiras, canecas e brindes!",
    },
    {
        "theme": "Rotogravura",
        "question": "Qual elemento é utilizado na rotogravura para transferir a tinta ao material?",
        "options": [
            "Uma tela de nylon.",
            "Um carimbo de borracha.",
            "Uma chapa de madeira.",
            "Um cilindro com pequenas cavidades gravadas.",
        ],
        "correct": 3,
        "explanation": "A rotogravura utiliza cilindros metálicos gravados com microcavidades (alvéolos em baixo-relevo) que retêm e transferem a tinta.",
    },
    {
        "theme": "Rotogravura",
        "question": "Em qual situação a rotogravura é especialmente indicada?",
        "options": [
            "Na impressão de grandes tiragens de embalagens flexíveis.",
            "Na pintura manual de quadros únicos.",
            "Na impressão doméstica de documentos em pequenas quantidades.",
            "Na produção artesanal de desenhos sem tinta.",
        ],
        "correct": 0,
        "explanation": "A rotogravura é ideal para altíssimas tiragens industriais, como embalagens flexíveis (salgadinhos, biscoitos) e revistas de circulação nacional!",
    },
    {
        "theme": "Serigrafia vs Rotogravura",
        "question": "Qual é a principal diferença entre serigrafia e rotogravura?",
        "options": [
            "Os dois processos utilizam exclusivamente impressoras digitais.",
            "A serigrafia utiliza uma tela, enquanto a rotogravura utiliza cilindros gravados.",
            "A rotogravura utiliza telas, enquanto a serigrafia utiliza cilindros gravados.",
            "Nenhum dos dois processos utiliza tinta.",
        ],
        "correct": 1,
        "explanation": "A diferença principal está na matriz: a serigrafia utiliza uma tela vazada, enquanto a rotogravura utiliza cilindros metálicos com cavidades gravadas!",
    },
]

CORES = ["#EF4444", "#3B82F6", "#EAB308", "#22C55E"]
FORMAS = ["🔴", "🔵", "🟡", "🟢"]
LETRAS = ["A", "B", "C", "D"]


# ==============================================================================
# SALA COMPARTILHADA (uma só para todos os aparelhos conectados)
# ==============================================================================
@st.cache_resource
def get_room():
    return {
        "lock": threading.Lock(),
        "game_id": 0,          # muda a cada reinício, para derrubar sessões antigas
        "status": "LOBBY",     # LOBBY | QUESTION | REVEAL | PODIUM
        "players": {},         # {nome: pontos}
        "q_index": -1,
        "q_start": None,       # horário (servidor) em que a pergunta foi liberada
        "answers": {},         # {idx_pergunta: {nome: {opt, time, correct, points}}}
    }


room = get_room()


def reset_room():
    with room["lock"]:
        room["game_id"] += 1
        room["players"] = {}
        room["answers"] = {}
        room["q_index"] = -1
        room["q_start"] = None
        room["status"] = "LOBBY"


def start_question(idx):
    with room["lock"]:
        room["q_index"] = idx
        room["answers"][idx] = {}
        room["q_start"] = time.time()
        room["status"] = "QUESTION"


def end_question():
    with room["lock"]:
        if room["status"] == "QUESTION":
            room["status"] = "REVEAL"


def go_podium():
    with room["lock"]:
        room["status"] = "PODIUM"


def join_player(name):
    """Retorna False se o nome já estiver em uso."""
    with room["lock"]:
        if name.lower() in [n.lower() for n in room["players"]]:
            return False
        room["players"][name] = 0
        return True


def register_answer(name, opt):
    """Pontos = base por velocidade (500 a 1000) + bônus para os primeiros a acertar."""
    with room["lock"]:
        if room["status"] != "QUESTION" or name not in room["players"]:
            return
        idx = room["q_index"]
        answers = room["answers"].setdefault(idx, {})
        if name in answers:  # só uma resposta por pergunta
            return
        elapsed = time.time() - room["q_start"]
        if elapsed > TEMPO_LIMITE + 1.5:
            return
        elapsed = min(elapsed, TEMPO_LIMITE)
        correct = (opt == QUESTIONS[idx]["correct"])
        points = 0
        if correct:
            base = int(1000 * (1 - (elapsed / TEMPO_LIMITE) / 2))
            ordem = sum(1 for a in answers.values() if a["correct"])
            bonus = BONUS_PRIMEIROS[ordem] if ordem < len(BONUS_PRIMEIROS) else 0
            points = base + bonus
            room["players"][name] += points
        answers[name] = {"opt": opt, "time": round(elapsed, 1), "correct": correct, "points": points}


def ranking():
    return sorted(list(room["players"].items()), key=lambda x: x[1], reverse=True)


def posicao(nome):
    for i, (n, _) in enumerate(ranking()):
        if n == nome:
            return i + 1
    return None


# ==============================================================================
# QR CODE
# ==============================================================================
def detectar_url():
    try:
        headers = st.context.headers
        host = headers.get("Host", "")
        if host:
            proto = headers.get("X-Forwarded-Proto") or ("http" if host.startswith(("localhost", "127.")) else "https")
            return f"{proto}://{host}"
    except Exception:
        pass
    return "https://SEU-APP.streamlit.app"


@st.cache_data
def gerar_qr(url):
    try:
        import qrcode
        img = qrcode.make(url)
        buf = BytesIO()
        img.save(buf, format="PNG")
        return buf.getvalue()
    except Exception:
        return f"https://api.qrserver.com/v1/create-qr-code/?size=500x500&data={quote(url, safe='')}"


def opcoes_html(q, revelar=False):
    html = '<div style="display:grid;grid-template-columns:1fr 1fr;gap:14px;margin:1rem 0;">'
    for i, texto in enumerate(q["options"]):
        certa = (i == q["correct"])
        opac = 1 if (not revelar or certa) else 0.3
        borda = "6px solid #0F172A" if (revelar and certa) else "6px solid transparent"
        cor_txt = "#0F172A" if i == 2 else "#FFFFFF"
        html += (
            f'<div style="background:{CORES[i]};opacity:{opac};border:{borda};border-radius:16px;'
            f'padding:1.2rem;font-size:1.35rem;font-weight:800;color:{cor_txt} !important;line-height:1.35;">'
            f'{FORMAS[i]} {LETRAS[i]}) {texto}</div>'
        )
    return html + "</div>"


def assinatura():
    st.markdown('<div class="dev-signature">✨ Desenvolvido por Daiane Silva</div>', unsafe_allow_html=True)


# ==============================================================================
# TELÃO DO APRESENTADOR
# ==============================================================================
@st.fragment(run_every=1)
def painel_telao():
    # Encerra sozinho quando o tempo acaba ou todos já responderam
    if room["status"] == "QUESTION":
        idx = room["q_index"]
        elapsed = time.time() - room["q_start"]
        respondidas = len(room["answers"].get(idx, {}))
        total = len(room["players"])
        if elapsed >= TEMPO_LIMITE or (total > 0 and respondidas >= total):
            end_question()

    status = room["status"]
    st.markdown('<div class="theme-badge">🖥️ TELÃO DO APRESENTADOR</div>', unsafe_allow_html=True)

    # ---------------- LOBBY ----------------
    if status == "LOBBY":
        st.session_state["balloons_done"] = False
        st.title("Quiz de Fixação: Serigrafia vs Rotogravura")
        st.caption("Produção Gráfica • SENAI")

        link = st.session_state.get("link_site", detectar_url())
        col_qr, col_info = st.columns([1.2, 1.8])
        with col_qr:
            st.markdown('<h3 style="text-align:center;color:#7C3AED;">Aponte a câmera 📱</h3>', unsafe_allow_html=True)
            st.image(gerar_qr(link), use_container_width=True)
            st.caption(f"🔗 {link}")
        with col_info:
            st.markdown(
                '<div class="white-card"><h3 style="margin-top:0;">Entrem pelo celular!</h3>'
                '<p style="font-size:1.15rem;">Aponte a câmera para o QR Code, digite seu nome e aguarde o início.'
                ' Quem acertar mais <b>rápido</b> ganha mais pontos!</p></div>',
                unsafe_allow_html=True,
            )
            if "SEU-APP" in link or "localhost" in link or "127.0.0.1" in link:
                st.warning("⚠️ O link do QR Code não é público. Ajuste em **Link do quiz** (no topo da página).")

            jogadores = list(room["players"].keys())
            st.markdown(f"### 👥 Alunos conectados: **{len(jogadores)}**")
            if jogadores:
                st.write(", ".join(f"`{n}`" for n in jogadores))
            else:
                st.caption("Aguardando os alunos conectarem...")
            if st.button("🚀 INICIAR QUIZ", type="primary", use_container_width=True, disabled=not jogadores):
                start_question(0)
                st.rerun(scope="fragment")

    # ---------------- PERGUNTA ----------------
    elif status == "QUESTION":
        idx = room["q_index"]
        q = QUESTIONS[idx]
        restante = max(0.0, TEMPO_LIMITE - (time.time() - room["q_start"]))
        respondidas = len(room["answers"].get(idx, {}))
        total = len(room["players"])

        st.markdown(
            f'<span class="theme-badge">{q["theme"]}</span> '
            f'<span style="color:#6D28D9;font-weight:800;">Questão {idx + 1} de {len(QUESTIONS)}</span>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div class="white-card"><p style="font-size:2rem;font-weight:800;margin:0;line-height:1.35;">{q["question"]}</p></div>',
            unsafe_allow_html=True,
        )
        st.progress(restante / TEMPO_LIMITE, text=f"⏱️ {int(restante) + 1}s")
        st.markdown(opcoes_html(q), unsafe_allow_html=True)
        st.info(f"✋ {respondidas} de {total} alunos responderam")
        if st.button("⏭️ Encerrar pergunta agora"):
            end_question()
            st.rerun(scope="fragment")

    # ---------------- RESULTADO DA PERGUNTA ----------------
    elif status == "REVEAL":
        idx = room["q_index"]
        q = QUESTIONS[idx]
        respostas = room["answers"].get(idx, {})
        acertos = sum(1 for a in respostas.values() if a["correct"])

        st.markdown(f'<span class="theme-badge">Resultado • Questão {idx + 1} de {len(QUESTIONS)}</span>', unsafe_allow_html=True)
        st.markdown(
            f'<div class="white-card"><p style="font-size:1.8rem;font-weight:800;margin:0;">{q["question"]}</p></div>',
            unsafe_allow_html=True,
        )
        st.markdown(opcoes_html(q, revelar=True), unsafe_allow_html=True)
        st.markdown(
            f'<div class="white-card" style="background:#F0FDF4 !important;border:2px solid #86EFAC !important;">'
            f'<strong style="color:#15803D;font-size:1.2rem;">💡 Explicação:</strong>'
            f'<p style="font-size:1.2rem;margin:0.4rem 0 0 0;">{q["explanation"]}</p></div>',
            unsafe_allow_html=True,
        )
        st.write(f"✅ **{acertos}** de **{len(room['players'])}** acertaram")

        st.markdown("### ⭐ Ranking")
        for i, (nome, pts) in enumerate(ranking()[:5]):
            medalha = ["🥇", "🥈", "🥉"][i] if i < 3 else f"{i + 1}º"
            st.write(f"{medalha} **{nome}** — `{pts} pts`")

        ultima = (idx + 1 >= len(QUESTIONS))
        if st.button("🏆 VER PÓDIO FINAL" if ultima else "➡️ PRÓXIMA PERGUNTA", type="primary", use_container_width=True):
            if ultima:
                go_podium()
            else:
                start_question(idx + 1)
            st.rerun(scope="fragment")

    # ---------------- PÓDIO ----------------
    elif status == "PODIUM":
        if not st.session_state.get("balloons_done"):
            st.balloons()
            st.session_state["balloons_done"] = True
        st.markdown(
            '<div style="text-align:center;margin-bottom:2rem;"><h1 style="font-size:2.5rem;">🏆 PÓDIO DOS CAMPEÕES 🏆</h1>'
            '<p style="font-size:1.25rem;">Mestres em Serigrafia e Rotogravura!</p></div>',
            unsafe_allow_html=True,
        )
        rk = ranking()
        col2, col1, col3 = st.columns(3)
        with col2:
            if len(rk) > 1:
                st.markdown(
                    f'<div class="podium-box podium-silver"><div style="font-size:3rem;">🥈</div>'
                    f'<h3>{rk[1][0]}</h3><div style="font-weight:700;font-size:1.1rem;">{rk[1][1]} pts</div>'
                    f'<h2 style="color:#64748B;">2º Lugar</h2></div>', unsafe_allow_html=True)
        with col1:
            if len(rk) > 0:
                st.markdown(
                    f'<div class="podium-box podium-gold"><div style="font-size:3.2rem;">👑</div>'
                    f'<h2 style="color:#D97706;">{rk[0][0]}</h2><div style="font-weight:900;font-size:1.3rem;">{rk[0][1]} pts</div>'
                    f'<h1 style="color:#F59E0B;font-size:2rem;">1º Lugar</h1></div>', unsafe_allow_html=True)
        with col3:
            if len(rk) > 2:
                st.markdown(
                    f'<div class="podium-box podium-bronze"><div style="font-size:3rem;">🥉</div>'
                    f'<h3>{rk[2][0]}</h3><div style="font-weight:700;font-size:1.1rem;">{rk[2][1]} pts</div>'
                    f'<h2 style="color:#EA580C;">3º Lugar</h2></div>', unsafe_allow_html=True)

        st.divider()
        st.markdown("### 📊 Classificação geral da turma")
        for i, (nome, pts) in enumerate(rk):
            st.write(f"**{i + 1}º** {nome} — `{pts} pts`")
        if st.button("🔄 Reiniciar jogo para outra turma"):
            reset_room()
            st.rerun(scope="fragment")


def tela_telao():
    if not st.session_state.get("telao_ok"):
        st.title("🖥️ Telão do Apresentador")
        with st.form("pin_form"):
            pin = st.text_input("PIN de acesso:", type="password")
            if st.form_submit_button("Entrar", type="primary", use_container_width=True):
                if pin == PIN_APRESENTADOR:
                    st.session_state["telao_ok"] = True
                    st.rerun()
                else:
                    st.error("PIN incorreto.")
        return

    if room["status"] == "LOBBY":
        with st.expander("🔗 Link do quiz (usado no QR Code)"):
            st.text_input(
                "Link público do site dos alunos:",
                value=detectar_url(),
                key="link_site",
                help="Se o QR Code não abrir no celular, cole aqui o endereço público do seu app.",
            )
    painel_telao()
    assinatura()


# ==============================================================================
# CELULAR DO ALUNO
# ==============================================================================
@st.fragment(run_every=2)
def painel_aluno():
    nome = st.session_state["p_name"]

    # Sala foi reiniciada pelo apresentador: volta para a tela de nome
    if st.session_state.get("game_id") != room["game_id"] or nome not in room["players"]:
        st.rerun()

    status = room["status"]
    pontos = room["players"].get(nome, 0)
    c1, c2 = st.columns([2, 1])
    c1.markdown(f"👤 **{nome}**")
    c2.markdown(f"⭐ **{pontos} pts**")

    if status == "LOBBY":
        st.markdown(
            '<div class="white-card" style="text-align:center;padding:2.5rem 1.5rem;">'
            '<div style="font-size:3.5rem;">✨</div><h3>Você está conectado!</h3>'
            '<p style="font-size:1.05rem;">Aguarde o apresentador iniciar o quiz no telão. '
            'A primeira pergunta aparece aqui automaticamente.</p></div>',
            unsafe_allow_html=True,
        )

    elif status == "QUESTION":
        idx = room["q_index"]
        q = QUESTIONS[idx]
        minha = room["answers"].get(idx, {}).get(nome)
        restante = max(0, int(TEMPO_LIMITE - (time.time() - room["q_start"])))

        if minha is None:
            st.markdown(
                f'<div class="white-card"><span class="theme-badge">{q["theme"]}</span>'
                f'<h4 style="color:#6D28D9;margin-bottom:0.3rem;">Questão {idx + 1} de {len(QUESTIONS)} • ⏱️ ~{restante}s</h4>'
                f'<p style="font-size:1.25rem;font-weight:800;line-height:1.45;margin:0;">{q["question"]}</p></div>',
                unsafe_allow_html=True,
            )
            st.markdown("**Responda rápido para pontuar mais!**")
            for i, texto in enumerate(q["options"]):
                if st.button(f"{FORMAS[i]} [{LETRAS[i]}]  {texto}", key=f"q_{idx}_btn_{i}", use_container_width=True):
                    register_answer(nome, i)
                    st.rerun(scope="fragment")
        else:
            st.markdown(
                '<div class="white-card" style="text-align:center;padding:2.5rem 1.5rem;">'
                '<div style="font-size:3.5rem;">✅</div><h3>Resposta enviada!</h3>'
                '<p style="font-size:1.05rem;">Aguarde o resultado no telão.</p></div>',
                unsafe_allow_html=True,
            )

    elif status == "REVEAL":
        idx = room["q_index"]
        q = QUESTIONS[idx]
        minha = room["answers"].get(idx, {}).get(nome)
        if minha is None:
            st.warning("⏰ Tempo esgotado! Você não respondeu a tempo.")
        elif minha["correct"]:
            st.success(f"🎉 **Você acertou!** +{minha['points']} pts (respondeu em {minha['time']}s)")
        else:
            st.error("😅 **Não foi dessa vez!** +0 pts")
        st.markdown(
            f'<div class="white-card"><strong>✅ Resposta correta:</strong>'
            f'<p style="font-size:1.1rem;font-weight:700;margin:0.3rem 0 0 0;">{FORMAS[q["correct"]]} {q["options"][q["correct"]]}</p></div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div class="white-card" style="background:#F0FDF4 !important;border:2px solid #86EFAC !important;">'
            f'<strong style="color:#15803D;">💡 Explicação:</strong>'
            f'<p style="margin:0.4rem 0 0 0;line-height:1.45;">{q["explanation"]}</p></div>',
            unsafe_allow_html=True,
        )
        st.write(f"🏅 Você está em **{posicao(nome)}º** lugar. Aguarde a próxima pergunta...")

    elif status == "PODIUM":
        st.markdown(
            f'<div class="white-card" style="text-align:center;padding:2.5rem 1.5rem;">'
            f'<div style="font-size:3.5rem;">🏁</div><h2>Parabéns, {nome}!</h2>'
            f'<p style="font-size:1.1rem;">Você concluiu o quiz!</p>'
            f'<div style="font-size:2.4rem;font-weight:900;color:#7C3AED;margin:1rem 0;">{pontos} pts</div>'
            f'<p>Você ficou em <b>{posicao(nome)}º</b> lugar. Veja o pódio no telão! 🏆</p></div>',
            unsafe_allow_html=True,
        )


def tela_aluno():
    # Se a sala foi reiniciada, esquece o nome antigo
    if "p_name" in st.session_state and st.session_state.get("game_id") != room["game_id"]:
        del st.session_state["p_name"]

    st.markdown('<div class="theme-badge">🎨 PRODUÇÃO GRÁFICA • SENAI</div>', unsafe_allow_html=True)
    st.title("Quiz de Fixação")
    st.caption("Serigrafia & Rotogravura")

    if "p_name" not in st.session_state:
        st.markdown(
            '<div class="white-card"><h3 style="margin-top:0;">Bem-vindo(a) ao Quiz! 👋</h3>'
            '<p style="margin-bottom:0;">Digite seu nome para disputar o pódio da turma:</p></div>',
            unsafe_allow_html=True,
        )
        with st.form("entrar"):
            nome = st.text_input("Seu nome ou apelido:", max_chars=20, placeholder="Ex: Maria S.")
            if st.form_submit_button("Entrar no jogo 🚀", type="primary", use_container_width=True):
                limpo = nome.strip()
                if not limpo:
                    st.warning("Por favor, digite seu nome!")
                elif join_player(limpo):
                    st.session_state["p_name"] = limpo
                    st.session_state["game_id"] = room["game_id"]
                    st.rerun()
                else:
                    st.warning("Esse nome já está em uso. Tente outro (ex.: acrescente uma letra).")
    else:
        painel_aluno()

    assinatura()


# ==============================================================================
if IS_TELAO:
    tela_telao()
else:
    tela_aluno()
