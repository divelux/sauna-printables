"""57. The sauna tonttu: a short read-aloud story inspired by Finnish folklore, a note for grown-ups, and four coloring pages.
Folklore facts are kept to what the sources say: a tonttu is a small household spirit tied to a building such as a farmhouse,
stable or sauna; the saunatonttu looks after the sauna and makes sure people behave properly in it; children are told to be
respectful in the sauna so as not to upset it. Checked in November 2026:
  - This is Finland (finland.fi), "Finnish mythical creatures still lurk"
  - Wikipedia, "Haltija" and "Tonttu"
The characters (Aino, Mummo) and the look of the tonttu are made up for this story.
Child safety: a grown-up is in the sauna the whole time, lowest bench, short rounds, leave as soon as it feels too hot,
water to drink, only grown-ups pour water, nobody touches the stove."""
import os
import re

import art
import art3
import common as C
import w2

SLUG = "sauna-gnome-story-coloring"
TITLE = "The Sauna Tonttu: A Story and Coloring Book"
DESC = ("A short read-aloud story inspired by Finnish folklore: Aino and her grandmother visit the lakeside sauna and say hello "
        "to the sauna tonttu. With a note for grown-ups and four coloring pages.")
KEYWORDS = ("sauna tonttu, saunatonttu, Finnish folklore story for kids, sauna elf, gnome coloring pages, kids story printable, "
            "Finnish sauna for kids, coloring book, DIVELUX")
NAME = "The Sauna Tonttu"

STORY = [
    "Mummo’s sauna stood at the edge of the lake, small and gray, with a crooked chimney and a bench by the door. On Saturday evenings the chimney puffed, and the whole yard smelled of birch smoke.",
    "“Is it ready?” Aino asked, for the third time.",
    "“Almost,” said Mummo. She put her hand on the door. “But before we go in, we say hello to the tonttu.”",
    "Aino looked around. “Who?”",
    "“The sauna tonttu. A very small keeper who lives in the sauna,” Mummo said. “My grandmother told me about him when I was your age. He looks after the stove and the benches, and he likes a sauna where people are calm and kind.”",
    "“What does he look like?”",
    "“I have never seen him,” Mummo said. “But I think he has a gray beard and a pointed cap. Maybe a felt one.”",
    "Aino knocked softly on the door. “Hello, tonttu. We’re coming in.”",
    "Nothing answered. But the door swung open with a friendly creak, and that, Mummo said, was a very good sign.",
    "Inside, the sauna was warm and dim. The stones on the stove were hot, and the wooden walls smelled like summer. Mummo spread a towel on the lowest bench, and Aino sat down on it. Mummo sat right next to her.",
    "“Why not the top bench?” Aino asked.",
    "“The top is the hottest. Down here it is gentler. Just right for us.”",
    "Mummo dipped the ladle in the bucket and poured a little water on the stones. <i>Tssss!</i> A soft cloud of steam rose up and rolled over them.",
    "“That is löyly,” Mummo said. “The sauna’s warm breath.”",
    "Aino laughed, then stopped. “Do I have to whisper?”",
    "“No. You can talk and laugh. The tonttu only minds shouting, quarreling and mess. And the stove is his: only grown-ups pour the water, and nobody touches the stove.”",
    "They sat and listened. The stove ticked. Outside, a bird called over the lake. Aino watched little drops roll down her arms. Her cheeks felt hot. Her ears felt hot. Everything felt very hot.",
    "“Mummo, I think I’m done.”",
    "“Then we go out,” Mummo said, and stood up at once. “That is the most important sauna rule of all. When you feel too hot, or a bit funny, you go out. Nobody stays longer than feels good. The tonttu would not want that either.”",
    "They stepped out onto the porch. The evening air felt cool and soft. Mummo gave Aino a cup of water, and Aino drank all of it. They sat on the bench wrapped in their towels and watched the lake turn pink.",
    "A dragonfly zipped past. Down by the shore, the reeds whispered in the breeze.",
    "“Does the tonttu ever come out here?” Aino asked.",
    "“Maybe on warm nights,” Mummo said. “To look at the stars.”",
    "“Can we go in again?”",
    "“After a rest. A little while out here, then a short, warm round.”",
    "When they went back in, the sauna felt friendlier, as if it had been waiting for them. Aino sat on her towel and counted the knots in the wood. Mummo gave the stones one small ladle of water. This time, as soon as Aino felt warm enough, she said so, and they went out together.",
    "At the end of the evening, Mummo hung the ladle on its hook. Aino picked a birch leaf off the floor and folded the towels. Then she brushed the lowest bench with her hand, the way she had seen Mummo do it.",
    "“There,” Aino said. “A tidy sauna.”",
    "Mummo smiled. “The tonttu will be pleased.”",
    "Aino turned at the door. In the dark corner by the stove, something glinted, just for a moment, like a tiny eye, or a drop of water catching the last light.",
    "“Good night, tonttu,” she whispered. “Thank you for the warm sauna.”",
    "She was almost sure she heard a soft, happy creak from the old wooden walls. Then she ran back to the house with Mummo, her towel flapping behind her, while the first stars came out over the lake.",
]
SPLIT = 16  # paragraphs on the first story page

