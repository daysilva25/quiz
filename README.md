import streamlit as st
import time

# ==============================================================================
# QUIZ DE FIXAÇÃO: SERIGRAFIA & ROTOGRAVURA
# Desenvolvido por Daiane Silva
# ==============================================================================

st.set_page_config(
    page_title="Quiz de Fixação • Serigrafia & Rotogravura",
    page_icon="🎨",
    layout="centered"
)

# --- FORÇA TEMA CLARO, FUNDO BRANCO E CONTRASTE MÁXIMO ---
st.markdown("""
<style>
    /* Força fundo claro e texto escuro em TODA a aplicação */
    html, body, [data-testid="stAppViewContainer"], .stApp, main {
        background-color: #F8FAFC !important;
        background: #F8FAFC !important;
        color: #0F172A !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
    }

    [data-testid="stHeader"] {
        background-color: #F8FAFC !important;
    }

    /* Títulos em Preto / Ardósia de Alta Legibilidade */
    h1, h2, h3, h4, [data-testid="stMarkdownContainer"] h1, [data-testid="stMarkdownContainer"] h2, [data-testid="stMarkdownContainer"] h3 {
        color: #0F172A !important;
        font-weight: 800 !important;
        letter-spacing: -0.5px !important;
    }

    /* Todos os textos normais em escuro nítido */
    p, span, label, div, [data-testid="stMarkdownContainer"] p {
        color: #1E293B !important;
    }

    /* Card da Pergunta e Informações em Branco Puro */
    .white-card {
        background-color: #FFFFFF !important;
        border: 2px solid #E2E8F0 !important;
        border-radius: 18px !important;
        padding: 1.5rem !important;
        margin-bottom: 1.25rem !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.04) !important;
    }

    /* Pílula de Tema */
    .theme-badge {
        background-color: #EDE9FE !important;
        border: 1px solid #DDD6FE !important;
        color: #6D28D9 !important;
        padding: 0.35rem 0.9rem !important;
        border-radius: 9999px !important;
        font-size: 0.85rem !important;
        font-weight: 700 !important;
        display: inline-block !important;
        margin-bottom: 0.5rem !important;
    }

    /* BOTÕES DAS ALTERNATIVAS: BRANCOS, GRANDES E TEXTO ESCURO NÍTIDO */
    .stButton > button {
        background-color: #FFFFFF !important;
        border: 2px solid #CBD5E1 !important;
        border-radius: 14px !important;
        padding: 1rem 1.25rem !important;
        min-height: 58px !important;
        text-align: left !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04) !important;
        transition: all 0.2s ease !important;
        width: 100% !important;
    }

    .stButton > button:hover {
        background-color: #F1F5F9 !important;
        border-color: #7C3AED !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 15px rgba(124, 58, 237, 0.12) !important;
    }

    /* FORÇA A COR DO TEXTO DENTRO DOS BOTÕES A SER ESCURA */
    .stButton > button p, .stButton > button div, .stButton > button span {
        color: #0F172A !important;
        font-size: 1.15rem !important;
        font-weight: 700 !important;
        line-height: 1.4 !important;
        text-align: left !important;
    }

    /* Botão Principal Roxo (Entrar / Iniciar) */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #7C3AED 0%, #6D28D9 100%) !important;
        border: none !important;
        box-shadow: 0 4px 15px rgba(124, 58, 237, 0.3) !important;
    }
    .stButton > button[kind="primary"] p {
        color: #FFFFFF !important;
        font-weight: 800 !important;
        font-size: 1.15rem !important;
    }

    /* Inputs de Texto */
    [data-baseweb="input"], input {
        background-color: #FFFFFF !important;
        color: #0F172A !important;
        border: 2px solid #CBD5E1 !important;
        border-radius: 12px !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
    }
    input::placeholder {
        color: #94A3B8 !important;
    }

    /* Abas Superiores */
    [data-baseweb="tab-list"] {
        background-color: #E2E8F0 !important;
        border-radius: 12px !important;
        padding: 4px !important;
        margin-bottom: 1.5rem !important;
    }
    [data-baseweb="tab"] {
        color: #475569 !important;
        font-weight: 700 !important;
    }
    [aria-selected="true"] {
        background-color: #FFFFFF !important;
        color: #7C3AED !important;
        border-radius: 8px !important;
        box-shadow: 0 2px 6px rgba(0,0,0,0.06) !important;
    }

    /* Pódio */
    .podium-box {
        background: #FFFFFF !important;
        border: 2px solid #E2E8F0 !important;
        border-radius: 16px !important;
        padding: 1.2rem !important;
        text-align: center !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.04) !important;
    }
    .podium-gold { border-top: 6px solid #F59E0B !important; }
    .podium-silver { border-top: 6px solid #94A3B8 !important; }
    .podium-bronze { border-top: 6px solid #FB923C !important; }

    /* Assinatura no Rodapé */
    .dev-signature {
        text-align: center !important;
        font-size: 0.82rem !important;
        color: #94A3B8 !important;
        margin-top: 2.5rem !important;
        padding-top: 1rem !important;
        border-top: 1px solid #E2E8F0 !important;
        font-weight: 600 !important;
    }
</style>
""", unsafe_allow_html=True)

