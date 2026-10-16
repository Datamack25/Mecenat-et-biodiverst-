"""Logique métier : données de secours, collecte d'actualités, enrichissement de l'encyclopédie."""
import csv, datetime, json, os, random, unicodedata, urllib.parse, urllib.request
import xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime
from pathlib import Path
import defaults as D

BASE = Path(__file__).resolve().parent
DATA = BASE / "data"
CSV = DATA / "encyclopedie.csv"
H = ["terme", "categorie", "definition", "exemple", "source", "date_ajout"]
CATS = ["Concepts", "Écosystèmes", "Espèces", "Menaces", "Protection", "Politiques", "Économie", "Insertion", "Mécénat", "Outre-mer", "Société", "Science"]

def norm(t):
    """Forme normalisée d'un terme (sans accents/casse/pluriel) pour détecter les doublons."""
    t = unicodedata.normalize("NFKD", t.lower()).encode("ascii", "ignore").decode()
    return " ".join((w[:-3] + "al" if w.endswith("aux") else w.rstrip("sx")) if len(w) > 3 else w for w in t.split())

def ensure_data():
    """Crée data/ et les fichiers manquants à partir de defaults.py."""
    DATA.mkdir(exist_ok=True)
    # Dépôt « à plat » (fichiers de données à la racine) : on les recopie dans data/ s'ils y manquent
    for name in ("encyclopedie.csv", "acteurs.json", "feeds.json", "news.json", "termes_a_traiter.txt", "geographie.csv"):
        src, dst = BASE / name, DATA / name
        if src.exists() and src.stat().st_size and (not dst.exists() or dst.stat().st_size == 0):
            dst.write_bytes(src.read_bytes())
    def w(p, txt):
        if not p.exists() or p.stat().st_size == 0:
            p.write_text(txt, encoding="utf-8")
    w(DATA / "feeds.json", json.dumps(D.FEEDS, ensure_ascii=False, indent=1))
    w(DATA / "acteurs.json", json.dumps(D.ACTORS, ensure_ascii=False, indent=1))
    w(DATA / "news.json", '{"updated": null, "items": []}')
    w(DATA / "termes_a_traiter.txt", "\n".join(D.QUEUE))
    if not CSV.exists() or CSV.stat().st_size == 0:
        with open(CSV, "w", encoding="utf-8", newline="") as f:
            wr = csv.writer(f); wr.writerow(H); wr.writerows(D.ENC_ROWS)

def fetch_news():
    """Collecte Google Actualités -> data/news.json. Retourne (nb_articles, erreurs)."""
    ensure_data()
    feeds = json.load(open(DATA / "feeds.json", encoding="utf-8"))
    import content
    feeds += [f for f in content.EXTRA_FEEDS if f not in feeds]
    seen, items, errs = set(), [], []
    for f in feeds:
        url = "https://news.google.com/rss/search?" + urllib.parse.urlencode({"q": f["q"] + " when:30d", "hl": "fr", "gl": "FR", "ceid": "FR:fr"})
        try:
            root = ET.fromstring(urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=30).read())
        except Exception as e:
            errs.append(f"{f['q']}: {e}"); continue
        for it in root.iter("item"):
            link = it.findtext("link")
            if link in seen: continue
            seen.add(link)
            try: d = parsedate_to_datetime(it.findtext("pubDate")).isoformat()
            except Exception: d = ""
            src = it.find("source")
            items.append({"title": it.findtext("title"), "link": link, "date": d, "source": src.text if src is not None else "", "theme": f["theme"], "territory": f["territory"]})
    if items:  # on ne remplace jamais un fichier existant par du vide
        items.sort(key=lambda x: x["date"], reverse=True)
        json.dump({"updated": datetime.datetime.utcnow().isoformat() + "Z", "items": items}, open(DATA / "news.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return len(items), errs

def enrich(n=10):
    """Ajoute n termes à l'encyclopédie (Claude si ANTHROPIC_API_KEY, sinon Wikipédia). Retourne un message."""
    ensure_data()
    rows = list(csv.DictReader(open(CSV, encoding="utf-8")))
    names = sorted(r["terme"] for r in rows)
    have = {norm(n) for n in names}
    today = datetime.date.today().isoformat(); new = []; key = os.getenv("ANTHROPIC_API_KEY")
    try:
        if key:
            prompt = (f"Tu enrichis une encyclopédie francophone sur la biodiversité, l'insertion professionnelle et le mécénat, focus territoires ultramarins français. Propose {n} NOUVEAUX termes (priorité : {', '.join(random.sample(CATS, 4))}), absents de : {'; '.join(names)[:6000]}. "
                      'Réponds UNIQUEMENT par un tableau JSON d\'objets {"terme","categorie","definition","exemple"}. Définition factuelle de 2 à 3 phrases, exemple concret en outre-mer, aucun chiffre incertain.')
            body = json.dumps({"model": os.getenv("MODEL", "claude-sonnet-5-5"), "max_tokens": 4000, "messages": [{"role": "user", "content": prompt}]}).encode()
            req = urllib.request.Request("https://api.anthropic.com/v1/messages", body, {"x-api-key": key, "anthropic-version": "2023-06-01", "content-type": "application/json"})
            txt = json.load(urllib.request.urlopen(req, timeout=180))["content"][0]["text"]
            for d in json.loads(txt[txt.index("["):txt.rindex("]") + 1]):
                if norm(d["terme"]) not in have:
                    have.add(norm(d["terme"]))
                    new.append([d["terme"].strip(), d.get("categorie", "Concepts"), d["definition"], d.get("exemple", ""), "Généré par IA (à vérifier)", today])
        else:
            q = [l.strip().split("|") for l in open(DATA / "termes_a_traiter.txt", encoding="utf-8") if l.strip()]
            for t in [t for t in q if norm(t[0]) not in have][:n]:
                try:
                    u = "https://fr.wikipedia.org/api/rest_v1/page/summary/" + urllib.parse.quote(t[0].replace(" ", "_"))
                    ex = json.load(urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "veille-outremer"}), timeout=30))["extract"]
                    new.append([t[0], t[1] if len(t) > 1 else "Concepts", ex, "", "Wikipédia (résumé)", today])
                except Exception:
                    pass
    except Exception as e:
        return f"Échec de l'enrichissement : {e}"
    if new:
        csv.writer(open(CSV, "a", encoding="utf-8", newline="")).writerows(new)
    return f"{len(new)} termes ajoutés"
