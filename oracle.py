import sys
from pathlib import Path
ROOT_DIR = Path(__file__).parent.resolve()
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import random
import datetime
import common_ui


# ══════════════════════════════════════════════════════════════════════
#  ORACLE DECK  –  16 Arcana do Grimório
#
#  Cards 1-8  → Rei Joaquim   (wisdom, patience, ancestral guidance)
#  Cards 9-16 → Princesa Guerreira  (courage, strength, transformation)
# ══════════════════════════════════════════════════════════════════════

ARCANA = [
    # ── Rei Joaquim ────────────────────────────────────────────────
    {
        "id": 1,
        "nome": "O Conselho do Ancião",
        "entidade": "Rei Joaquim",
        "elemento": "Terra",
        "emoji_entidade": "👑",
        "mensagem": (
            "A sabedoria não se encontra na pressa, meu filho. "
            "Sente-se à sombra da árvore antiga e escute o que o silêncio "
            "tem a dizer. As respostas que você busca já moram dentro de você."
        ),
        "conselho": (
            "Dedique tempo à reflexão antes de tomar qualquer decisão importante. "
            "Consulte os mais velhos e honre a experiência daqueles que vieram antes."
        ),
        "palavras": ["paciência", "sabedoria", "silêncio", "ancestralidade"],
    },
    {
        "id": 2,
        "nome": "A Coroa de Espinhos",
        "entidade": "Rei Joaquim",
        "elemento": "Terra",
        "emoji_entidade": "👑",
        "mensagem": (
            "Todo reinado cobra seu preço. Os espinhos que perfuram "
            "a fronte do rei são as dores que ele carrega por seu povo. "
            "Aceite o peso de suas responsabilidades com dignidade."
        ),
        "conselho": (
            "Não fuja das dificuldades que acompanham suas conquistas. "
            "A verdadeira nobreza está em servir mesmo quando dói."
        ),
        "palavras": ["sacrifício", "dever", "resiliência", "nobreza"],
    },
    {
        "id": 3,
        "nome": "O Cachimbo Sagrado",
        "entidade": "Rei Joaquim",
        "elemento": "Ar",
        "emoji_entidade": "👑",
        "mensagem": (
            "A fumaça que sobe carrega suas preces ao céu. "
            "Respire fundo, acalme a mente e deixe a fumaça "
            "limpar os caminhos bloqueados. Clareza virá."
        ),
        "conselho": (
            "Pratique a meditação e a oração. Afaste-se do barulho "
            "do mundo para encontrar sua voz interior."
        ),
        "palavras": ["meditação", "clareza", "purificação", "oração"],
    },
    {
        "id": 4,
        "nome": "A Raiz Profunda",
        "entidade": "Rei Joaquim",
        "elemento": "Terra",
        "emoji_entidade": "👑",
        "mensagem": (
            "A árvore que resiste à tempestade é aquela cujas raízes "
            "alcançam as águas profundas. Conheça suas origens, "
            "honre seus ancestrais, e nenhuma ventania o derrubará."
        ),
        "conselho": (
            "Reconecte-se com suas raízes familiares e espirituais. "
            "Fortaleça os alicerces antes de construir mais alto."
        ),
        "palavras": ["raízes", "ancestrais", "fundação", "firmeza"],
    },
    {
        "id": 5,
        "nome": "O Bastão de Mando",
        "entidade": "Rei Joaquim",
        "elemento": "Fogo",
        "emoji_entidade": "👑",
        "mensagem": (
            "O bastão não confere poder a quem o segura — ele revela "
            "o poder que já existe. Assuma a liderança que lhe cabe. "
            "O povo precisa da sua voz."
        ),
        "conselho": (
            "É hora de liderar com firmeza e compaixão. "
            "Não espere permissão para ocupar seu lugar de direito."
        ),
        "palavras": ["liderança", "autoridade", "propósito", "comando"],
    },
    {
        "id": 6,
        "nome": "A Benção do Preto Velho",
        "entidade": "Rei Joaquim",
        "elemento": "Água",
        "emoji_entidade": "👑",
        "mensagem": (
            "Estenda as mãos, receba a benção. As lágrimas do passado "
            "regam as flores do futuro. Você está protegido por forças "
            "que seus olhos não podem ver."
        ),
        "conselho": (
            "Abra o coração para receber ajuda espiritual. "
            "Pratique a gratidão e retribua as bençãos recebidas."
        ),
        "palavras": ["proteção", "benção", "gratidão", "amparo"],
    },
    {
        "id": 7,
        "nome": "O Terreiro Iluminado",
        "entidade": "Rei Joaquim",
        "elemento": "Fogo",
        "emoji_entidade": "👑",
        "mensagem": (
            "O chão onde seus pés pisam é sagrado. Não procure templos "
            "distantes quando o divino habita em cada grão de terra "
            "sob seus pés. Sacraliza onde estiver."
        ),
        "conselho": (
            "Crie espaço sagrado ao seu redor, onde quer que esteja. "
            "A espiritualidade é vivida no cotidiano."
        ),
        "palavras": ["sagrado", "presença", "ritual", "cotidiano"],
    },
    {
        "id": 8,
        "nome": "A Palavra Encantada",
        "entidade": "Rei Joaquim",
        "elemento": "Ar",
        "emoji_entidade": "👑",
        "mensagem": (
            "Cuidado com o que a boca pronuncia, pois a palavra do sábio "
            "cria e destrói mundos. Fale com intenção, abençoe com a voz, "
            "e nunca subestime o poder de um bom conselho."
        ),
        "conselho": (
            "Escolha suas palavras com cuidado. Use a fala para curar, "
            "aconselhar e edificar. O silêncio também é uma forma de sabedoria."
        ),
        "palavras": ["palavra", "intenção", "cura verbal", "sabedoria oral"],
    },

    # ── Princesa Guerreira ─────────────────────────────────────────
    {
        "id": 9,
        "nome": "A Espada Flamejante",
        "entidade": "Princesa Guerreira",
        "elemento": "Fogo",
        "emoji_entidade": "⚔️",
        "mensagem": (
            "A lâmina que arde não conhece o medo. Levante-se, "
            "empunhe sua espada e corte os laços que o aprisionam. "
            "A batalha exige coragem, e você a possui."
        ),
        "conselho": (
            "Enfrente seus medos de frente. Não é hora de recuar — "
            "a vitória pertence a quem ousa avançar."
        ),
        "palavras": ["coragem", "batalha", "libertação", "ação"],
    },
    {
        "id": 10,
        "nome": "O Escudo de Luz",
        "entidade": "Princesa Guerreira",
        "elemento": "Ar",
        "emoji_entidade": "⚔️",
        "mensagem": (
            "Nem toda batalha se vence atacando. Às vezes a maior "
            "demonstração de força é saber se defender sem perder "
            "a compaixão. Proteja-se, mas não se feche."
        ),
        "conselho": (
            "Estabeleça limites saudáveis. Proteja sua energia "
            "sem se isolar do mundo. A defesa inteligente é uma arte."
        ),
        "palavras": ["proteção", "limites", "defesa", "discernimento"],
    },
    {
        "id": 11,
        "nome": "A Dança dos Ventos",
        "entidade": "Princesa Guerreira",
        "elemento": "Ar",
        "emoji_entidade": "⚔️",
        "mensagem": (
            "Como o vento que muda de direção sem aviso, "
            "a transformação chega para rearranjar sua vida. "
            "Não resista — dance com a mudança e encontre novo ritmo."
        ),
        "conselho": (
            "Aceite as transformações em curso. Flexibilidade "
            "e adaptação são as armas mais poderosas que você pode ter."
        ),
        "palavras": ["transformação", "mudança", "adaptação", "fluxo"],
    },
    {
        "id": 12,
        "nome": "O Grito de Guerra",
        "entidade": "Princesa Guerreira",
        "elemento": "Fogo",
        "emoji_entidade": "⚔️",
        "mensagem": (
            "Sua voz é sua arma mais poderosa! Não engula suas verdades — "
            "grite-as ao mundo se for preciso. O silêncio de quem deveria "
            "falar é a arma do opressor."
        ),
        "conselho": (
            "Fale! Defenda suas ideias, seus direitos e os daqueles que "
            "não podem se defender. Sua voz importa."
        ),
        "palavras": ["voz", "verdade", "justiça", "expressão"],
    },
    {
        "id": 13,
        "nome": "A Coroa de Vitória",
        "entidade": "Princesa Guerreira",
        "elemento": "Terra",
        "emoji_entidade": "⚔️",
        "mensagem": (
            "A vitória já está escrita nas estrelas, mas cabe a você "
            "percorrer o caminho até ela. Cada passo dado com fé "
            "aproxima você da coroa que lhe pertence."
        ),
        "conselho": (
            "Persista! O triunfo está mais perto do que imagina. "
            "Celebre cada pequena conquista no caminho."
        ),
        "palavras": ["vitória", "triunfo", "perseverança", "conquista"],
    },
    {
        "id": 14,
        "nome": "As Chamas Purificadoras",
        "entidade": "Princesa Guerreira",
        "elemento": "Fogo",
        "emoji_entidade": "⚔️",
        "mensagem": (
            "O fogo que destrói é o mesmo que purifica. "
            "Deixe arder o que não lhe serve mais — relacionamentos "
            "tóxicos, crenças limitantes, hábitos destrutivos."
        ),
        "conselho": (
            "Faça uma limpeza profunda em sua vida. Libere o que está "
            "estagnado para abrir espaço ao novo e sagrado."
        ),
        "palavras": ["purificação", "renovação", "limpeza", "renascimento"],
    },
    {
        "id": 15,
        "nome": "O Caminho da Floresta",
        "entidade": "Princesa Guerreira",
        "elemento": "Terra",
        "emoji_entidade": "⚔️",
        "mensagem": (
            "Na escuridão da floresta densa, a guerreira não precisa "
            "ver o destino — ela confia em seus instintos. "
            "Confie no que seu coração sabe, mesmo sem enxergar o fim."
        ),
        "conselho": (
            "Siga sua intuição. Nem todos os caminhos são claros, "
            "mas sua bússola interna sabe o rumo certo."
        ),
        "palavras": ["intuição", "confiança", "caminho", "mistério"],
    },
    {
        "id": 16,
        "nome": "A Estrela Guia",
        "entidade": "Princesa Guerreira",
        "elemento": "Água",
        "emoji_entidade": "⚔️",
        "mensagem": (
            "Olhe para o alto! Mesmo na noite mais escura, "
            "há uma estrela que brilha só para você. "
            "A orientação divina está presente — basta levantar os olhos."
        ),
        "conselho": (
            "Busque orientação espiritual e confie na proteção dos guias. "
            "Você nunca caminha sozinho(a)."
        ),
        "palavras": ["guia", "esperança", "direção divina", "fé"],
    },
]