# --- BASE DE PERGUNTAS (EMBUTIDA NO CÓDIGO) ---
QUESTIONS = [
    {
        "theme": "Serigrafia",
        "question": "A Serigrafia (silk-screen) pertence a qual categoria de processo de impressão quanto ao tipo de sua matriz?",
        "options": [
            "Permeográfico (a tinta é forçada através das aberturas da malha)",
            "Relevográfico (a imagem a ser impressa fica em alto-relevo)",
            "Encavográfico (a imagem fica em cavidades/baixo-relevo)",
            "Planográfico (grafismo e não-grafismo estão no mesmo nível)"
        ],
        "correct": 0,
        "explanation": "Na serigrafia a matriz é permeável (malha de poliéster). A tinta passa apenas pelas áreas vazadas onde não há emulsão!"
    },
    {
        "theme": "Rotogravura",
        "question": "Como a imagem é gravada na matriz do processo de Rotogravura?",
        "options": [
            "Em microporos em uma tela de tecido tensionada",
            "Em alvéolos (reentrâncias em baixo-relevo) em um cilindro de cobre",
            "Em uma chapa metálica plana através da repulsão de água e gordura",
            "Em um fotopolímero flexível em alto-relevo colado no cilindro"
        ],
        "correct": 1,
        "explanation": "A rotogravura é um processo encavográfico (baixo-relevo). Os cilindros de aço e cobre possuem milhões de minúsculas células (alvéolos) que seguram a tinta."
    },
    {
        "theme": "Rotogravura",
        "question": "Por que a Rotogravura é o padrão da indústria para embalagens de salgadinho (BOPP) e rótulos de grande escala?",
        "options": [
            "Porque a gravação dos cilindros é barata e compensa poucas unidades",
            "Porque é um processo artesanal feito manualmente folha por folha",
            "Pela altíssima velocidade e uniformidade em tiragens gigantescas, diluindo o custo dos cilindros",
            "Porque só funciona em papéis foscos e cartões de alta gramatura"
        ],
        "correct": 2,
        "explanation": "A gravação de cilindros de rotogravura é cara, mas em tiragens de centenas de milhares ou milhões de metros, o custo unitário fica incrivelmente baixo com máxima velocidade!"
    },
    {
        "theme": "Serigrafia",
        "question": "Qual é uma das principais vantagens técnicas da Serigrafia para o Design Gráfico?",
        "options": [
            "Velocidade de mais de 100.000 impressões por hora",
            "Deposição de camada espessa e opaca de tinta, imprimindo em quase qualquer material (tecido, vidro, madeira)",
            "Resolução microscópica de retículas infinitamente superior ao offset",
            "Dispensa o uso de tintas líquidas, usando apenas calor"
        ],
        "correct": 1,
        "explanation": "A serigrafia deposita muito mais tinta que os outros processos, gerando alta cobertura e cores vivas em praticamente qualquer suporte."
    },
    {
        "theme": "Duelo: Serigrafia vs Rotogravura",
        "question": "Qual componente é responsável por raspar o excesso de tinta do cilindro na Rotogravura antes do contato com o material?",
        "options": [
            "Rodo de poliuretano (puxador)",
            "Doctor Blade (lâmina raspadora de aço)",
            "Emulsão fotossensível diazoica",
            "Bastidor de madeira com presilhas"
        ],
        "correct": 1,
        "explanation": "Pegadinha clássica! A Doctor Blade raspa o excesso na Rotogravura. Já o rodo de poliuretano é a ferramenta da Serigrafia!"
    }
]

