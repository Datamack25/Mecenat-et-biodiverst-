import base64, csv, datetime, json, os
from pathlib import Path
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
import core
from hero import HERO_SVG
import html as _html, random, urllib.parse
import content
import pdf_export as px

PLATFORM_NAME = "Veille Outre-mer · Biodiversité · Insertion · Mécénat"  # <- modifiez ici le nom de la plateforme
JOURS = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"]
MOIS = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre", "novembre", "décembre"]

st.set_page_config(page_title="Veille Outre-mer", page_icon="🌴", layout="wide", initial_sidebar_state="collapsed")
content.ensure(core)

def paris(dt=None):
    try:
        from zoneinfo import ZoneInfo
        return (dt or datetime.datetime.now(datetime.timezone.utc)).astimezone(ZoneInfo("Europe/Paris"))
    except Exception:
        return dt or datetime.datetime.now()

def today_fr():
    n = paris()
    return f"{JOURS[n.weekday()]} {n.day} {MOIS[n.month - 1]} {n.year}"

def fmt_upd(iso):
    try:
        return paris(datetime.datetime.fromisoformat(iso.replace("Z", "+00:00"))).strftime("%d/%m/%Y %H:%M")
    except Exception:
        return "jamais"

def run(kind):
    try:
        if "ANTHROPIC_API_KEY" in st.secrets:
            os.environ["ANTHROPIC_API_KEY"] = st.secrets["ANTHROPIC_API_KEY"]
    except Exception:
        pass
    if kind == "news":
        n, errs = core.fetch_news()
        msg = f"{n} articles collectés" + (f" (erreurs : {' | '.join(errs[:2])})" if errs else "")
    else:
        msg = core.enrich()
    st.cache_data.clear()
    return msg

@st.cache_data(ttl=600)
def load_news():
    try:
        return json.load(open(core.DATA / "news.json", encoding="utf-8"))
    except Exception:
        return {"updated": None, "items": []}

@st.cache_data(ttl=600)
def load_enc():
    try:
        E = pd.read_csv(core.CSV, on_bad_lines="skip").fillna("")
    except Exception:
        E = pd.DataFrame(core.D.ENC_ROWS, columns=core.H)
    for c in core.H:
        if c not in E:
            E[c] = ""
    return E.astype(str)

@st.cache_data
def load_actors():
    try:
        return json.load(open(core.DATA / "acteurs.json", encoding="utf-8"))
    except Exception:
        return core.D.ACTORS

APP_VERSION = "3.1 · 09/10/2026"
PAGES = ["🏠 Accueil", "📰 Actualités", "🏛️ Fondations & acteurs", "💼 Emplois", "📚 Encyclopédie", "📖 Lectures & textes", "🗺️ Territoires", "🧰 Boîtes à outils"]
TH = {"outremer": "Outre-mer", "biodiversite": "Biodiversité", "insertion": "Insertion pro", "mecenat": "Mécénat", "rse": "RSE / réglementaire", "emploi": "Emploi", "fondations": "Fondations", "competences": "Mécénat de compétences", "philanthropie": "Philanthropie / emploi"}
e = lambda x: _html.escape(str("" if x is None else x), quote=True)

