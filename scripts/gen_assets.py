#!/usr/bin/env python3
"""Generate dossier-style SVG banner assets for the OMJOSHI15 profile README.
Dark/gold terminal-dossier aesthetic (own design, own content) with static shapes only —
no external fonts, no scripts, GitHub-SVG-sanitizer safe."""
import math
import os

OUT = os.path.join(os.path.dirname(__file__), "profile-repo", "assets")
os.makedirs(OUT, exist_ok=True)

BG = "#0a0a0c"
BG2 = "#0e0e11"
GRID = "#1a1a1f"
LINE = "#2a2a30"
GOLD = "#c9a876"
WHITE = "#eee8db"
DIM = "#8a8a90"
MONO = "ui-monospace, 'SF Mono', 'Courier New', monospace"
SANS = "'Helvetica Neue', Arial, sans-serif"

W = 900


def frame(h, body, title=""):
    grid = ""
    for x in range(0, W, 30):
        grid += f'<line x1="{x}" y1="0" x2="{x}" y2="{h}" stroke="{GRID}" stroke-width="1"/>'
    for y in range(0, h, 30):
        grid += f'<line x1="0" y1="{y}" x2="{W}" y2="{y}" stroke="{GRID}" stroke-width="1"/>'
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {h}" width="{W}" height="{h}" role="img" aria-label="{title}">
<rect width="{W}" height="{h}" fill="{BG}"/>
<g opacity="0.5">{grid}</g>
<rect x="1" y="1" width="{W-2}" height="{h-2}" fill="none" stroke="{LINE}" stroke-width="1"/>
{body}
</svg>'''


def write(name, svg):
    path = os.path.join(OUT, f"{name}.svg")
    with open(path, "w") as f:
        f.write(svg)
    print("wrote", path)


# ---------------------------------------------------------------- hero
body = f'''
<rect x="40" y="40" width="{W-80}" height="380" fill="none" stroke="{LINE}" stroke-width="1"/>
<text x="88" y="180" font-family="{SANS}" font-weight="800" font-size="92" fill="{WHITE}">OM</text>
<text x="88" y="270" font-family="{SANS}" font-weight="800" font-size="92" fill="{GOLD}">JOSHI</text>
<text x="90" y="320" font-family="{MONO}" font-size="22" letter-spacing="2" fill="{DIM}">I MODEL THE PATTERN <tspan fill="{GOLD}">BEFORE THE LOSS</tspan></text>
<text x="90" y="365" font-family="{MONO}" font-size="15" letter-spacing="1.5" fill="{DIM}">OJ / ID-15 &#183; ROLE / AI &amp; BACKEND ENGINEERING &#183; SYSTEM / ACTIVE</text>
<text x="90" y="390" font-family="{MONO}" font-size="15" letter-spacing="1.5" fill="{DIM}">FIELD / FRAUD DETECTION &#215; APPLIED ML</text>
<circle cx="92" cy="415" r="5" fill="{GOLD}"/>
<text x="106" y="420" font-family="{MONO}" font-size="15" letter-spacing="1.5" fill="{GOLD}">PROFILE VERIFIED</text>
'''
write("hero", frame(460, body, "Om Joshi"))

# ---------------------------------------------------------------- divider
body = f'<line x1="0" y1="20" x2="{W}" y2="20" stroke="{LINE}" stroke-width="1"/>'
write("divider", frame(40, body, "divider"))

# ---------------------------------------------------------------- manifesto
body = f'''
<text x="{W/2}" y="70" text-anchor="middle" font-family="{MONO}" font-size="24" letter-spacing="1" fill="{WHITE}">
  "Fraud is not a rule to catch.
</text>
<text x="{W/2}" y="110" text-anchor="middle" font-family="{MONO}" font-size="24" letter-spacing="1" fill="{GOLD}">
  It is a pattern to model."
