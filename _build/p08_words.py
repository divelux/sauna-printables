"""8. Sauna Words poster: a small glossary in seven languages.

Only words we could confirm are included. Sources checked: the DIVELUX open dataset
(../../dataset, terms such as löyly, vihta/vasta, kiuas, leil, viht, keris, Aufguss, pirtis, pirts, vanta, slota,
pirtininkas, pirtnieks, bastu, kallbadhus, saunahattu, Saunahut, saunamüts, predbannik, parilka, venik, laznia),
Wiktionary entries (lauteet, kiulu, шайка, полок, каменка, lave, garas, gars) and published usage
(saunalava in Estonian retail listings; "Hüva leili!" in ERR's Estonia Explained).
"""
import os
import common as C

SLUG = "sauna-words-poster"
TITLE = "Sauna Words Poster"
DESC = "A printable poster of sauna words in seven languages: Finnish, Russian, German, Estonian, Swedish, Lithuanian and Latvian, from löyly to Aufguss."
KEYWORDS = "sauna words, sauna glossary, sauna vocabulary poster, löyly meaning, Aufguss meaning, banya words, Finnish sauna terms, sauna dictionary, DIVELUX"

# (word, extra script or "", gloss)
MAIN = [
    ("Finnish", "suomi", [
        ("sauna", "", "the hot room itself"),
        ("löyly", "", "the steam that rises when water hits the hot stones"),
        ("kiuas", "", "the stove with its stones"),
        ("lauteet", "", "the wooden benches"),
        ("vihta, vasta", "", "birch whisk: vihta in the west, vasta in the east"),
        ("kiulu", "", "small wooden water bucket"),
        ("kauha", "", "the ladle"),
        ("savusauna", "", "smoke sauna, no chimney"),
        ("avanto", "", "ice hole for a cold dip"),
        ("saunahattu", "", "sauna hat"),
    ]),
    ("Russian", "русский", [
        ("banya", "баня", "the steam bath"),
        ("parilka", "парилка", "the steam room itself"),
        ("par", "пар", "steam"),
        ("venik", "веник", "leafy whisk of birch or oak"),
        ("kamenka", "каменка", "the stove with its stones"),
        ("polok", "полок", "the tiered bench"),
        ("shaika", "шайка", "washtub"),
        ("predbannik", "предбанник", "the room for resting and tea"),
        ("S lyogkim parom!", "С лёгким паром!", "“enjoy your steam,” said to someone just out of the banya"),
    ]),
    ("German", "Deutsch", [
        ("Aufguss", "", "water poured on the stones, hot air fanned with a towel"),
        ("Saunameister", "", "the one who leads the Aufguss"),
        ("Saunagang", "", "one round in the hot room"),
        ("Saunahut", "", "sauna hat; also Saunamütze"),
        ("Ruheraum", "", "the quiet room for resting"),
        ("Tauchbecken", "", "cold plunge pool"),
        ("Dampfbad", "", "steam bath"),
        ("textilfrei", "", "no swimwear; sit on a towel"),
    ]),
    ("Estonian", "eesti", [
        ("saun", "", "sauna"),
        ("leil", "", "the steam from the stones"),
        ("keris", "", "the stove with its stones"),
        ("viht", "", "birch whisk"),
        ("saunalava", "", "the bench platform"),
        ("suitsusaun", "", "smoke sauna"),
        ("saunamüts", "", "sauna hat"),
        ("Hüva leili!", "", "“good steam!”, a bather's wish"),
    ]),
]
SMALL = [
    ("Swedish", "svenska", [("bastu", "sauna (from badstuga, “bath cabin”)"), ("bada bastu", "to take a sauna"),
                            ("lave", "the bench"), ("kallbadhus", "seaside cold-bath house")]),
    ("Lithuanian", "lietuvių", [("pirtis", "the bathhouse"), ("garas", "steam"), ("vanta", "whisk"),
                                ("pirtininkas", "bath master")]),
    ("Latvian", "latviešu", [("pirts", "the bathhouse"), ("gars", "steam"), ("slota", "whisk"),
                             ("pirtnieks", "bath master")]),
]