CSS = """<style>
:root{color-scheme:light}
#MainMenu,footer,[data-testid="stToolbar"],[data-testid="stDecoration"]{display:none!important}
header[data-testid="stHeader"]{background:transparent!important;height:0!important;min-height:0!important;overflow:visible}
.block-container,[data-testid="stMainBlockContainer"]{padding:0 5vw 0!important;max-width:100%!important}
.stApp{background:#f4f8f6}
.st-key-maj{position:fixed;top:9px;right:18px;z-index:99999;width:auto!important}
.st-key-maj button{background:#0e7c66;border:0;border-radius:22px;font-weight:700;padding:6px 18px}.st-key-maj button,.st-key-maj button *{color:#fff!important}
.st-key-page{margin:0 -5vw 0;padding:10px 5vw;padding-right:270px;background:#fff;border-bottom:1px solid #dfe9e5}
.st-key-page div[role="radiogroup"]{gap:6px;flex-wrap:wrap}
.st-key-page label{background:#f4f8f6;border:1px solid #dfe9e5;border-radius:22px;padding:5px 14px;cursor:pointer}
.st-key-page label>div:first-child{display:none}
.st-key-page label:has(input:checked){background:#0e7c66;border-color:#0e7c66}.st-key-page label:has(input:checked) p{color:#fff!important}
[data-testid="stSidebarCollapsedControl"],[data-testid="collapsedControl"],[data-testid="stExpandSidebarButton"]{position:fixed!important;top:64px;left:0;z-index:100000;background:#0e7c66;border-radius:0 12px 12px 0;padding:4px 6px}
[data-testid="stSidebarCollapsedControl"] *,[data-testid="collapsedControl"] *,[data-testid="stExpandSidebarButton"] *{color:#fff!important;fill:#fff!important}
[data-testid="stSidebar"]{background:#fff!important;border-right:1px solid #dfe9e5}
.stApp,[data-testid="stSidebar"] *,[data-testid="stExpander"] summary *,label,[data-testid="stCaptionContainer"],[data-testid="stMetricValue"],[data-testid="stMetricLabel"],button[role="tab"],[data-testid="stMarkdownContainer"] p,h1,h2,h3{color:#13231f!important}
input,textarea,[data-baseweb="input"],[data-baseweb="textarea"],[data-baseweb="select"]>div{background:#fff!important;color:#13231f!important}
.hero{position:relative;overflow:hidden;margin:0 -5vw;padding:78px 5vw 130px;background:linear-gradient(135deg,#06483b,#0e7c66 55%,#2aa8a0)}
.hero .art{position:absolute;inset:0;background-repeat:no-repeat;background-position:right bottom;background-size:auto 100%}
.hero .sl{position:absolute;inset:0;background-size:cover;background-position:center;opacity:0}.hero .ov{position:absolute;inset:0;background:linear-gradient(rgba(6,72,59,.72),rgba(14,124,102,.45))}
.hero h1,.hero p,.hero .pill{position:relative;color:#fff!important}.hero h1{font-size:clamp(1.9rem,4vw,3rem);line-height:1.12;margin:12px 0 14px;max-width:620px;font-weight:800;padding:0}
.hero p{max-width:540px;font-size:1.05rem}.pill{display:inline-block;background:rgba(255,255,255,.2);padding:5px 14px;border-radius:20px;font-size:.85rem}
.ph{margin:0 -5vw 14px;padding:38px 5vw;background:linear-gradient(135deg,#06483b,#0e7c66)}.ph h1,.ph p{color:#fff!important;margin:0 0 4px;padding:0}.ph h1{font-size:2rem}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:14px;margin:-70px 0 10px;position:relative;z-index:2}
.stat{background:#fff;border-radius:16px;padding:18px;text-align:center;box-shadow:0 8px 24px rgba(6,72,59,.13)}.stat b{display:block;font-size:1.8rem;color:#0e7c66!important;font-weight:800}.stat span{color:#5d6f69;font-size:.85rem}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:16px;margin:8px 0}.grid.sm{grid-template-columns:repeat(auto-fill,minmax(210px,1fr))}
.card{background:#fff;border:1px solid #dfe9e5;border-radius:16px;padding:18px;box-shadow:0 2px 8px rgba(0,0,0,.04)}
.card h3{margin:9px 0 6px;font-size:1.02rem;line-height:1.35;padding:0}.card h3 a{text-decoration:none;color:#13231f!important}.card p{margin:6px 0;font-size:.93rem}
.ex{background:#eef7f3;border-left:3px solid #0e7c66;padding:7px 10px;border-radius:6px;font-size:.88rem}.meta{color:#5d6f69!important;font-size:.8rem;margin-top:6px}
.tag{display:inline-block;background:#e3f3ee;color:#0e7c66!important;border-radius:12px;padding:2px 10px;font-size:.75rem;font-weight:700;margin:0 5px 4px 0}.tag.p{background:#fff1e0;color:#b25e00!important}
.st-key-tools{padding-bottom:20px}
.creator{background:#06483b;margin:30px -5vw 0;text-align:center;padding:26px 5vw;font-size:.92rem;line-height:1.7}.creator,.creator *{color:#fff!important}
@media(max-width:800px){.st-key-maj{top:auto;bottom:16px;right:16px}.st-key-page{padding-right:5vw}}
</style>"""
st.markdown(CSS, unsafe_allow_html=True)