</text>
'''
write("manifesto", frame(150, body, "manifesto"))

# ---------------------------------------------------------------- status
stats = [("PIPELINE", "5-LAYER ASYNC"), ("DECISION", "APPROVE / REVIEW / BLOCK"), ("LATENCY TARGET", "< 300ms"), ("STATUS", "ONLINE")]
cw = (W - 80) / len(stats)
cells = ""
for i, (label, value) in enumerate(stats):
    x = 40 + i * cw
    cells += f'''<line x1="{x}" y1="20" x2="{x}" y2="100" stroke="{LINE}" stroke-width="1"/>
<text x="{x+24}" y="55" font-family="{MONO}" font-size="13" letter-spacing="1.5" fill="{DIM}">{label}</text>
<text x="{x+24}" y="82" font-family="{MONO}" font-size="17" letter-spacing="0.5" fill="{GOLD}">{value}</text>'''
cells += f'<line x1="{W-40}" y1="20" x2="{W-40}" y2="100" stroke="{LINE}" stroke-width="1"/>'
write("status", frame(120, cells, "system status"))

# ---------------------------------------------------------------- capability-map
cats = [
    ("DETECTION", ["Rule Engines", "Velocity Scoring", "Anomaly Detection", "Blacklist Rules"]),
    ("ENGINEERING", ["Python", "FastAPI", "React", "Node.js"]),
    ("INFRASTRUCTURE", ["MongoDB", "Neo4j", "Redis", "Docker"]),
    ("INTELLIGENCE", ["LangChain", "RAG", "ChromaDB", "LLM Scoring"]),
]
gw, gh = (W - 80) / 2, 150
body = ""
for i, (title, items) in enumerate(cats):
    cx, cy = 40 + (i % 2) * gw, 30 + (i // 2) * gh
    body += f'<rect x="{cx+10}" y="{cy}" width="{gw-20}" height="{gh-20}" fill="{BG2}" stroke="{LINE}" stroke-width="1"/>'
    body += f'<text x="{cx+30}" y="{cy+34}" font-family="{MONO}" font-size="15" letter-spacing="2" fill="{GOLD}">{title}</text>'
    body += f'<line x1="{cx+30}" y1="{cy+46}" x2="{cx+gw-50}" y2="{cy+46}" stroke="{LINE}" stroke-width="1"/>'
    for j, item in enumerate(items):
        body += f'<text x="{cx+30}" y="{cy+72+j*20}" font-family="{MONO}" font-size="14" fill="{WHITE}">&#183; {item}</text>'
write("capability-map", frame(30 + gh * 2, body, "capability map"))

# ---------------------------------------------------------------- risk-radar (spider chart)
axes = ["Rule Engine", "Graph Analysis", "RAG / LLM", "Velocity Scoring", "Explainability"]
vals = [0.8, 0.65, 0.85, 0.7, 0.75]
cx, cy, R = W / 2, 260, 160
n = len(axes)


def pt(i, r):
    ang = -math.pi / 2 + i * 2 * math.pi / n
    return cx + r * math.cos(ang), cy + r * math.sin(ang)


rings = ""
for frac in (0.25, 0.5, 0.75, 1.0):
    pts = " ".join(f"{pt(i, R*frac)[0]:.1f},{pt(i, R*frac)[1]:.1f}" for i in range(n))
    rings += f'<polygon points="{pts}" fill="none" stroke="{LINE}" stroke-width="1"/>'
spokes = ""
labels = ""
for i, name in enumerate(axes):
    x, y = pt(i, R)
    spokes += f'<line x1="{cx}" y1="{cy}" x2="{x:.1f}" y2="{y:.1f}" stroke="{LINE}" stroke-width="1"/>'
    lx, ly = pt(i, R + 30)
    anchor = "middle" if abs(lx - cx) < 5 else ("start" if lx > cx else "end")
    labels += f'<text x="{lx:.1f}" y="{ly:.1f}" text-anchor="{anchor}" font-family="{MONO}" font-size="14" fill="{DIM}">{name}</text>'
data_pts = " ".join(f"{pt(i, R*vals[i])[0]:.1f},{pt(i, R*vals[i])[1]:.1f}" for i in range(n))
body = rings + spokes + f'<polygon points="{data_pts}" fill="{GOLD}" fill-opacity="0.22" stroke="{GOLD}" stroke-width="2"/>' + labels
body += f'<text x="{cx}" y="26" text-anchor="middle" font-family="{MONO}" font-size="15" letter-spacing="2" fill="{GOLD}">SCORING LAYER SIGNAL</text>'
write("risk-radar", frame(460, body, "risk radar"))

# ---------------------------------------------------------------- projects
projects = [
    ("indus11", "Indus11 — AI Fraud Detection Engine",
     "Real-time financial fraud detection scoring every transaction across a 5-layer async pipeline.",
     ["Rule engine + Neo4j fraud-ring graph analysis + RAG/LLM scoring run concurrently via asyncio.gather()",
      "Composite score routes each transaction to APPROVE (0-39) / REVIEW (40-69) / BLOCK (70+)",
      "MongoDB (Beanie) persistence, Redis velocity windows, React + Recharts dashboard"],
     ["Python", "FastAPI", "Neo4j", "MongoDB", "LangChain"], "OMJOSHI15/indus11"),
    ("task-manager", "Task Manager — Full-Stack CRUD",
     "RESTful API paired with a React review dashboard for task management.",
     ["Node.js + Express API with request logging and centralized error-handling middleware",
      "React dashboard with optimistic UI, toast notifications, delete-confirmation flow",
      "Full CRUD contract shared across API and UI"],
     ["Node.js", "Express", "React"], "OMJOSHI15/task-manager-api"),
    ("student-ml", "Student Performance Prediction",
     "Full-stack ML app predicting final grades and flagging at-risk students.",
     ["Linear Regression for grade prediction, Decision Tree for at-risk flagging",
      "Flask backend serving scikit-learn models, deployed on Vercel",
      "pandas-driven feature pipeline over student records"],
     ["Python", "Flask", "scikit-learn", "pandas"], "OMJOSHI15/student-performance-prediction"),
    ("internship", "AI Engineering Internship — TechnoGuide",
     "21-day applied AI internship spanning ML, NLP, and computer vision projects.",
     ["Daily project cadence across classical ML, NLP, and CV",
      "Applied tooling across the AI engineering stack, not just theory",
      "Shipped a project log documenting each day's build"],
     ["Python", "ML", "NLP", "Computer Vision"], "OMJOSHI15/AI-internship-TechnoGuide"),
]

for slug, title, summary, bullets, tags, repo in projects:
    h = 170 + len(bullets) * 26
    body = f'<text x="40" y="50" font-family="{SANS}" font-weight="700" font-size="24" fill="{WHITE}">{title}</text>'
    body += f'<line x1="40" y1="65" x2="{W-40}" y2="65" stroke="{LINE}" stroke-width="1"/>'
    body += f'<text x="40" y="98" font-family="{MONO}" font-size="15" fill="{DIM}">{summary}</text>'
    y = 130
    for b in bullets:
        body += f'<text x="40" y="{y}" font-family="{MONO}" font-size="12.5" fill="{WHITE}">&#183; {b}</text>'
        y += 26
    tagstr = "  ".join(f"[{t}]" for t in tags)
    body += f'<text x="40" y="{y+16}" font-family="{MONO}" font-size="13" letter-spacing="1" fill="{GOLD}">{tagstr}</text>'
    body += f'<text x="{W-40}" y="{y+16}" text-anchor="end" font-family="{MONO}" font-size="13" fill="{DIM}">github.com/{repo} &#8599;</text>'
    write(f"project-{slug}", frame(h + 20, body, title))

# ---------------------------------------------------------------- credentials
creds = [
    "Computer Engineering &#8212; in progress",
    "Indus11 &#8212; AI fraud-detection system, 5-layer scoring pipeline",
    "Applied Web Dev Fundamentals &#8212; full CRUD stacks, REST APIs",
    "AI Engineering Internship &#8212; TechnoGuide Infosoft",
]
body = ""
for i, c in enumerate(creds):
    y = 45 + i * 34
    body += f'<circle cx="50" cy="{y-5}" r="4" fill="{GOLD}"/>'
    body += f'<text x="70" y="{y}" font-family="{MONO}" font-size="16" fill="{WHITE}">{c}</text>'
write("credentials", frame(45 + len(creds) * 34, body, "credentials"))

# ---------------------------------------------------------------- protocols
protos = [
    "Hardening the rule engine + graph analyzer scoring thresholds",
    "Tuning RAG prompt + few-shot examples for the LLM scoring layer",
    "React dashboard UX pass on the review-queue flow",
]
body = f'<text x="40" y="40" font-family="{MONO}" font-size="15" letter-spacing="2" fill="{GOLD}">ACTIVE PROTOCOLS</text>'
for i, p in enumerate(protos):
    y = 80 + i * 34
    body += f'<text x="40" y="{y}" font-family="{MONO}" font-size="15" fill="{DIM}">[{"RUNNING":^9}]</text>'
    body += f'<text x="180" y="{y}" font-family="{MONO}" font-size="15" fill="{WHITE}">{p}</text>'
write("protocols", frame(80 + len(protos) * 34, body, "active protocols"))

# ---------------------------------------------------------------- trajectory
stages = [("2024", "Static portfolios &amp; component basics"), ("2025", "Full-stack CRUD apps &amp; REST APIs"), ("2026", "AI fraud-detection systems")]
sw = (W - 160) / (len(stages) - 1)
body = f'<line x1="80" y1="90" x2="{W-80}" y2="90" stroke="{LINE}" stroke-width="2"/>'
for i, (year, label) in enumerate(stages):
    x = 80 + i * sw
    body += f'<circle cx="{x}" cy="90" r="7" fill="{GOLD}"/>'
    body += f'<text x="{x}" y="60" text-anchor="middle" font-family="{MONO}" font-size="16" fill="{GOLD}">{year}</text>'
    body += f'<text x="{x}" y="125" text-anchor="middle" font-family="{MONO}" font-size="13" fill="{DIM}">{label}</text>'
write("trajectory", frame(160, body, "trajectory"))

# ---------------------------------------------------------------- philosophy
body = f'''
<text x="{W/2}" y="65" text-anchor="middle" font-family="{MONO}" font-size="22" letter-spacing="1" fill="{WHITE}">Detect the pattern.</text>
<text x="{W/2}" y="105" text-anchor="middle" font-family="{MONO}" font-size="22" letter-spacing="1" fill="{WHITE}">Explain the decision.</text>
<text x="{W/2}" y="145" text-anchor="middle" font-family="{MONO}" font-size="22" letter-spacing="1" fill="{GOLD}">Automate the trust.</text>
'''
write("philosophy", frame(180, body, "philosophy"))

# ---------------------------------------------------------------- final
body = f'''
<text x="{W/2}" y="55" text-anchor="middle" font-family="{MONO}" font-size="15" letter-spacing="3" fill="{DIM}">// END OF TRANSMISSION</text>
<text x="{W/2}" y="100" text-anchor="middle" font-family="{SANS}" font-weight="700" font-size="26" fill="{WHITE}">Open to backend / AI engineering roles</text>
'''
write("final", frame(140, body, "final"))

# ---------------------------------------------------------------- buttons
def button(name, label, w=200):
    body = f'''<rect x="1" y="1" width="{w-2}" height="58" rx="8" fill="{BG2}" stroke="{GOLD}" stroke-width="1.5"/>
<text x="{w/2}" y="37" text-anchor="middle" font-family="{MONO}" font-size="16" letter-spacing="2" fill="{GOLD}">{label}</text>'''
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} 60" width="{w}" height="60" role="img" aria-label="{label}">{body}</svg>'
    write(name, svg)


button("btn-linkedin", "LINKEDIN")
button("btn-github", "GITHUB")

print("done")
