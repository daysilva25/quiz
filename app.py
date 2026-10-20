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

# --- ESTILO VISUAL COM CORES SUAVES (DESIGN EDITORIAL) ---
st.markdown("""
<style>
    .stApp {
        background: radial-gradient(circle at 50% 0%, #F5F3FF 0%, #F8FAFC 60%, #E2E8F0 100%);
        color: #1E293B;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }

    h1, h2, h3, h4 {
        color: #1E293B !important;
        font-weight: 800 !important;
        letter-spacing: -0.5px;
    }

    /* Card Suave com Sombra Delicada */
    .soft-card {
        background: rgba(255, 255, 255, 0.95);
        border: 1px solid #E2E8F0;
        border-radius: 18px;
        padding: 1.5rem;
        box-shadow: 0 10px 25px -5px rgba(100, 116, 139, 0.08);
        margin-bottom: 1.25rem;
    }

    /* Pílula de Tema Suave */
    .theme-pill {
        background: rgba(139, 92, 246, 0.12);
        border: 1px solid rgba(139, 92, 246, 0.25);
        color: #6D28D9;
        padding: 0.3rem 0.9rem;
        border-radius: 9999px;
        font-size: 0.82rem;
        font-weight: 700;
        display: inline-block;
        margin-bottom: 0.5rem;
    }

    /* Pódio dos Campeões */
    .podium-box {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 16px;
        padding: 1.2rem;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    }

    .podium-gold { border-top: 6px solid #F59E0B; }
    .podium-silver { border-top: 6px solid #94A3B8; }
    .podium-bronze { border-top: 6px solid #FB923C; }

    /* Assinatura no Rodapé */
    .dev-signature {
        text-align: center;
        font-size: 0.8rem;
        color: #94A3B8;
        margin-top: 2.5rem;
        padding-top: 1rem;
        border-top: 1px solid #E2E8F0;
        font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)

# --- BASE DE PERGUNTAS (EMBUTIDA NO PRÓPRIO CÓDIGO) ---
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
    st.markdown('<div class="theme-pill">🎨 PRODUÇÃO GRÁFICA</div>', unsafe_allow_html=True)
    st.title("Quiz de Fixação")
    st.caption("Serigrafia & Rotogravura")

    if "player_name" not in st.session_state:
        st.session_state["player_name"] = ""

    if not st.session_state["player_name"]:
        st.markdown("""
        <div class="soft-card">
            <h4>Bem-vindo(a) ao Quiz! 👋</h4>
            <p style="color: #64748B; font-size: 0.95rem;">Digite seu nome para participar:</p>
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

        col_p1, col_p2 = st.columns([2, 1])
        with col_p1:
            st.write(f"👤 Jogador: **{player_name}**")
        with col_p2:
            st.write(f"⭐ **{my_score} pts**")

        if room["state"] == "LOBBY":
            st.markdown("""
            <div class="soft-card" style="text-align: center; padding: 2rem;">
                <div style="font-size: 3rem;">✨</div>
                <h3>Você está conectado!</h3>
                <p style="color: #64748B;">Fique de olho no telão da sala. O quiz começará em instantes!</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("🔄 Atualizar status", use_container_width=True):
                st.rerun()

        elif room["state"] in ["QUESTION", "REVEAL"]:
            q_idx = room["current_q"]
            if q_idx < len(QUESTIONS):
                q = QUESTIONS[q_idx]

                st.markdown(f"""
                <div class="soft-card">
                    <span class="theme-pill">{q['theme']}</span>
                    <h4>Pergunta {q_idx + 1} de {len(QUESTIONS)}</h4>
                    <p style="font-size: 1.15rem; font-weight: 700; color: #1E293B; margin-top: 0.5rem; line-height: 1.4;">
                        {q['question']}
                    </p>
                </div>
                """, unsafe_allow_html=True)

                q_answers = room["answers"].setdefault(q_idx, {})
                already_answered = player_name in q_answers

                if room["state"] == "QUESTION" and not already_answered:
                    st.write("**Escolha sua alternativa:**")
                    symbols = ["▲", "◆", "●", "■"]
                    for idx, opt_text in enumerate(q["options"]):
                        if st.button(f"{symbols[idx]} {opt_text}", key=f"opt_btn_{idx}", use_container_width=True):
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
                        st.info("✓ **Resposta enviada!** Aguardando o apresentador revelar no telão...")
                        if st.button("🔄 Atualizar tela", use_container_width=True):
                            st.rerun()
                    else:
                        if ans["correct"]:
                            st.balloons()
                            st.success(f"🎉 **Você Acertou!** (+{ans['points']} pts)")
                        else:
                            st.error("😅 **Não foi dessa vez!** (+0 pts)")

                        st.markdown(f"""
                        <div class="soft-card" style="background: #F0FDF4; border-color: #BBF7D0;">
                            <strong style="color: #166534;">💡 Explicação Didática:</strong>
                            <p style="color: #15803D; margin-top: 0.3rem;">{q['explanation']}</p>
                        </div>
                        """, unsafe_allow_html=True)

                        if st.button("🔄 Próxima Rodada", use_container_width=True):
                            st.rerun()

        elif room["state"] == "PODIUM":
            st.markdown("""
            <div class="soft-card" style="text-align: center; padding: 2rem;">
                <div style="font-size: 3.5rem;">🏆</div>
                <h2>Fim do Quiz!</h2>
                <p style="color: #64748B