@st.cache_data
def _photo(path, mtime):
    import io
    from PIL import Image, ImageOps
    im = ImageOps.exif_transpose(Image.open(path)).convert("RGB")
    im = ImageOps.fit(im, (1400, 560), Image.LANCZOS)  # recadrage automatique au format du bandeau
    b = io.BytesIO(); im.save(b, "JPEG", quality=72, optimize=True)
    return "data:image/jpeg;base64," + base64.b64encode(b.getvalue()).decode()

def load_photos():
    out = []
    for p in sorted((Path(__file__).parent / "assets").glob("hero*")):  # hero.jpg, hero1.jpg, hero2.jpg...
        if p.suffix.lower() in (".jpg", ".jpeg", ".png", ".webp"):
            try:
                out.append(_photo(str(p), p.stat().st_mtime))
            except Exception:
                pass
    return out[:6]

def hero_html():
    ph = load_photos(); n = len(ph)
    if n:
        x = 100 / n
        kf = f"<style>@keyframes hf{{0%{{opacity:0}}4%{{opacity:1}}{x:.1f}%{{opacity:1}}{x + 4:.1f}%{{opacity:0}}100%{{opacity:0}}}}</style>" if n > 1 else ""
        anim = lambda i: f"animation:hf {n * 5}s infinite;animation-delay:{i * 5}s;" if n > 1 else "opacity:1;"
        art = kf + "".join(f'<div class="sl" style="background-image:url({p});{anim(i)}"></div>' for i, p in enumerate(ph)) + '<div class="ov"></div>'
    else:
        art = f'<div class="art" style="background-image:url(&quot;data:image/svg+xml;utf8,{urllib.parse.quote(HERO_SVG)}&quot;)"></div>'
    return (f'<div class="hero">{art}<span class="pill">📅 {e(today_fr())}</span><h1>{e(PLATFORM_NAME)}</h1>'
            '<p>Actualités des territoires ultramarins, biodiversité, insertion professionnelle et mécénat : une veille quotidienne, un annuaire d\'acteurs et une encyclopédie.</p></div>')

def card(tags, title, body="", meta="", link=None, ex=""):
    t = "".join(f'<span class="tag{" p" if p else ""}">{e(x)}</span>' for x, p in tags)
    h = f'<a href="{e(link)}" target="_blank" rel="noopener">{e(title)}</a>' if link else e(title)
    return f'<div class="card">{t}<h3>{h}</h3>' + (f"<p>{e(body)}</p>" if body else "") + (f'<div class="ex">{ex}</div>' if ex else "") + (f'<div class="meta">{e(meta)}</div>' if meta else "") + "</div>"

def grid(cards, small=False):
    st.markdown(f'<div class="grid{" sm" if small else ""}">' + "".join(cards) + "</div>", unsafe_allow_html=True)

def banner(title, sub, pdf_key=None):
    st.markdown(f'<div class="ph"><h1>{e(title)}</h1><p>{e(sub)}</p></div>', unsafe_allow_html=True)
    if pdf_key:
        _, fn, pdf = PDFS[pdf_key]
        st.download_button("📄 Exporter cet onglet en PDF", pdf, f"{fn}.pdf", "application/pdf", key="dl_" + pdf_key)

def goto(p):
    st.session_state.page = p