# ── Element visual mapping ────────────────────────────────────────────

ELEMENTOS = {
    "Fogo":  {"emoji": "🔥", "cor": "#DC143C"},
    "Água":  {"emoji": "💧", "cor": "#1E90FF"},
    "Terra": {"emoji": "🌿", "cor": "#2ECC71"},
    "Ar":    {"emoji": "💨", "cor": "#C0C0C0"},
}


# ── Moon-phase spiritual influence ────────────────────────────────────

INFLUENCIA_LUNAR = {
    "Nova": {
        "energia": "Introspecção e novos começos",
        "conselho": (
            "Lua Nova: momento de plantar sementes de intenção. "
            "Recolha-se, medite e trace novos planos."
        ),
    },
    "Crescente": {
        "energia": "Crescimento e construção",
        "conselho": (
            "Lua Crescente: a energia cresce — hora de agir sobre "
            "os planos traçados e construir com determinação."
        ),
    },
    "Quarto Crescente": {
        "energia": "Decisão e comprometimento",
        "conselho": (
            "Quarto Crescente: momento de tomar decisões firmes. "
            "Supere obstáculos e reafirme seus compromissos."
        ),
    },
    "Gibosa Crescente": {
        "energia": "Refinamento e ajustes",
        "conselho": (
            "Gibosa Crescente: refine seus esforços. Ajuste o rumo "
            "e prepare-se para a plenitude que se aproxima."
        ),
    },
    "Cheia": {
        "energia": "Plenitude e revelação",
        "conselho": (
            "Lua Cheia: tudo se revela sob esta luz. Celebre conquistas, "
            "mas atenção às emoções intensificadas."
        ),
    },
    "Gibosa Minguante": {
        "energia": "Gratidão e partilha",
        "conselho": (
            "Gibosa Minguante: hora de agradecer e compartilhar. "
            "Distribua os frutos das suas colheitas."
        ),
    },
    "Quarto Minguante": {
        "energia": "Liberação e perdão",
        "conselho": (
            "Quarto Minguante: libere mágoas, perdoe e solte "
            "o que já cumpriu seu propósito em sua vida."
        ),
    },
    "Minguante": {
        "energia": "Descanso e preparação",
        "conselho": (
            "Lua Minguante: descanse, purifique-se e prepare o terreno "
            "para o novo ciclo que se aproxima."
        ),
    },
}


# ══════════════════════════════════════════════════════════════════════
#  PUBLIC API
# ══════════════════════════════════════════════════════════════════════

def draw_card():
    """Draw a single random arcanum from the deck."""
    return random.choice(ARCANA)


def get_moon_influence():
    """Current moon phase with its spiritual influence text."""
    phase = common_ui.get_moon_phase()
    influence = INFLUENCIA_LUNAR.get(phase["name"], INFLUENCIA_LUNAR["Nova"])
    return {"phase": phase, "influence": influence}


def build_full_reading():
    """Assemble a complete oracle reading (card + moon + timestamp)."""
    card = draw_card()
    moon = get_moon_influence()
    return {
        "card": card,
        "moon": moon,
        "timestamp": datetime.datetime.now().isoformat(),
        "illumination": common_ui.get_moon_illumination(),
    }