# --- ESTADO COMPARTILHADO EM MEMÓRIA ---
@st.cache_resource
def get_room_state():
    return {
        "state": "LOBBY",
        "current_q": 0,
        "q_start_time": time.time(),
        "scores": {},
        "answers": {}
    }

room = get_room_state()

# --- DUAS ABAS: CELULAR E TELÃO ---
tab_player, tab_host = st.tabs(["📱 Jogar pelo Celular", "🖥️ Telão do Apresentador"])

# ==============================================================================
# 1. ABA DO JOGADOR (CELULAR)
# ==============================================================================
with tab_player:
    st.markdown('<div class="theme-badge">🎨 PRODUÇÃO GRÁFICA</div>', unsafe_allow_html=True)
    st.title("Quiz de Fixação")
    st.caption("Serigrafia & Rotogravura")

    if "player_name" not in st.session_state:
        st.session_state["player_name"] = ""

    # Identificação do Jogador
    if not st.session_state["player_name"]:
        st.markdown("""
        <div class="white-card">
            <h3 style="margin-top: 0;">Bem-vindo(a) ao Quiz! 👋</h3>
            <p style="color: #475569; font-size: 1rem; margin-bottom: 0;">Digite seu nome para participar:</p>
        </div>
        """, unsafe_allow_html=True)

        nome = st.text_input("Seu Nome ou Apelido:", max_chars=20, placeholder="Ex: Daiane Silva")
        if st.button("Entrar no Jogo 🚀", type="primary", use_container_width=True):
            if nome.strip():
                st.session_state["player_name"] = nome.strip()
                if nome.strip() not in room["scores"]:
                    room["scores"][nome.strip()] = 0
                st.rerun()
            else:
                st.warning("Por favor, digite seu nome!")
    else:
        player_name = st.session_state["player_name"]
        my_score = room["scores"].get(player_name, 0)

        # Barra do Jogador
        col_p1, col_p2 = st.columns([2, 1])
        with col_p1:
            st.markdown(f"👤 Jogador: **{player_name}**")
        with col_p2:
            st.markdown(f"⭐ **{my_score} pts**")

        # 1. Espera no Celular
        if room["state"] == "LOBBY":
            st.markdown("""
            <div class="white-card" style="text-align: center; padding: 2.5rem 1.5rem;">
                <div style="font-size: 3.5rem; margin-bottom: 0.5rem;">✨</div>
                <h3 style="margin-bottom: 0.5rem;">Você está conectado!</h3>
                <p style="color: #475569; font-size: 1.05rem;">Fique de olho no telão da sala. O quiz começará em instantes!</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("🔄 Atualizar status", use_container_width=True):
                st.rerun()

        # 2. Pergunta Ativa no Celular
        elif room["state"] in ["QUESTION", "REVEAL"]:
            q_idx = room["current_q"]
            if q_idx < len(QUESTIONS):
                q = QUESTIONS[q_idx]

                st.markdown(f"""
                <div class="white-card">
                    <span class="theme-badge">{q['theme']}</span>
                    <h4 style="color: #6D28D9; margin-bottom: 0.3rem;">Pergunta {q_idx + 1} de {len(QUESTIONS)}</h4>
                    <p style="font-size: 1.25rem; font-weight: 800; color: #0F172A; line-height: 1.45; margin: 0;">
                        {q['question']}
                    </p>
                </div>
                """, unsafe_allow_html=True)

                q_answers = room["answers"].setdefault(q_idx, {})
                already_answered = player_name in q_answers

                if room["state"] == "QUESTION" and not already_answered:
                    st.markdown("<p style='font-weight: 700; color: #0F172A; font-size: 1.05rem;'>Selecione a resposta correta:</p>", unsafe_allow_html=True)
                    symbols = ["🔴 [A]", "🔵 [B]", "🟡 [C]", "🟢 [D]"]
                    for idx, opt_text in enumerate(q["options"]):
                        btn_text = f"{symbols[idx]}  {opt_text}"
                        if st.button(btn_text, key=f"opt_btn_{idx}", use_container_width=True):
                            elapsed = time.time() - room["q_start_time"]
                            remaining = max(0.0, 25.0 - elapsed)
                            is_correct = (idx == q["correct"])
                            points = 0
                            if is_correct:
                                ratio = min(1.0, remaining / 25.0)
                                points = int(500 + 500 * ratio)
                                room["scores"][player_name] = room["scores"].get(player_name, 0) + points

                            q_answers[player_name] = {
                                "option": idx,
                                "points": points,
                                "correct": is_correct
                            }
                            st.rerun()

                elif already_answered:
                    ans = q_answers[player_name]
                    if room["state"] == "QUESTION":
                        st.info("✓ **Resposta registrada com sucesso!** Aguardando o apresentador revelar no telão...")
                        if st.button("🔄 Atualizar tela", use_container_width=True):
                            st.rerun()
                    else:
                        if ans["correct"]:
                            st.balloons()
                            st.success(f"🎉 **Você Acertou!** (+{ans['points']} pts)")
                        else:
                            st.error("😅 **Não foi dessa vez!** (+0 pts)")

                        st.markdown(f"""
                        <div class="white-card" style="background: #F0FDF4 !important; border: 2px solid #86EFAC !important;">
                            <strong style="color: #15803D; font-size: 1.05rem;">💡 Explicação Didática:</strong>
                            <p style="color: #166534 !important; margin-top: 0.4rem; font-size: 1rem; line-height: 1.45;">
                                {q['explanation']}
                            </p>
                        </div>
                        """, unsafe_allow_html=True)

                        if st.button("🔄 Próxima Rodada", use_container_width=True):
                            st.rerun()

        # 3. Pódio Final no Celular
        elif room["state"] == "PODIUM":
            st.markdown("""
            <div class="white-card" style="text-align: center; padding: 2.5rem 1.5rem;">
                <div style="font-size: 3.5rem; margin-bottom: 0.5rem;">🏆</div>
                <h2>Fim do Quiz!</h2>
                <p style="color: #475569; font-size: 1.05rem;">Confira os grandes campeões no telão da sala!</p>
            </div>
            """, unsafe_allow_html=True)

            sorted_ranking = sorted(room["scores"].items(), key=lambda x: x[1], reverse=True)
            my_rank = next((idx + 1 for idx, (n, s) in enumerate(sorted_ranking) if n == player_name), 1)
            st.metric("Sua Posição Final", f"{my_rank}º Lugar", f"{my_score} pts")

    st.markdown('<div class="dev-signature">✨ Desenvolvido por Daiane Silva</div>', unsafe_allow_html=True)

# ==============================================================================
# 2. ABA DO TELÃO (APRESENTADOR)
# ==============================================================================
with tab_host:
    st.markdown('<div class="theme-badge">🖥️ CONTROLE DO TELÃO</div>', unsafe_allow_html=True)
    st.title("Painel do Apresentador")

    pin = st.text_input("Digite o PIN do Apresentador:", type="password", key="pin_host")

    if pin != "2026":
        st.info("Digite o código PIN `2026` para gerenciar a apresentação.")
    else:
        st.success("Modo Apresentador Liberado!")

        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("🚀 Iniciar Pergunta", use_container_width=True, type="primary"):
                room["state"] = "QUESTION"
                room["q_start_time"] = time.time()
                st.rerun()
        with c2:
            if st.button("👁️ Revelar Resposta", use_container_width=True):
                room["state"] = "REVEAL"
                st.rerun()
        with c3:
            if st.button("➡️ Avançar / Pódio", use_container_width=True):
                if room["current_q"] + 1 < len(QUESTIONS):
                    room["current_q"] += 1
                    room["state"] = "QUESTION"
                    room["q_start_time"] = time.time()
                else:
                    room["state"] = "PODIUM"
                st.rerun()

        st.divider()

        if room["state"] == "LOBBY":
            st.markdown("""
            <div class="white-card" style="text-align: center; padding: 2rem;">
                <h2 style="margin-top: 0;">🎨 Quiz de Fixação: Serigrafia vs Rotogravura</h2>
                <p style="color: #475569; font-size: 1.15rem; margin: 0.8rem 0;">
                    Acessem pelo celular e entrem na aba <b>"📱 Jogar pelo Celular"</b>!
                </p>
                <div style="font-size: 1.4rem; font-weight: 800; color: #7C3AED; background: #EDE9FE; display: inline-block; padding: 0.5rem 1.5rem; border-radius: 12px; margin-top: 0.5rem;">
                    Código PIN: 2026
                </div>
            </div>
            """, unsafe_allow_html=True)

            players_count = len(room["scores"])
            st.write(f"👥 **{players_count} Aluno(s) conectado(s):**")
            if room["scores"]:
                st.write(", ".join([f"`{name}`" for name in room["scores"].keys()]))

        elif room["state"] in ["QUESTION", "REVEAL"]:
            q = QUESTIONS[room["current_q"]]
            st.markdown(f"""
            <div class="white-card">
                <span class="theme-badge">{q['theme']}</span>
                <h3 style="color: #6D28D9; margin-bottom: 0.3rem;">Pergunta {room['current_q'] + 1} de {len(QUESTIONS)}</h3>
                <h2 style="color: #0F172A; line-height: 1.4; margin: 0;">{q['question']}</h2>
            </div>
            """, unsafe_allow_html=True)

            symbols = ["🔴 [A]", "🔵 [B]", "🟡 [C]", "🟢 [D]"]
            for idx, opt in enumerate(q["options"]):
                is_correct = (idx == q["correct"]) and room["state"] == "REVEAL"
                if is_correct:
                    st.success(f"✓ **{symbols[idx]} {opt}** (CORRETA!)")
                else:
                    st.markdown(f"<div style='padding: 0.6rem 0.8rem; background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 10px; margin-bottom: 0.4rem; font-size: 1.05rem;'><b>{symbols[idx]}</b> {opt}</div>", unsafe_allow_html=True)

            if room["state"] == "REVEAL":
                st.info(f"💡 **Explicação para a turma:** {q['explanation']}")

        elif room["state"] == "PODIUM":
            st.balloons()
            st.markdown("""
            <div style="text-align: center; margin-bottom: 2rem;">
                <h1>🏆 PÓDIO DOS CAMPEÕES 🏆</h1>
                <p style="color: #475569; font-size: 1.2rem;">Mestres em Serigrafia e Rotogravura!</p>
            </div>
            """, unsafe_allow_html=True)

            sorted_ranking = sorted(room["scores"].items(), key=lambda x: x[1], reverse=True)
            col_p2, col_p1, col_p3 = st.columns(3)

            with col_p2:
                if len(sorted_ranking) > 1:
                    st.markdown(f"""
                    <div class="podium-box podium-silver">
                        <div style="font-size: 2.8rem;">🥈</div>
                        <h4 style="margin: 0.3rem 0;">{sorted_ranking[1][0]}</h4>
                        <div style="color: #475569; font-weight: 700;">{sorted_ranking[1][1]} pts</div>
                        <h2 style="color: #64748B; margin-top: 0.5rem;">2º Lugar</h2>
                    </div>
                    """, unsafe_allow_html=True)

            with col_p1:
                if len(sorted_ranking) > 0:
                    st.markdown(f"""
                    <div class="podium-box podium-gold">
                        <div style="font-size: 3.2rem;">👑</div>
                        <h4 style="margin: 0.3rem 0;">{sorted_ranking[0][0]}</h4>
                        <div style="color: #D97706; font-weight: 800; font-size: 1.2rem;">{sorted_ranking[0][1]} pts</div>
                        <h1 style="color: #F59E0B; margin-top: 0.5rem;">1º Lugar</h1>
                    </div>
                    """, unsafe_allow_html=True)

            with col_p3:
                if len(sorted_ranking) > 2:
                    st.markdown(f"""
                    <div class="podium-box podium-bronze">
                        <div style="font-size: 2.8rem;">🥉</div>
                        <h4 style="margin: 0.3rem 0;">{sorted_ranking[2][0]}</h4>
                        <div style="color: #475569; font-weight: 700;">{sorted_ranking[2][1]} pts</div>
                        <h2 style="color: #EA580C; margin-top: 0.5rem;">3º Lugar</h2>
                    </div>
                    """, unsafe_allow_html=True)

        st.markdown("### 📊 Classificação Geral da Turma")
        ranking = sorted(room["scores"].items(), key=lambda x: x[1], reverse=True)
        if ranking:
            for i, (name, pts) in enumerate(ranking):
                st.write(f"**{i+1}º** {name} — `{pts} pts`")
        else:
            st.caption("Nenhum participante pontuou ainda.")

        if st.button("🔄 Resetar Quiz Completo"):
            room["scores"] = {}
            room["answers"] = {}
            room["current_q"] = 0
            room["state"] = "LOBBY"
            st.rerun()

    st.markdown('<div class="dev-signature">✨ Desenvolvido por Daiane Silva</div>', unsafe_allow_html=True)