flash = ""
if st.button("🔄 Mettre à jour la plateforme", key="maj"):
    with st.spinner("Mise à jour : actualités, puis encyclopédie…"):
        m_news = run("news")
        m_enc = run("enc")
    flash = f"✅ Mise à jour terminée le {today_fr()} · {m_news} · {m_enc}"
page = st.radio("Menu", PAGES, horizontal=True, key="page", label_visibility="collapsed")

N, A, E = load_news(), load_actors(), load_enc()
META = (PLATFORM_NAME, today_fr())
PDFS = {
    "news": ("Actualités", "actualites", px.cards_pdf("Actualités", [(n["title"], f'{n["theme"]} | {n["territory"]} | {n["source"]} | {(n["date"] or "")[:10]}', n["link"]) for n in N["items"][:300]], META)),
    "actors": ("Acteurs", "acteurs", px.cards_pdf("Acteurs de la biodiversité et de l'insertion", [(x["n"], f'{x["t"]} | {", ".join(x["d"])}', x["x"] + (f' ({x["u"]})' if x.get("u") else "")) for x in A], META)),
    "encyc": ("Encyclopédie", "encyclopedie", px.cards_pdf("Encyclopédie", [(r["terme"], r["categorie"], r["definition"] + (f' Exemple : {r["exemple"]}' if r["exemple"] else "")) for r in E.sort_values("terme").to_dict("records")], META)),
    "reads": ("Lectures", "lectures", px.cards_pdf("Fiches de lecture", [(r[2], f"{r[0]} | {r[1]} | {r[3]}", f"{r[4]} Pourquoi la lire : {r[5]}") for r in content.READS], META)),
    "geo": ("Territoires", "territoires", px.table_pdf("Territoires et communes", pd.DataFrame(content.geo_rows(), columns=["Territoire", "Commune", "Type", "Statut"]), META)),
    "jobs": ("Emplois", "emplois", px.cards_pdf("Emplois : intitulés et employeurs", [(j[0], j[1], "Employeurs : " + j[2]) for j in content.JOBS["titres"]] + [(r[0], f"{r[1]} | {r[2]}", "Postes : " + r[3]) for r in content.JOBS["recruteurs"]] + [(j[0], "Philanthropie et mécénat | " + j[1], "Employeurs : " + j[2]) for j in content.PHIL_JOBS["titres"]], META)),
    "found": ("Fondations", "fondations", px.cards_pdf("Fondations et intermédiaires du mécénat", [(f["n"], f["t"] + " | " + ", ".join(f["d"]), f["x"] + (" Engagement des collaborateurs : " + f["c"] + "." if f["c"] else "")) for f in content.FOUND + content.INTERMEDIARIES], META)),
    "regs": ("Réglementation", "reglementation", px.cards_pdf("RSE et réglementation", [(r[1], r[0], r[2]) for r in content.REGS], META)),
}

with st.sidebar:  # Administration : flèche verte en haut à gauche pour ouvrir ce volet
    st.subheader("⚙️ Administration")
    st.caption(f"{len(E)} termes · {len(A)} acteurs · {len(N['items'])} articles")
    st.download_button("⬇️ Encyclopédie (CSV)", open(core.CSV, "rb").read(), f"encyclopedie_{paris():%Y-%m-%d}.csv", "text/csv", key="dl_admin")
    with st.form("add", clear_on_submit=True):
        t = st.text_input("Terme"); c = st.text_input("Catégorie", "Concepts")
        de = st.text_area("Définition"); ex = st.text_input("Exemple")
        if st.form_submit_button("Ajouter à l'encyclopédie") and t and de:
            csv.writer(open(core.CSV, "a", encoding="utf-8", newline="")).writerow([t.strip(), c, de, ex, "Ajout manuel", datetime.date.today().isoformat()])
            st.cache_data.clear(); st.rerun()

TITLES = {"aap": "Appels à projets", "partenaires": "Suivi des partenaires", "mecenat_competences": "Mécénat de compétences", "grille_evaluation": "Grille d'évaluation des candidatures", "dpef_suivi": "Plan de rédaction DPEF"}