CSS = w2.CSS + """
.page{padding:.5in .65in .34in}
.cover{padding:.55in .65in .34in}
.cover .k{font-size:7.2pt;letter-spacing:.18em;text-transform:uppercase;font-weight:600;color:var(--muted)}
.cover h1{font-size:88pt;line-height:.82;margin:.12in 0 .1in -.04in;white-space:normal}
.cover .sub{font-family:var(--display);font-weight:500;font-size:16pt;line-height:1.25;color:var(--ink-2)}
.cover .art{flex:1;display:flex;align-items:center;justify-content:center;min-height:0;margin:.15in 0}
.cover .art svg{display:block;height:100%;max-height:6.2in;width:auto;max-width:100%}
.cover .ladder{height:.1in;margin-bottom:.1in}
.cover .by{display:flex;justify-content:space-between;align-items:flex-end;font-size:9pt;color:var(--ink-2);margin-bottom:.12in}
.cover .by b{font-family:var(--display);font-weight:700;font-size:12pt;color:var(--ink)}
.story{flex:1;min-height:0;column-count:2;column-gap:.4in;column-fill:balance;margin-top:.16in}
.story p{font-family:var(--body);font-size:12pt;line-height:1.5;color:var(--ink);margin:0 0 .09in;text-wrap:pretty;break-inside:avoid-column}
.story p.first::first-letter{font-family:var(--display);font-weight:800;font-size:44pt;float:left;line-height:.8;margin:.04in .06in 0 0}
.vign{display:flex;justify-content:center;align-items:flex-end;gap:.4in;flex:none;margin-top:.06in;border-top:1px solid var(--line-2);padding-top:.1in}
.vign svg{display:block;height:1.3in;width:auto}
.end{font-family:var(--display);font-weight:700;font-size:13pt;text-align:center;margin-top:.12in;color:var(--ink-2)}
.gnote{display:grid;grid-template-columns:1fr 1fr;column-gap:.36in;margin-top:.16in;flex:none}
.gnote p{font-size:9.4pt;line-height:1.48;color:var(--ink-2);margin-bottom:.08in}
.gnote h3{font-family:var(--display);font-weight:700;font-size:15pt;letter-spacing:-.01em;margin-bottom:.06in}
.words{margin-top:.08in}
.words li{font-size:9.2pt;line-height:1.4;color:var(--ink-2);padding:.04in 0;border-top:1px solid var(--line)}
.words b{font-family:var(--display);font-weight:700;font-size:10.4pt;color:var(--ink);margin-right:.06in}
.kids{background:var(--card);border:1.5px solid var(--ink);border-radius:var(--r);padding:.14in .18in;flex:none;margin-top:.16in}
.kids h3{font-family:var(--display);font-weight:800;font-stretch:75%;font-size:24pt;line-height:.95;letter-spacing:-.01em;margin-bottom:.08in}
.kids .cl li{font-size:9.4pt}
.src{margin-top:.14in;flex:none}
.src li{font-size:8pt;line-height:1.4;color:var(--muted);padding:.02in 0}
.src b{color:var(--ink-2);font-weight:600}
.ct{display:flex;justify-content:space-between;align-items:flex-end;gap:.3in;border-bottom:2px solid var(--ink);padding-bottom:.09in;flex:none}
.ct h2{font-family:var(--display);font-weight:800;font-stretch:75%;font-size:34pt;line-height:.9;letter-spacing:-.018em;margin:0;white-space:nowrap}
.ct .k{display:block;font-family:var(--body);font-size:6.4pt;letter-spacing:.16em;text-transform:uppercase;font-weight:600;color:var(--muted);margin-bottom:.06in}
.ct p{font-size:9.4pt;line-height:1.4;color:var(--ink-2);max-width:3.4in;text-align:right;text-wrap:balance}
.color{padding:.45in .6in .32in;background:#fff}
.artw{flex:1;display:flex;align-items:center;justify-content:center;min-height:0}
.artw svg{display:block;width:7.08in;height:8.5in}
"""


def cover_art():
    o = []
    o.append('<circle cx="375" cy="420" r="300" fill="#fbf1e5" stroke="none"/>')
    o.append(art.steam(160, 470, 150, 16) + art.steam(590, 470, 150, 16) + art.steam(630, 430, 120, 12))
    o.append(art3.tonttu(375, 700, 1.75, hold="lantern", uid="cv", cap_fill="#f0a877", tunic_fill="#f5c7a0", boot_fill="#c99b6c"))
    for x, a in ((150, -150), (180, -40), (570, -140), (598, -30)):
        o.append(art.leaf(x, 702, a, 40, 13))
    o.append(art.ln("M100 704H650"))
    return art.svg(750, 760, "".join(o), 3)


def para(i, t):
    cls = ' class="first"' if i == 0 else ""
    return f"<p{cls}>{t}</p>"


