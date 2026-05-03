import streamlit as st
import streamlit.components.v1 as components
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from dotenv import load_dotenv
load_dotenv()
import os

# ─────────────────────────────────────────────
#  Page Config
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="RestaurantAI — Name Generator",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
#  Global CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=DM+Sans:wght@300;400;500&display=swap');

:root {
    --cream:   #FAF7F2;
    --charcoal:#1C1917;
    --amber:   #D97706;
    --amber-lt:#FDE68A;
    --rust:    #B45309;
    --sage:    #4B5563;
    --card-bg: #FFFFFF;
    --border:  #E5DDD0;
    --radius:  16px;
    --shadow:  0 4px 24px rgba(28,25,23,.08);
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--cream) !important;
    color: var(--charcoal);
}

#MainMenu, footer, header { visibility: hidden; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: var(--charcoal) !important;
    border-right: none;
}
[data-testid="stSidebar"] * { color: var(--cream) !important; }
[data-testid="stSidebar"] .stSelectbox > div > div,
[data-testid="stSidebar"] select {
    background: #2C2825 !important;
    border: 1px solid #3D3733 !important;
    border-radius: 8px !important;
    color: var(--cream) !important;
}
[data-testid="stSidebar"] .stRadio > div { gap: 8px; }
[data-testid="stSidebar"] .stRadio [data-baseweb="radio"] {
    background: #2C2825;
    border: 1px solid #3D3733;
    border-radius: 8px;
    padding: 8px 14px;
    transition: background .2s;
}
[data-testid="stSidebar"] .stRadio [data-baseweb="radio"]:has(input:checked) {
    background: var(--amber) !important;
    border-color: var(--amber) !important;
}
[data-testid="stSidebarCollapseButton"] button {
    background: transparent !important;
    border: 1px solid #3D3733 !important;
    border-radius: 8px !important;
    color: #9C8E80 !important;
}
[data-testid="stSidebarCollapseButton"] button:hover { background: #2C2825 !important; }

/* Generate button */
[data-testid="stSidebar"] .stButton > button {
    width: 100%;
    background: linear-gradient(135deg, var(--amber), var(--rust));
    color: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 14px !important;
    font-family: 'DM Sans', sans-serif;
    font-weight: 500;
    font-size: 1rem;
    letter-spacing: .04em;
    cursor: pointer;
    transition: opacity .2s, transform .15s;
    margin-top: 8px;
}
[data-testid="stSidebar"] .stButton > button:hover { opacity: .88; transform: translateY(-1px); }
[data-testid="stSidebar"] .stButton > button:active { transform: translateY(0); }

/* Main content */
.block-container { padding: 2.5rem 3rem 4rem !important; max-width: 860px; }

/* Hero */
.hero-header { text-align: center; padding: 48px 0 36px; border-bottom: 1px solid var(--border); margin-bottom: 40px; }
.hero-header .eyebrow { font-size: .72rem; font-weight: 500; letter-spacing: .18em; text-transform: uppercase; color: var(--amber); margin-bottom: 12px; }
.hero-header h1 { font-family: 'Playfair Display', serif; font-size: clamp(2rem, 5vw, 3.2rem); font-weight: 700; color: var(--charcoal); line-height: 1.15; margin: 0 0 10px; }
.hero-header .sub { font-size: .95rem; color: var(--sage); font-weight: 300; }

/* Cards */
.result-card { background: var(--card-bg); border: 1px solid var(--border); border-radius: var(--radius); padding: 36px 40px; margin-bottom: 28px; box-shadow: var(--shadow); position: relative; overflow: hidden; }
.result-card::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 4px; background: linear-gradient(90deg, var(--amber), var(--rust)); }
.section-label { font-size: .7rem; font-weight: 500; letter-spacing: .16em; text-transform: uppercase; color: var(--amber); margin-bottom: 14px; display: flex; align-items: center; gap: 8px; }
.section-label::after { content: ''; flex: 1; height: 1px; background: var(--border); }
.restaurant-name { font-family: 'Playfair Display', serif; font-size: clamp(2rem, 4vw, 3rem); font-weight: 700; color: var(--charcoal); line-height: 1.1; margin: 0 0 6px; }
.tagline-text { font-family: 'Playfair Display', serif; font-style: italic; font-size: 1.35rem; color: var(--rust); line-height: 1.45; }
.menu-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-top: 4px; }
.menu-item { background: var(--cream); border: 1px solid var(--border); border-radius: 10px; padding: 14px 18px; display: flex; align-items: center; gap: 12px; font-size: .92rem; color: var(--rust) !important; font-weight: 500; }
.menu-item:hover { border-color: var(--amber); box-shadow: 0 2px 12px rgba(217,119,6,.1); }
.menu-item .num { background: linear-gradient(135deg, var(--amber), var(--rust)); color: #fff; font-size: .7rem; font-weight: 600; width: 24px; height: 24px; border-radius: 50%; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
.badge { display: inline-block; background: var(--amber-lt); color: var(--rust); border-radius: 20px; padding: 4px 14px; font-size: .75rem; font-weight: 500; margin-top: 2px; }
.empty-state { text-align: center; padding: 80px 40px; color: var(--sage); }
.empty-state .big-icon { font-size: 4rem; margin-bottom: 16px; }
.empty-state h3 { font-family: 'Playfair Display', serif; font-size: 1.5rem; color: var(--charcoal); margin-bottom: 8px; }
.empty-state p { font-size: .9rem; font-weight: 300; }
.stSpinner > div { border-color: var(--amber) transparent transparent transparent !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  Sidebar Reopen Button via components.html
#  This runs in its OWN iframe, so window.parent
#  gives us direct access to the top document —
#  bypassing the st.markdown sandbox restriction.
# ─────────────────────────────────────────────
components.html("""
<script>
(function () {
    var topDoc = window.parent.document;

    /* --- inject the floating button into the TOP page --- */
    function injectBtn() {
        if (topDoc.getElementById('_rst_open_btn')) return;
        var btn = topDoc.createElement('button');
        btn.id = '_rst_open_btn';
        btn.title = 'Open sidebar';
        btn.textContent = '\u2630';          /* ☰ */
        var s = btn.style;
        s.cssText = [
            'position:fixed', 'top:50vh', 'left:0',
            'transform:translateY(-50%)',
            'z-index:2147483647',
            'background:linear-gradient(160deg,#D97706,#B45309)',
            'color:#fff', 'border:none',
            'border-radius:0 14px 14px 0',
            'width:38px', 'min-height:72px',
            'font-size:1.4rem', 'line-height:1',
            'cursor:pointer', 'display:none',
            'align-items:center', 'justify-content:center',
            'box-shadow:4px 0 20px rgba(217,119,6,.55)',
            'transition:width .2s,box-shadow .2s',
            'padding:0'
        ].join(';');

        btn.addEventListener('mouseenter', function () {
            btn.style.width = '50px';
            btn.style.boxShadow = '6px 0 28px rgba(217,119,6,.75)';
        });
        btn.addEventListener('mouseleave', function () {
            btn.style.width = '38px';
            btn.style.boxShadow = '4px 0 20px rgba(217,119,6,.55)';
        });
        btn.addEventListener('click', function () {
            clickSidebarToggle();
            setTimeout(syncBtn, 400);
        });
        topDoc.body.appendChild(btn);
    }

    /* --- find and click whatever Streamlit uses to open sidebar --- */
    function clickSidebarToggle() {
        var tries = [
            '[data-testid="collapsedControl"]',
            '[data-testid="stSidebarCollapsedControl"]',
            'button[aria-label="Open sidebar"]',
            'button[aria-label="open sidebar"]',
            'button[aria-label="Show sidebar"]',
            'section[data-testid="stSidebar"] ~ div button',
        ];
        for (var i = 0; i < tries.length; i++) {
            var el = topDoc.querySelector(tries[i]);
            if (el) { el.click(); return; }
        }
    }

    /* --- show button only when sidebar is collapsed (<40px wide) --- */
    function isSidebarHidden() {
        var sb = topDoc.querySelector('[data-testid="stSidebar"]');
        if (!sb) return false;
        return sb.getBoundingClientRect().width < 40;
    }

    function syncBtn() {
        var btn = topDoc.getElementById('_rst_open_btn');
        if (!btn) return;
        btn.style.display = isSidebarHidden() ? 'flex' : 'none';
    }

    /* --- bootstrap --- */
    function boot() {
        injectBtn();
        syncBtn();

        /* Watch sidebar resize */
        var sb = topDoc.querySelector('[data-testid="stSidebar"]');
        if (sb && window.ResizeObserver) {
            new ResizeObserver(syncBtn).observe(sb);
        }

        /* Fallback polling every 600 ms */
        setInterval(syncBtn, 600);
    }

    /* Wait until stSidebar exists in the top doc */
    var poll = setInterval(function () {
        if (topDoc.querySelector('[data-testid="stSidebar"]')) {
            clearInterval(poll);
            boot();
        }
    }, 250);
})();
</script>
""", height=0)


# ─────────────────────────────────────────────
#  Hero Header
# ─────────────────────────────────────────────
st.markdown("""
<div class="hero-header">
    <p class="eyebrow">✦ AI-Powered Branding ✦</p>
    <h1>Restaurant Name Generator</h1>
    <p class="sub">Craft the perfect identity for your culinary concept — in seconds.</p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  Sidebar
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding:28px 0 20px; text-align:center;">
        <span style="font-size:2.2rem;">🍽️</span>
        <p style="font-family:'Playfair Display',serif; font-size:1.2rem; color:#FAF7F2; margin:6px 0 0;">RestaurantAI</p>
        <p style="font-size:.72rem; color:#9C8E80; letter-spacing:.12em; text-transform:uppercase;">Brand Studio</p>
    </div>
    <hr style="border:none; border-top:1px solid #3D3733; margin-bottom:24px;">
    """, unsafe_allow_html=True)

    st.markdown('<p style="font-size:.72rem; color:#9C8E80; letter-spacing:.12em; text-transform:uppercase; margin-bottom:6px;">Cuisine Type</p>', unsafe_allow_html=True)
    cuisine = st.selectbox(
        "Cuisine",
        ("Indian","Italian","Mexican","Russian","Japanese","Chinese","American",
         "Pakistani","Arabian","Canadian","Thai","Korean","French","Mediterranean",
         "Spanish","Greek","Turkish","Lebanese","Vietnamese",
         "Brazilian","German","Ethiopian","Moroccan","Indonesian","Caribbean"),
        label_visibility="collapsed"
    )

    st.markdown('<p style="font-size:.72rem; color:#9C8E80; letter-spacing:.12em; text-transform:uppercase; margin:20px 0 6px;">Food Preference</p>', unsafe_allow_html=True)
    food_type = st.radio(
        "Food Preference",
        ["Veg 🥦", "Non-Veg 🍗", "Both 🍱"],
        label_visibility="collapsed"
    )
    food_type_clean = food_type.split(" ")[0]

    st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)
    generate = st.button("✨ Generate Brand Identity", use_container_width=True)

    st.markdown("""
    <hr style="border:none; border-top:1px solid #3D3733; margin:28px 0 16px;">
    <p style="font-size:.72rem; color:#6B6057; text-align:center; line-height:1.6;">
        Powered by LLaMA 3.1 via Groq<br>Built with LangChain + Streamlit
    </p>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  LLM Setup
# ─────────────────────────────────────────────
llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model="llama-3.1-8b-instant"
)

prompt1 = PromptTemplate.from_template(
    "Suggest ONE fancy name for a {cuisine} restaurant. Only return the name, nothing else."
)
prompt2 = PromptTemplate.from_template(
    """Suggest exactly 5 popular {food_type} food items for a restaurant named {restaurant_name}.

Rules:
- Only return a numbered list
- No preamble, no extra sentences

Format:
1. item
2. item
3. item
4. item
5. item"""
)
prompt3 = PromptTemplate.from_template(
    "Write ONE short catchy tagline (under 12 words) for a restaurant named {restaurant_name}. Only return the tagline, no quotes."
)

# ─────────────────────────────────────────────
#  Generate & Render
# ─────────────────────────────────────────────
if generate:
    with st.spinner("Crafting your restaurant identity…"):
        restaurant_name = (prompt1 | llm).invoke({"cuisine": cuisine}).content.strip()
        food_items_raw  = (prompt2 | llm).invoke({"restaurant_name": restaurant_name, "food_type": food_type_clean}).content
        tagline         = (prompt3 | llm).invoke({"restaurant_name": restaurant_name}).content.strip().replace('"','')

    items = []
    for line in food_items_raw.split("\n"):
        line = line.strip()
        if not line or "here are" in line.lower():
            continue
        if "." in line:
            line = line.split(".", 1)[1].strip()
        if line:
            items.append(line)
    items = items[:5]

    st.markdown(f"""
    <div class="result-card">
        <div class="section-label">🏷️ Restaurant Name</div>
        <p class="restaurant-name">{restaurant_name}</p>
        <p class="restaurant-meta">
            <span class="badge">{cuisine}</span>&nbsp;
            <span class="badge">{food_type}</span>
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="result-card">
        <div class="section-label">✨ Brand Tagline</div>
        <p class="tagline-text">"{tagline}"</p>
    </div>
    """, unsafe_allow_html=True)

    items_html = "".join([
        f'<div class="menu-item"><span class="num">{i+1}</span>{item}</div>'
        for i, item in enumerate(items)
    ])
    st.markdown(f"""
    <div class="result-card">
        <div class="section-label">🍛 Signature Menu Items</div>
        <div class="menu-grid">{items_html}</div>
    </div>
    """, unsafe_allow_html=True)

else:
    st.markdown("""
    <div class="empty-state">
        <div class="big-icon">🍴</div>
        <h3>Your Brand Awaits</h3>
        <p>Select a cuisine and food preference in the sidebar,<br>then hit <strong>Generate</strong> to craft your restaurant identity.</p>
    </div>
    """, unsafe_allow_html=True)