def tracker(key, cols, seed=None, cfg=None):
    path = core.DATA / f"{key}.csv"
    try:
        df = pd.read_csv(path).fillna("") if path.exists() else pd.DataFrame(seed or [], columns=cols)
    except Exception:
        df = pd.DataFrame(seed or [], columns=cols)
    ed = st.data_editor(df, num_rows="dynamic", width="stretch", key="ed_" + key, column_config=cfg or {})
    c1, c2, c3 = st.columns(3)
    if c1.button("💾 Enregistrer", key="sv_" + key):
        ed.to_csv(path, index=False); st.success("Enregistré (sur Streamlit Cloud, exportez le CSV pour le conserver durablement).")
    c2.download_button("⬇️ Exporter en CSV", ed.to_csv(index=False).encode(), f"{key}.csv", "text/csv", key="dl_" + key)
    c3.download_button("📄 Exporter en PDF", px.table_pdf(TITLES.get(key, key), ed, (PLATFORM_NAME, today_fr())), f"{key}.pdf", "application/pdf", key="pdf_" + key)
    return ed



if flash:
    st.success(flash)
ncard = lambda n: card([(TH.get(n["theme"], n["theme"]), 0), (n["territory"], 1)], n["title"], meta=f'{n["source"]} · {(n["date"] or "")[:10]}', link=n["link"])
NONE = '<div class="card">Aucun article pour le moment. Cliquez sur « Mettre à jour la plateforme » (en haut à droite).</div>'

if page == PAGES[0]:
    st.markdown(hero_html(), unsafe_allow_html=True)
    stats = [(len(N["items"]), "articles en veille"), (len(A), "acteurs référencés"), (len(E), "termes d'encyclopédie"), (fmt_upd(N["updated"]), "dernière mise à jour")]
    st.markdown('<div class="stats">' + "".join(f'<div class="stat"><b>{e(v)}</b><span>{l}</span></div>' for v, l in stats) + "</div>", unsafe_allow_html=True)
    st.subheader("À la une")
    grid([ncard(n) for n in N["items"][:6]] or [NONE])
    st.subheader("Explorer")
    cols = st.columns(3)
    for col, (p, x) in zip(cols, [(PAGES[1], "Suivez l'actualité des territoires, de la biodiversité, de l'insertion et du mécénat."), (PAGES[2], "Fondations et acteurs, publics et privés : biodiversité, insertion, mécénat de compétences."), (PAGES[4], "Comprendre les grands concepts, avec définitions et exemples.")]):
        col.markdown(f'<div class="card"><h3>{e(p)}</h3><p>{e(x)}</p></div>', unsafe_allow_html=True)
        col.button("Ouvrir →", key="go_" + p, on_click=goto, args=(p,))
elif page == PAGES[1]:
    banner("Actualités", "Outre-mer, biodiversité, insertion professionnelle, mécénat et RSE.", "news")
    c1, c2, c3 = st.columns([1, 1, 2])
    th = c1.selectbox("Thème", ["Tous"] + list(TH.values())); te = c2.selectbox("Territoire", ["Tous"] + sorted({n["territory"] for n in N["items"]})); q = c3.text_input("Rechercher un article")
    L = [n for n in N["items"] if (th == "Tous" or TH.get(n["theme"]) == th) and (te == "Tous" or n["territory"] == te) and q.lower() in (n["title"] or "").lower()]
    lim = st.session_state.setdefault("nlim", 60)
    st.caption(f"{len(L)} articles")
    grid([ncard(n) for n in L[:lim]] or [NONE])
    if len(L) > lim:
        st.button("Voir plus d'articles", on_click=lambda: st.session_state.update(nlim=lim + 60))
