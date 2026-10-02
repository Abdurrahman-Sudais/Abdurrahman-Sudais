"""Builds assets/terminal.svg. Edit the STEPS below, then run: python assets/gen_terminal.py"""
from html import escape
from pathlib import Path

BS = chr(92)
HOME = "C:" + BS + "Users" + BS + "sudais"
PROMPT = "PS " + HOME + "> "

BG = "#012456"; W = "#EEEDF0"; Y = "#F9F1A5"; G = "#16C60C"; C = "#61D6D6"; M = "#E074E0"

# Each step: (command, args, output lines). An output line is a string or a list of (text, colour) runs.
STEPS = [
    ("whoami", "", [
        "",
        [("Name      ", G), (': Abdurrahman "Sudais"', W)],
        [("Role      ", G), (": Computer Engineering Student · Full-Stack & Mobile Developer", W)],
        [("Location  ", G), (": Nigeria", W)],
        [("Focus     ", G), (": Mobile apps · AI agents · Full-stack products", W)],
        [("Motto     ", G), (": Building real products, not just demos", W)],
    ]),
    ("Get-ChildItem", "." + BS + "projects", [
        "",
        "    Directory: " + HOME + BS + "projects",
        "",
        [("Mode         LastWriteTime   Name                  Description", G)],
        [("----         -------------   ----                  -----------", G)],
        [("d-----       9/23/2026       ", W), ("travelmate            ", C), ("Flutter carpooling app", W)],
        [("d-----       9/17/2026       ", W), ("equitrade-guardian    ", C), ("AI agent for a nonprofit", W)],
        [("d-----       9/10/2026       ", W), ("studyvid-ai           ", C), ("AI video explainers", W)],
        [("d-----       9/22/2026       ", W), ("aurora                ", C), ("Voice desktop assistant", W)],
        [("d-----       7/28/2026       ", W), ("liab                  ", C), ("AI OS for students", W)],
    ]),
    ("Get-Content", "." + BS + "hackathons.txt", [
        [("AWS Agents for Humans  ", Y), ("->  EquiTrade Guardian (Good Neighbor track)", W)],
        [("Google Gemma 4         ", Y), ("->  LIAB, the AI operating system for students", W)],
    ]),
    ("Get-Content", "." + BS + "status.txt", [
        "Currently : Frontend dev on TravelMate (Flutter carpooling app)",
        "Open to   : Collabs · Open Source · Interesting Ideas",
    ]),
    ("Start-Game", "chess -Opponent $you", [
        [("Board ready. Fair warning: I play like Tal.", M)],
    ]),
    ("Get-Uptime", "", [
        "Coding since way back · Still shipping · No signs of stopping",
    ]),
    ("Test-Connection", "sudais", [
        [("Reply from ", W), ("call-him-sudais.vercel.app", C), (" · X ", W), ("@call_him_sudais", C),
         (" · LinkedIn ", W), ("/in/call-him-sudais", C)],
    ]),
]

LH = 21; X = 20; Y0 = 62; WIDTH = 900; CHAR = 8.4
TYPE = 0.06     # seconds per typed character
PAUSE = 0.5     # pause before each command starts typing
OUT_GAP = 0.25  # pause between Enter and the output appearing

elements = []; keyframes = []; y = Y0; t = 0.2


def runs(line):
    return [(line, W)] if isinstance(line, str) else line


def text(y, line):
    spans = "".join(f'<tspan fill="{c}">{escape(s, quote=False)}</tspan>' for s, c in runs(line))
    return f'<text x="{X}" y="{y}">{spans}</text>'


def appear(at, inner):
    return f'<g class="r" style="animation-delay:{at:.2f}s">{inner}</g>'


elements.append(appear(t, text(y, "Windows PowerShell") + text(y + LH, "Copyright (C) Microsoft Corporation. All rights reserved.")))
y += LH * 3

for cmd, args, output in STEPS:
    t += PAUSE
    typed = cmd + (" " + args if args else "")
    cx = X + len(PROMPT) * CHAR
    n = len(typed)
    dur = n * TYPE
    line = [(PROMPT, W), (cmd, Y)] + ([(" " + args, W)] if args else [])
    # The prompt and command appear together, with a cover (cursor + background) sliding right to "type" it.
    k = len(keyframes)
    keyframes.append(f"@keyframes t{k}{{to{{transform:translateX({n * CHAR:.1f}px)}}}}")
    cover = (f'<g style="animation:t{k} {dur:.2f}s steps({n}) {t:.2f}s forwards,gone .01s steps(1) {t + dur:.2f}s forwards">'
             f'<rect x="{cx:.1f}" y="{y - 15}" width="9" height="19" fill="{W}"/>'
             f'<rect x="{cx + 9:.1f}" y="{y - 15}" width="{WIDTH}" height="19" fill="{BG}"/></g>')
    elements.append(appear(t, text(y, line) + cover))
    t += dur + OUT_GAP
    y += LH
    block = []
    for o in output:
        if any(s for s, _ in runs(o)):
            block.append(text(y, o))
        y += LH
    if block:
        elements.append(appear(t, "".join(block)))
    y += LH

t += PAUSE
cx = X + len(PROMPT) * CHAR
elements.append(appear(t, text(y, PROMPT) + f'<rect class="cur" x="{cx:.1f}" y="{y - 15}" width="9" height="19" fill="{W}"/>'))
H = y + 22

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{H}" viewBox="0 0 {WIDTH} {H}" role="img" aria-label="PowerShell terminal introducing Abdurrahman Sudais: profile, projects, hackathons, status and contact">
<style>
text{{font-family:"Cascadia Mono",Consolas,"Courier New",monospace;font-size:14px;white-space:pre}}
.r{{opacity:0;animation:show .01s steps(1) forwards}}
@keyframes show{{to{{opacity:1}}}}
{chr(10).join(keyframes)}
@keyframes gone{{to{{opacity:0}}}}
.cur{{animation:blink 1s steps(1) infinite}}
@keyframes blink{{50%{{opacity:0}}}}
.t{{font-family:"Segoe UI",Arial,sans-serif;font-size:12px;fill:#E6E6E6}}
</style>
<clipPath id="w"><rect width="{WIDTH}" height="{H}" rx="8"/></clipPath>
<g clip-path="url(#w)">
<rect width="{WIDTH}" height="{H}" fill="{BG}"/>
<rect width="{WIDTH}" height="32" fill="#1F1F1F"/>
<rect x="12" y="9" width="16" height="14" rx="2" fill="#2671BE"/>
<path d="M15 12.5l4 3.5-4 3.5" stroke="#fff" stroke-width="1.6" fill="none"/>
<path d="M20.5 20h4.5" stroke="#fff" stroke-width="1.6"/>
<text class="t" x="38" y="20.5">Windows PowerShell</text>
<path d="M{WIDTH - 128} 16h10" stroke="#CCCCCC"/>
<rect x="{WIDTH - 82.5}" y="11.5" width="9" height="9" stroke="#CCCCCC" fill="none"/>
<path d="M{WIDTH - 33} 11l9 9M{WIDTH - 24} 11l-9 9" stroke="#CCCCCC"/>
{chr(10).join(elements)}
</g>
<rect x=".5" y=".5" width="{WIDTH - 1}" height="{H - 1}" rx="8" fill="none" stroke="#3A3A3A"/>
</svg>
'''
Path(__file__).with_name("terminal.svg").write_text(svg, encoding="utf-8")
print(f"wrote terminal.svg ({WIDTH}x{H}, animation ~{t:.1f}s)")
