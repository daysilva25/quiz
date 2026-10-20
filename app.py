import streamlit as st
import time

# ==============================================================================
# QUIZ DE FIXAÇÃO: SERIGRAFIA & ROTOGRAVURA
# Desenvolvido por Daiane Silva
# Sistema Automático Estilo Kahoot (Pontuação por Velocidade & Pódio)
# ==============================================================================

st.set_page_config(
    page_title="Quiz de Fixação • Serigrafia & Rotogravura",
    page_icon="🎨",
    layout="centered"
)

# --- FORÇA TEMA CLARO, FUNDO BRANCO E MÁXIMA LEGIBILIDADE ---
st.markdown("""
<style>
    html, body, [data-testid="stAppViewContainer"], .stApp, main {
        background-color: #F8FAFC !important;
        background: #F8FAFC !important;
        color: #0F172A !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
    }

    [data-testid="stHeader"] {
        background-color: #F8FAFC !important;
    }

    /* Títulos em Preto/Escuro Nítido */
    h1, h2, h3, h4, [data-testid="stMarkdownContainer"] h1, [data-testid="stMarkdownContainer"] h2, [data-testid="stMarkdownContainer"] h3 {
        color: #0F172A !important;
        font-weight: 800 !important;
        letter-spacing: -0.5px !important;
    }

    /* Parágrafos e labels com alto contraste */
    p, span, label, div, [data-testid="stMarkdownContainer"] p {
        color: #1E293B !important;
    }

    /* Card Branco Limpo */
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

    .stButton > button p, .stButton > button div, .stButton > button span {
        color: #0F172A !important;
        font-size: 1.15rem !important;
        font-weight: 700 !important;
        line-height: 1.4 !important;
        text-align: left !important;
    }

    /* Botão Primário Roxo */
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

    /* Pódio dos Campeões */
    .podium-box {
        background: #FFFFFF !important;
        border: 2px solid #E2E8F0 !important;
        border-radius: 16px !important;
        padding: 1.2rem !important;
        text-align: center !important;
        box-shadow: 0 6px 18px rgba(0,0,0,0.06) !important;
    }
    .podium-gold { border-top: 8px solid #F59E0B !important; }
    .podium-silver { border-top: 8px solid #94A3B8 !important; }
    .podium-bronze { border-top: 8px solid #FB923C !important; }

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

# --- BASE DE PERGUNTAS ---
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
        "explanation": "Na serigrafia a matriz é permeável (malha de poliéster). A tinta vaza apenas pelas áreas abertas onde não há emulsão!"
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
        "explanation": "A rotogravura é um processo encavográfico (baixo-relevo). Os cilindros de cobre possuem milhões de minúsculas células (alvéolos) que transferem a tinta."
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
        "explanation": "A gravação do cilindro tem custo inicial alto, mas em tiragens de milhões de metros o custo unitário fica incrivelmente baixo com máxima velocidade!"
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
        "explanation": "A serigrafia deposita muito mais tinta que outros processos, permitindo cores vivas e opacas em camisetas, canecas, vidros e acrílicos."
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
        "explanation": "Pegadinha de prova! A Doctor Blade raspa o excesso do cilindro na Rotogravura. Já o rodo de poliuretano é da Serigrafia!"
    }
]

# --- ESTADO COMPARTILHADO EM MEMÓRIA (COMPARTILHADO POR TODA A TURMA) ---
@st.cache_resource
def get_shared_room():
    return {
        "status": "LOBBY",         # LOBBY, RUNNING, PODIUM
        "scores": {},              # {nome: pontuacao_acumulada}
        "players": [],             # [nome1, nome2, ...]
        "finished_players": {}     # {nome: total_pontos}
    }

room = get_shared_room()

tab_player, tab_host = st.tabs(["📱 Jogar pelo Celular", "🖥️ Telão do Apresentador"])

# ==============================================================================
# 1. ABA DO JOGADOR (CELULAR) - 100% AUTOMÁTICO
# ==============================================================================
with tab_player:
    st.markdown('<div class="theme-badge">🎨 PRODUÇÃO GRÁFICA</div>', unsafe_allow_html=True)
    st.title("Quiz de Fixação")
    st.caption("Serigrafia & Rotogravura")

    # Estados locais de sessão do aluno
    if "p_name" not in st.session_state:
        st.session_state["p_name"] = ""
    if "q_index" not in st.session_state:
        st.session_state["q_index"] = 0
    if "q_start_time" not in st.session_state:
        st.session_state["q_start_time"] = None
    if "last_result" not in st.session_state:
        st.session_state["last_result"] = None
    if "quiz_finished" not in st.session_state:
        st.session_state["quiz_finished"] = False

    # PASSO 1: O ALUNO COLOCA O NOME
    if not st.session_state["p_name"]:
        st.markdown("""
        <div class="white-card">
            <h3 style="margin-top: 0;">Bem-vindo(a) ao Quiz! 👋</h3>
            <p style="color: #475569; font-size: 1rem; margin-bottom: 0;">Digite seu nome para entrar na sala e disputar o pódio:</p>
        </div>
        """, unsafe_allow_html=True)

        nome_digitado = st.text_input("Seu Nome ou Apelido:", max_chars=20, placeholder="Ex: Daiane Silva")
        if st.button("Entrar no Jogo 🚀", type="primary", use_container_width=True):
            clean_name = nome_digitado.strip()
            if clean_name:
                st.session_state["p_name"] = clean_name
                if clean_name not in room["players"]:
                    room["players"].append(clean_name)
                    room["scores"][clean_name] = 0
                st.rerun()
            else:
                st.warning("Por favor, digite seu nome!")

    # ALUNO LOGADO
    else:
        player_name = st.session_state["p_name"]
        current_score = room["scores"].get(player_name, 0)

        # Barra do Jogador
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown(f"👤 Jogador: **{player_name}**")
        with col2:
            st.markdown(f"⭐ **{current_score} pts**")

        # Se o apresentador ainda não liberou o jogo
        if room["status"] == "LOBBY":
            st.markdown("""
            <div class="white-card" style="text-align: center; padding: 2.5rem 1.5rem;">
                <div style="font-size: 3.5rem; margin-bottom: 0.5rem;">✨</div>
                <h3 style="margin-bottom: 0.5rem;">Você está na Sala de Espera!</h3>
                <p style="color: #475569; font-size: 1.05rem;">
                    Assim que o apresentador clicar em <b>Iniciar Quiz</b> no telão, suas perguntas vão começar!
                </p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("🔄 Atualizar para começar", use_container_width=True):
                st.rerun()

        # O JOGO ESTÁ LIBERADO!
        elif room["status"] in ["RUNNING", "PODIUM"]:
            q_i = st.session_state["q_index"]

            # Se já respondeu todas as perguntas
            if q_i >= len(QUESTIONS) or st.session_state["quiz_finished"]:
                st.session_state["quiz_finished"] = True
                room["finished_players"][player_name] = current_score

                st.markdown(f"""
                <div class="white-card" style="text-align: center; padding: 2.5rem 1.5rem;">
                    <div style="font-size: 3.5rem; margin-bottom: 0.5rem;">🏁</div>
                    <h2>Parabéns, {player_name}!</h2>
                    <p style="color: #475569; font-size: 1.1rem;">Você concluiu todas as perguntas do Quiz!</p>
                    <div style="font-size: 2.4rem; font-weight: 900; color: #7C3AED; margin: 1rem 0;">
                        {current_score} pts
                    </div>
                    <p style="color: #64748B;">Olhe para o telão da sala para ver o <b>Pódio dos Campeões</b>!</p>
                </div>
                """, unsafe_allow_html=True)

            # Perguntas ativas no celular do aluno
            else:
                q = QUESTIONS[q_i]

                # Se acabou de responder, mostra o feedback imediato
                if st.session_state["last_result"] is not None:
                    res = st.session_state["last_result"]
                    if res["is_correct"]:
                        st.balloons()
                        st.success(f"🎉 **Você Acertou!** (+{res['points']} pts em {res['time_taken']}s)")
                    else:
                        st.error(f"😅 **Não foi dessa vez!** (+0 pts)")

                    st.markdown(f"""
                    <div class="white-card" style="background: #F0FDF4 !important; border: 2px solid #86EFAC !important;">
                        <strong style="color: #15803D; font-size: 1.05rem;">💡 Explicação Didática:</strong>
                        <p style="color: #166534 !important; margin-top: 0.4rem; font-size: 1rem; line-height: 1.45;">
                            {q['explanation']}
                        </p>
                    </div>
                    """, unsafe_allow_html=True)

                    btn_next_text = "Ver Resultado Final 🏆" if q_i + 1 >= len(QUESTIONS) else "Próxima Pergunta ➡️"
                    if st.button(btn_next_text, type="primary", use_container_width=True):
                        st.session_state["q_index"] += 1
                        st.session_state["last_result"] = None
                        st.session_state["q_start_time"] = time.time()
                        st.rerun()

                # Pergunta para responder
                else:
                    if st.session_state["q_start_time"] is None:
                        st.session_state["q_start_time"] = time.time()

                    st.markdown(f"""
                    <div class="white-card">
                        <span class="theme-badge">{q['theme']}</span>
                        <h4 style="color: #6D28D9; margin-bottom: 0.3rem;">Pergunta {q_i + 1} de {len(QUESTIONS)}</h4>
                        <p style="font-size: 1.25rem; font-weight: 800; color: #0F172A; line-height: 1.45; margin: 0;">
                            {q['question']}
                        </p>
                    </div>
                    """, unsafe_allow_html=True)

                    st.markdown("<p style='font-weight: 700; color: #0F172A; font-size: 1.05rem;'>Selecione a opção correta rápido para pontuar mais:</p>", unsafe_allow_html=True)
                    symbols = ["🔴 [A]", "🔵 [B]", "🟡 [C]", "🟢 [D]"]

                    for opt_idx, opt_text in enumerate(q["options"]):
                        if st.button(f"{symbols[opt_idx]}  {opt_text}", key=f"q_{q_i}_btn_{opt_idx}", use_container_width=True):
                            elapsed = time.time() - st.session_state["q_start_time"]
                            is_correct = (opt_idx == q["correct"])

                            # FÓRMULA OFICIAL KAHOOT:
                            # Até 1000 pontos. Resposta rápida ganha ~980 pts. Resposta lenta ganha ~500 pts. Erro = 0 pts.
                            points = 0
                            if is_correct:
                                time_limit = 25.0
                                factor = 1.0 - ((min(elapsed, time_limit) / time_limit) / 2.0)
                                points = int(1000 * factor)
                                room["scores"][player_name] = room["scores"].get(player_name, 0) + points

                            st.session_state["last_result"] = {
                                "is_correct": is_correct,
                                "points": points,
                                "time_taken": round(elapsed, 1)
                            }
                            st.rerun()

    st.markdown('<div class="dev-signature">✨ Desenvolvido por Daiane Silva</div>', unsafe_allow_html=True)

# ==============================================================================
# 2. ABA DO TELÃO (APRESENTADOR) - SÓ CONEXÕES E PÓDIO!
# ==============================================================================
with tab_host:
    st.markdown('<div class="theme-badge">🖥️ CONTROLE DO TELÃO</div>', unsafe_allow_html=True)
    st.title("Painel do Telão")

    pin = st.text_input("PIN do Apresentador:", type="password", key="pin_host")

    if pin != "2026":
        st.info("Digite o PIN `2026` para gerenciar o telão da apresentação.")
    else:
        st.success("Modo Telão Ativo!")

        # 1. TELA DE ENTRADA / ESPERA
        if room["status"] == "LOBBY":
            st.markdown("""
            <div class="white-card" style="text-align: center; padding: 2rem;">
                <h1 style="font-size: 1.8rem; margin-top: 0;">🎨 Quiz de Fixação: Serigrafia vs Rotogravura</h1>
                <p style="color: #475569; font-size: 1.2rem; margin: 0.8rem 0;">
                    Acessem o link pelo celular e entrem na aba <b>"📱 Jogar pelo Celular"</b>!
                </p>
                <div style="font-size: 1.5rem; font-weight: 800; color: #7C3AED; background: #EDE9FE; display: inline-block; padding: 0.6rem 1.8rem; border-radius: 14px; margin-top: 0.5rem;">
                    Código da Sala: 2026
                </div>
            </div>
            """, unsafe_allow_html=True)

            connected_count = len(room["players"])
            st.markdown(f"### 👥 Alunos Conectados: **{connected_count}**")

            if room["players"]:
                st.write(", ".join([f"`{name}`" for name in room["players"]]))
            else:
                st.caption("Aguardando os alunos entrarem...")

            st.write("")
            if st.button("🚀 INICIAR QUIZ (Liberar para a turma responder)", type="primary", use_container_width=True):
                room["status"] = "RUNNING"
                st.rerun()

        # 2. TELA DURANTE O JOGO (ACOMPANHAMENTO AO VIVO)
        elif room["status"] == "RUNNING":
            st.markdown("""
            <div class="white-card" style="text-align: center; padding: 1.5rem;">
                <h2 style="margin: 0; color: #7C3AED;">🎮 Quiz em Andamento!</h2>
                <p style="color: #475569; font-size: 1.05rem; margin-top: 0.5rem;">
                    A turma está respondendo as perguntas no celular com pontuação por agilidade.
                </p>
            </div>
            """, unsafe_allow_html=True)

            fin_count = len(room["finished_players"])
            tot_count = len(room["players"])
            st.info(f"📊 **{fin_count} de {tot_count}** alunos já concluíram todas as perguntas.")

            # Placar em tempo real
            st.markdown("### ⭐ Ranking em Tempo Real:")
            sorted_scores = sorted(room["scores"].items(), key=lambda x: x[1], reverse=True)
            for idx, (p_name, s) in enumerate(sorted_scores[:5]):
                medal = "🥇" if idx == 0 else "🥈" if idx == 1 else "🥉" if idx == 2 else f"{idx+1}º"
                st.write(f"{medal} **{p_name}** — `{s} pts`")

            st.write("")
            if st.button("🏆 EXIBIR PÓDIO DOS CAMPEÕES", type="primary", use_container_width=True):
                room["status"] = "PODIUM"
                st.rerun()

        # 3. TELA DO PÓDIO FINAL (ESTILO KAHOOT)
        elif room["status"] == "PODIUM":
            st.balloons()
            st.markdown("""
            <div style="text-align: center; margin-bottom: 2rem;">
                <h1 style="font-size: 2.5rem;">🏆 PÓDIO DOS CAMPEÕES 🏆</h1>
                <p style="color: #475569; font-size: 1.25rem;">Mestres em Serigrafia e Rotogravura!</p>
            </div>
            """, unsafe_allow_html=True)

            sorted_ranking = sorted(room["scores"].items(), key=lambda x: x[1], reverse=True)
            col_p2, col_p1, col_p3 = st.columns(3)

            # 2º Lugar
            with col_p2:
                if len(sorted_ranking) > 1:
                    st.markdown(f"""
                    <div class="podium-box podium-silver">
                        <div style="font-size: 3rem;">🥈</div>
                        <h3 style="margin: 0.3rem 0; font-size: 1.25rem;">{sorted_ranking[1][0]}</h3>
                        <div style="color: #475569; font-weight: 700; font-size: 1.1rem;">{sorted_ranking[1][1]} pts</div>
                        <h2 style="color: #64748B; margin-top: 0.5rem;">2º Lugar</h2>
                    </div>
                    """, unsafe_allow_html=True)

            # 1º Lugar
            with col_p1:
                if len(sorted_ranking) > 0:
                    st.markdown(f"""
                    <div class="podium-box podium-gold">
                        <div style="font-size: 3.2rem;">👑</div>
                        <h2 style="margin: 0.3rem 0; font-size: 1.45rem; color: #D97706;">{sorted_ranking[0][0]}</h2>
                        <div style="color: #D97706; font-weight: 900; font-size: 1.3rem;">{sorted_ranking[0][1]} pts</div>
                        <h1 style="color: #F59E0B; margin-top: 0.5rem; font-size: 2rem;">1º Lugar</h1>
                    </div>
                    """, unsafe_allow_html=True)

            # 3º Lugar
            with col_p3:
                if len(sorted_ranking) > 2:
                    st.markdown(f"""
                    <div class="podium-box podium-bronze">
                        <div style="font-size: 3rem;">🥉</div>
                        <h3 style="margin: 0.3rem 0; font-size: 1.25rem;">{sorted_ranking[2][0]}</h3>
                        <div style="color: #475569; font-weight: 700; font-size: 1.1rem;">{sorted_ranking[2][1]} pts</div>
                        <h2 style="color: #EA580C; margin-top: 0.5rem;">3º Lugar</h2>
                    </div>
                    """, unsafe_allow_html=True)

            st.divider()

            # Classificação Geral
            st.markdown("### 📊 Classificação Geral da Turma:")
            for i, (name, pts) in enumerate(sorted_ranking):
                st.write(f"**{i+1}º** {name} — `{pts} pts`")

            st.write("")
            if st.button("🔄 Reiniciar Jogo para Outra Turma"):
                room["status"] = "LOBBY"
                room["scores"] = {}
                room["players"] = []
                room["finished_players"] = {}
                st.rerun()

    st.markdown('<div class="dev-signature">✨ Desenvolvido por Daiane Silva</div>', unsafe_allow_html=True)