elif page == PAGES[2]:
    banner("Fondations & acteurs", "Fondations, intermédiaires et organismes qui agissent pour la biodiversité, l'insertion et le mécénat de compétences.", "found")
    tf, tc, ta = st.tabs(["🌿 Biodiversité & insertion", "🤝 Mécénat de compétences (veille)", "🏛️ Autres acteurs"])
    fc = lambda f: card([(f["t"], 1)] + [(d, 0) for d in f["d"]], f["n"] + " ↗", f["x"], meta=("Engagement des collaborateurs : " + f["c"] if f["c"] else ""), link=f.get("u") or "https://www.google.com/search?q=" + urllib.parse.quote(f["n"]))
    with tf:
        c1, c2 = st.columns([1, 2])
        dm = c1.selectbox("Domaine", ["Tous", "Biodiversité", "Insertion"], key="fd"); q = c2.text_input("Rechercher une fondation", key="fq")
        L = [f for f in content.FOUND if (dm == "Tous" or dm in f["d"]) and q.lower() in (f["n"] + f["x"]).lower()]
        st.caption(f"{len(L)} fondations · sans site indiqué, le lien lance une recherche : à vérifier avant diffusion")
        grid([fc(f) for f in L])
    with tc:
        st.info("Fondations dont les collaborateurs peuvent s'impliquer (mécénat de compétences, parrainage) et organismes qui facilitent ces missions. Vérifiez les programmes en cours sur leur site.")
        st.subheader("Fondations avec implication des collaborateurs"); grid([fc(f) for f in content.FOUND if f["c"]])
        st.subheader("Intermédiaires et réseaux"); grid([fc(f) for f in content.INTERMEDIARIES])
        st.subheader("Veille : dernières actualités")
        W = [n for n in N["items"] if n["theme"] in ("competences", "fondations")]
        grid([ncard(n) for n in W[:12]] or [NONE])
    with ta:
        c1, c2 = st.columns([1, 2])
        dm = c1.selectbox("Domaine", ["Tous", "Biodiversité", "Insertion", "Mécénat", "Territoires"]); q = c2.text_input("Rechercher un acteur")
        L = [a_ for a_ in A if (dm == "Tous" or dm in a_["d"]) and q.lower() in (a_["n"] + a_["x"]).lower()]
        st.caption(f"{len(L)} acteurs (liens à vérifier avant diffusion)")
        grid([card([(a_["t"], 1)] + [(d, 0) for d in a_["d"]], a_["n"] + (" ↗" if a_.get("u") else ""), a_["x"], link=a_.get("u")) for a_ in L])
elif page == PAGES[3]:
    banner("Emplois", "Métiers, employeurs et pistes de recherche : environnement, insertion, philanthropie et mécénat.", "jobs")
    ter = st.selectbox("Territoire de recherche", ["Outre-mer", "Guadeloupe", "Martinique", "Mayotte", "La Réunion", "Guyane", "France"])
    st.markdown("[France Travail ↗](https://www.francetravail.fr) · [Apec ↗](https://www.apec.fr) · [Welcome to the Jungle ↗](https://www.welcometothejungle.com)")
    jl = lambda L: grid([card([(j[1], 0)], j[0], "Employeurs : " + j[2], link="https://www.google.com/search?q=" + urllib.parse.quote(f"offre emploi {j[0]} {ter}")) for j in L])
    je, jp = st.tabs(["🌿 Environnement & insertion", "💝 Philanthropie & mécénat"])
    with je:
        jl(content.JOBS["titres"]); st.subheader("Acteurs qui recrutent"); grid([card([(r[1], 1)], r[0], f"{r[2]} · {r[3]}") for r in content.JOBS["recruteurs"]])
    with jp:
        jl(content.PHIL_JOBS["titres"]); st.subheader("Acteurs qui recrutent"); grid([card([(r[1], 1)], r[0], f"{r[2]} · {r[3]}") for r in content.PHIL_JOBS["recruteurs"]])
        st.subheader("Veille : actualités emploi et philanthropie"); grid([ncard(n) for n in [n for n in N["items"] if n["theme"] in ("philanthropie", "emploi")][:9]] or [NONE])