CSS = """
.page{padding:.5in .56in .34in}
.head{display:block}
h1{font-weight:800;font-stretch:75%;font-size:80pt;line-height:.84;letter-spacing:-.022em;margin:.08in 0 0 -.04in;white-space:nowrap}
h1 i{font-style:normal;color:var(--ember)}
.lead{font-family:var(--display);font-weight:500;font-size:13.5pt;line-height:1.3;color:var(--ink-2);margin-top:.13in}
.main{flex:1;display:grid;grid-template-columns:repeat(4,1fr);column-gap:.26in;margin-top:.18in;min-height:0}
.lang{border-top:2px solid var(--ink);padding-top:.07in;display:flex;flex-direction:column;min-height:0}
.lang h2{font-weight:800;font-stretch:75%;font-size:22pt;line-height:1;letter-spacing:-.012em}
.lang h2 span{font-family:var(--body);font-stretch:100%;font-weight:400;font-size:8.6pt;letter-spacing:0;color:var(--muted);margin-left:.07in}
.lang dl{margin:.07in 0 0;flex:1;display:flex;flex-direction:column;justify-content:space-between}
.lang .e{border-top:1px solid var(--line-2);padding:.04in 0 .035in}
.lang dt{font-family:var(--display);font-weight:700;font-size:13.5pt;line-height:1.12;letter-spacing:-.01em}
.lang dt span{font-family:var(--body);font-weight:400;font-size:9pt;letter-spacing:0;color:var(--ink-2);margin-left:.07in;white-space:nowrap;display:inline-block}
.lang dt span.blk{display:block;margin:.01in 0 0;line-height:1.3}
.lang dd{margin:.01in 0 0;font-size:8.5pt;line-height:1.32;color:var(--ink-2)}
.small{display:grid;grid-template-columns:repeat(3,1fr);column-gap:.3in;margin-top:.16in;flex:none}
.small .lang dl{display:block}
.small .e{display:grid;grid-template-columns:1.04in 1fr;column-gap:.08in;align-items:baseline;padding:.04in 0}
.small dt{font-size:12pt}
.small dd{margin:0}
.fine{font-size:7.5pt;line-height:1.42;color:var(--muted);margin:.12in 0 .1in}
"""


def build():
    cols = []
    for name, native, words in MAIN:
        es = "".join(f'<div class="e"><dt>{C.esc(w)}' + (f'<span{" class=blk" if len(w) + len(x) > 17 else ""}>{C.esc(x)}</span>' if x else "")
                     + f'</dt><dd>{C.esc(g)}</dd></div>' for w, x, g in words)
        cols.append(f'<section class="lang"><h2>{name}<span>{C.esc(native)}</span></h2><dl>{es}</dl></section>')
    small = []
    for name, native, words in SMALL:
        es = "".join(f'<div class="e"><dt>{C.esc(w)}</dt><dd>{C.esc(g)}</dd></div>' for w, g in words)
        small.append(f'<section class="lang"><h2>{name}<span>{C.esc(native)}</span></h2><dl>{es}</dl></section>')
    n = sum(len(w) for _, _, w in MAIN) + sum(len(w) for _, _, w in SMALL)
    body = f"""<main class="page">
<span class="kicker">A small dictionary of the hot room</span>
<div class="head"><h1>Sauna words<i>.</i></h1><p class="lead">{n} words bathers use in seven languages, from the stove to the steam.</p></div>
<div class="main">{''.join(cols)}</div>
<div class="small">{''.join(small)}</div>
<p class="fine">Words keep their original spelling. Russian is shown in Latin letters with the Cyrillic beside it. In Ukrainian the bathhouse is a laznia (лазня). Short glosses, not full dictionary entries: usage varies by region and family.</p>
{C.foot()}
</main>"""
    C.write(os.path.join(C.ROOT, SLUG, SLUG + ".html"), C.doc(TITLE, DESC, KEYWORDS, CSS, body, ext=True))
    meta = dict(title="Sauna Words: A Printable Glossary Poster in Seven Languages", subject=DESC, keywords=KEYWORDS)
    jobs = C.std_jobs(SLUG, SLUG + ".html", SLUG, meta)
    return dict(slug=SLUG, jobs=jobs, preview=dict(pdf=jobs[0]["pdf"]))