def build():
    pages = []
    pages.append(f"""<main class="page cover">
<span class="k">A read-aloud story · ages 4 to 8 · with four coloring pages</span>
<h1>The sauna tonttu<i>.</i></h1>
<p class="sub">A story inspired by Finnish folklore</p>
<div class="art">{cover_art()}</div>
<div class="ladder"><i></i><i></i><i></i><i></i></div>
<div class="by"><span><b>Written and drawn by DIVELUX</b><br>Makers of wool sauna hats, Irvine, California</span><span>For a grown-up and a child to read together</span></div>
{C.foot(NAME)}
</main>""")
    s1 = "".join(para(i, t) for i, t in enumerate(STORY[:SPLIT]))
    s2 = "".join(para(i + SPLIT, t) for i, t in enumerate(STORY[SPLIT:]))
    v1 = art.svg(300, 330, art.bucket(0, 0, 1.0, ladle=True).replace('translate(0 0)', 'translate(0 80)'), 3)
    v2 = art.svg(400, 380, art3.tonttu(200, 370, 1.1, hold="whisk", uid="v2"), 3)
    pages.append(f"""<main class="page">
{w2.ph("Aino and the sauna tonttu", "A story inspired by Finnish folklore")}
<div class="story">{s1}</div>
<div class="vign">{v1}</div>
{C.foot(NAME + " · story 1 of 2")}
</main>""")
    pages.append(f"""<main class="page">
<div class="story" style="margin-top:0">{s2}<p class="end">The end</p></div>
<div class="vign">{v2}</div>
{C.foot(NAME + " · story 2 of 2")}
</main>""")
    words = "".join(f"<li><b>{a}</b>{b}</li>" for a, b in [
        ("tonttu", "(TONT-too) a small spirit of Finnish folk belief who lives in and looks after a house, a barn or a sauna."),
        ("saunatonttu", "the tonttu of the sauna."),
        ("löyly", "the steam that rises when water is poured on the hot sauna stones."),
        ("Mummo", "a Finnish word for grandma."),
    ])
    kids = w2.checks([
        "<b>A grown-up stays in the sauna</b> with children the whole time.",
        "<b>Lowest bench, short rounds.</b> Milder heat than for grown-ups, and plenty of breaks outside.",
        "<b>Out as soon as it feels too hot,</b> or if a child feels dizzy or unwell. Children may leave any time they want.",
        "<b>Water to drink</b> between rounds.",
        "<b>Only grown-ups pour water</b> on the stones. Nobody touches the stove or the stones.",
        "<b>Walk, don’t run.</b> Floors and steps get slippery.",
        "<b>Babies, toddlers, or any health question:</b> ask your child’s doctor first.",
    ])
    pages.append(f"""<main class="page">
{w2.ph("For grown-ups", "About the tonttu, and taking children to the sauna")}
<div class="gnote">
<div><h3>About the sauna tonttu</h3>
<p>In Finnish folk belief, a <i>tonttu</i> is a small household spirit tied to one building, such as a farmhouse, a stable or a sauna. The sauna has its own, the <i>saunatonttu</i>. It looks after the sauna and makes sure people behave well there. Children were told to be respectful in the sauna so they would not upset it.</p>
<p>Stories about the tonttu differ from place to place and from family to family. This one does not retell any of them. Aino, Mummo and this tonttu with his felt cap are made up, in the spirit of those old stories: be kind, keep it calm, leave the sauna tidy.</p></div>
<div><h3>Words in the story</h3><ul class="words">{words}</ul></div>
</div>
<div class="kids"><h3>Sauna with children</h3>{kids}
<p class="fine" style="margin-top:.08in">General information, not medical advice. Talk to your child’s doctor if you are unsure.</p></div>
<ul class="src"><li><b>Sources for the folklore note:</b> This is Finland, “Finnish mythical creatures still lurk” (finland.fi) · Wikipedia, “Haltija” and “Tonttu”. Checked November 2026.</li>
<li>More free sauna printables and tools: <a href="{C.TOOLS}">diveluxsaunahat.com/pages/sauna-tools</a></li></ul>
{C.foot(NAME)}
</main>""")
    n = len(art3.T_PAGES)
    for i, (title, cap, fn) in enumerate(art3.T_PAGES, 1):
        pages.append(f"""<main class="page color">
<div class="ct"><div><span class="k">Coloring page {i} of {n}</span><h2>{C.esc(title)}</h2></div><p>{C.esc(cap)}</p></div>
<div class="artw">{fn()}</div>
{C.foot(NAME + " · coloring")}
</main>""")
    C.write(os.path.join(C.ROOT, SLUG, SLUG + ".html"), C.doc(TITLE, DESC, KEYWORDS, CSS, "\n".join(pages)))
    meta = dict(title="The Sauna Tonttu: A Story Inspired by Finnish Folklore, with Coloring Pages", subject=DESC, keywords=KEYWORDS)
    jobs = C.std_jobs(SLUG, SLUG + ".html", SLUG, meta)
    return dict(slug=SLUG, jobs=jobs, preview=dict(pdf=jobs[0]["pdf"], pages=[1, 2, 5], dpi=75))


def word_count():
    return len(re.findall(r"[A-Za-zöÖ’']+", re.sub(r"<[^>]+>", "", " ".join(STORY))))


if __name__ == "__main__":
    print("story words:", word_count())