elif page == PAGES[4]:
    banner("Encyclopédie", "Termes, définitions et exemples pour comprendre la biodiversité, l'insertion, le mécénat et la RSE.", "encyc")
    c1, c2 = st.columns([1, 2])
    cat = c1.selectbox("Catégorie", ["Toutes"] + sorted(E.categorie.unique())); q = c2.text_input("Rechercher un terme")
    D_ = E[(E.categorie == cat) | (cat == "Toutes")]
    D_ = D_[(D_.terme + D_.definition + D_.exemple).str.contains(q, case=False, regex=False)].sort_values("terme")
    st.caption(f"{len(D_)} / {len(E)} termes")
    grid([card([(r["categorie"], 0)], r["terme"], r["definition"], f'{r["source"]} · {r["date_ajout"]}', ex=(f"<b>Exemple :</b> {e(r['exemple'])}" if r["exemple"] else "")) for r in D_.to_dict("records")])
elif page == PAGES[5]:
    banner("Lectures & textes", "Fiches de lecture sur la biodiversité et les espèces envahissantes ; textes clés RSE et mécénat (à vérifier avant usage).", "reads")
    tl, tr = st.tabs(["📖 Fiches de lecture", "⚖️ Réglementation"])
    with tl:
        rt = st.selectbox("Thème", ["Tous", "Action biodiversité", "Espèces envahissantes", "Cadre & politiques"])
        L = [r for r in content.READS if rt == "Tous" or r[0] == rt]
        rc = lambda r: card([(r[0], 0), (r[1], 1)], r[2], r[4], r[3], ex=f"<b>Pourquoi la lire :</b> {e(r[5])}")
        if st.button("🎲 Me recommander une fiche"):
            st.session_state.pick = random.choice(L)
        if st.session_state.get("pick") and st.session_state.pick in L:
            st.subheader("Notre recommandation"); grid([rc(st.session_state.pick)])
        grid([rc(r) for r in L])
    with tr:
        st.download_button("📄 Réglementation en PDF", PDFS["regs"][2], "reglementation.pdf", "application/pdf", key="dl_regs2")
        grid([card([(r[0], 0)], r[1], r[2]) for r in content.REGS])
elif page == PAGES[6]:
    banner("Territoires", "Communes de la Guadeloupe, de la Martinique, de Mayotte, de La Réunion et de la Guyane.", "geo")
    G = content.geo_rows(); T = list(content.GEO)
    c1, c2 = st.columns([1, 2])
    tt = c1.selectbox("Territoire", ["Tous"] + [f"{t} ({len(content.GEO[t].split(';'))})" for t in T]); q = c2.text_input("Rechercher une commune")
    L = [g for g in G if (tt == "Tous" or tt.startswith(g[0] + " (")) and q.lower() in g[1].lower()]
    st.caption(f"{len(L)} communes")
    grid([card([(g[3], 1)] if g[3] else [], g[1], meta=g[0]) for g in L], small=True)

if page == PAGES[-1]:
    banner("🧰 Boîtes à outils", "Appels à projets, partenaires, mécénat de compétences, évaluation des candidatures, DPEF et exports PDF.")
    with st.container(key="tools"):
        t1, t2, t3, t4, t5, t6 = st.tabs(["📣 Appels à projets", "🤝 Partenaires", "🏭 Mécénat de compétences", "⚖️ Grille d'évaluation", "📝 DPEF / RSE", "📄 Exports PDF"])
        ST = st.column_config.SelectboxColumn
        with t1:
            st.caption("Suivi des appels à projets : ouverture, clôture, budget, statut.")
            tracker("aap", ["Intitulé", "Thématique", "Territoire", "Ouverture", "Clôture", "Budget (€)", "Statut"], cfg={"Statut": ST(options=["Préparation", "Ouvert", "En instruction", "Jury", "Clos"])})
        with t2:
            st.caption("Suivi des partenaires : conventions, contacts, prochaines actions.")
            tracker("partenaires", ["Partenaire", "Type", "Territoire", "Contact", "Convention", "Prochaine action", "Échéance", "Statut"], cfg={"Statut": ST(options=["Prospect", "En discussion", "Convention signée", "En cours", "Terminé"])})
        with t3:
            st.caption("Salariés (notamment d'usines) mis à disposition d'associations. Valorisation indicative.")
            mc = tracker("mecenat_competences", ["Site / usine", "Équipe", "Association bénéficiaire", "Mission", "Heures prévues", "Heures réalisées", "Statut"], cfg={"Statut": ST(options=["Planifié", "En cours", "Réalisé", "Annulé"]), "Heures prévues": st.column_config.NumberColumn(), "Heures réalisées": st.column_config.NumberColumn()})
            taux = st.number_input("Coût horaire chargé moyen (€)", 0.0, 500.0, 35.0, 1.0)
            hp, hr = pd.to_numeric(mc["Heures prévues"], errors="coerce").sum(), pd.to_numeric(mc["Heures réalisées"], errors="coerce").sum()
            m1, m2, m3 = st.columns(3)
            m1.metric("Heures prévues / réalisées", f"{hp:.0f} / {hr:.0f}"); m2.metric("Valorisation réalisée", f"{hr * taux:,.0f} €"); m3.metric("Réduction d'impôt indicative (60 %)", f"{hr * taux * 0.6:,.0f} €")
            st.caption("Estimation indicative : plafonds, conditions et taux à vérifier avec votre service fiscal (CGI art. 238 bis).")
        with t4:
            st.caption("Notez chaque candidature de 0 à 5 par critère : le score pondéré est calculé automatiquement.")
            W = {"Impact biodiversité": 25, "Insertion professionnelle": 20, "Ancrage local": 15, "Faisabilité et budget": 15, "Gouvernance": 10, "Mesure d'impact": 15}
            g = tracker("grille_evaluation", ["Projet"] + list(W), cfg={k: st.column_config.NumberColumn(min_value=0, max_value=5) for k in W})
            if len(g):
                g = g.copy(); g["Score /5"] = sum(pd.to_numeric(g[k], errors="coerce").fillna(0) * w for k, w in W.items()) / 100
                st.dataframe(g[["Projet", "Score /5"]].sort_values("Score /5", ascending=False), width="stretch")
            st.caption("Pondérations : " + " · ".join(f"{k} {w} %" for k, w in W.items()))
        with t5:
            st.caption("Plan de rédaction de la DPEF : étapes, livrables, responsables, avancement.")
            d = tracker("dpef_suivi", ["Étape", "Livrable", "Responsable", "Échéance", "Statut"], seed=content.DPEF_STEPS, cfg={"Statut": ST(options=["À faire", "En cours", "Validé"])})
            if len(d): st.progress(float((d["Statut"] == "Validé").mean()), text=f"Avancement : {(d['Statut'] == 'Validé').mean():.0%}")
            st.download_button("⬇️ Télécharger la trame DPEF (Markdown)", content.DPEF_MD, "trame_dpef.md", key="dl_dpef")

        with t6:
            st.caption("Un PDF par onglet du site.")
            cols = st.columns(4)
            for i, (k, (lab, fn, pdf)) in enumerate(PDFS.items()):
                cols[i % 4].download_button(f"📄 {lab}", pdf, f"{fn}.pdf", "application/pdf", key=f"pdf_tab_{i}")

st.markdown(f'<div class="creator">{e(PLATFORM_NAME)} · {e(today_fr())}<br><span style="opacity:.85;font-size:.85rem">Sources : Google Actualités, Wikipédia, acteurs publics et privés. Contenus générés par IA à vérifier.</span><br>Plateforme travaillée et réalisée par <b>Mackenson CINEUS</b><br><span style="opacity:.6;font-size:.75rem">Version {APP_VERSION}</span></div>', unsafe_allow_html=True)
