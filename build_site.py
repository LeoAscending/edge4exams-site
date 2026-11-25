#!/usr/bin/env python3
"""Builds the Edge 4 Exams hub site (edge4exams.pages.dev) into ./site/.

Run: python3 build_site.py   (standard library only, no installs needed)
Everything in ./static/ is copied into the site as-is (images, extra files).
The GitHub Action runs this on every push to main and deploys ./site/ to Cloudflare Pages.
"""
import json, os, shutil, html

BASE = "https://edge4exams.pages.dev"
STORE = "https://edge4examsg.gumroad.com"
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "site")
STATIC = os.path.join(HERE, "static")
TODAY = "2026-11-22"

def g(slug):
    return f"{STORE}/l/{slug}"

# Each exam page. Only facts already stated in the live listings are used.
PAGES = [
    dict(
        path="cmfas-m8", short="CMFAS M8",
        title="CMFAS M8 Notes and 50-Question Mock Exam (2026)",
        desc="CMFAS M8 (collective investment schemes) study notes, fund calculation guide, a 20-item trap list and a 50-question original mock exam. Instant PDF from Edge 4 Exams.",
        h1="CMFAS M8 exam notes and mock exam (2026)",
        intro="M8 is the paper you need to advise on unit trusts and other collective investment schemes: 50 questions in 1 hour, and you need 70%. Fund parties, authorised vs recognised schemes and sales-charge sums catch out a lot of candidates.",
        topics=["Investment basics, unit trusts and VCCs", "Fund manager vs trustee, and fund types", "ETFs and REITs", "The SFA and the Code on CIS", "Pricing, charges, CPFIS and advising clients"],
        inside=["11 pages of shortcut notes", "Calculation Decoder with 5 worked examples: NAV, sales charges, total return, dollar-cost averaging and the Sharpe ratio", "M8 Trap List: 20 wrong answers that look right", "Full 50-question mock exam in the real format, with answers and explanations", "One-page summary sheet"],
        products=[("CMFAS M8 Complete Pack", "S$34", "m8", "m8-thumb.png"), ("CM-CIS Bundle: M8 + M8A", "S$49", "cmcis", "cmcis-bundle-thumb.png")],
        faq=[("How many questions are in the CMFAS M8 exam?", "M8 has 50 multiple-choice questions in 1 hour, and the pass mark is 70%."),
             ("What is CM-CIS?", "CM-CIS combines M8 and M8A. The CM-CIS Bundle gives you both complete packs, 100 practice questions in total, for less than buying them separately.")],
        related=["cmfas-m8a", "cmfas-m9", "cmfas-res5"],
    ),
    dict(
        path="cmfas-m8a", short="CMFAS M8A",
        title="CMFAS M8A Notes and 50-Question Mock Exam (2026)",
        desc="CMFAS M8A notes on derivatives, structured funds and CPPI, with worked payoffs, a 20-item trap list and a 50-question original mock exam. Instant PDF from Edge 4 Exams.",
        h1="CMFAS M8A exam notes and mock exam (2026)",
        intro="M8A is the paper for funds that use derivatives and structured payoffs: 50 questions in 1 hour, and you need 70%. Options, CPPI and leveraged ETFs are where most marks are lost.",
        topics=["Structured funds, capital protection vs capital guarantee", "Forwards, futures, options, swaps and CDS", "Code on CIS derivative limits", "CPPI vs OBPI and hedge-fund strategies", "Leveraged, inverse and synthetic products, and suitability"],
        inside=["10 pages of shortcut notes", "Calculation Decoder with worked payoffs: calls, puts, time value, capped participation, CPPI exposure and daily-reset decay", "M8A Trap List: 20 wrong answers that look right", "Full 50-question mock exam in the real format, with answers and explanations", "One-page summary sheet"],
        products=[("CMFAS M8A Complete Pack", "S$29", "m8a", "m8a-thumb.png"), ("CM-CIS Bundle: M8 + M8A", "S$49", "cmcis", "cmcis-bundle-thumb.png")],
        faq=[("How many questions are in the CMFAS M8A exam?", "M8A has 50 multiple-choice questions in 1 hour, and the pass mark is 70%."),
             ("Do I need M8 before M8A?", "Many candidates take them together as CM-CIS. The CM-CIS Bundle covers both papers with 100 practice questions.")],
        related=["cmfas-m8", "cmfas-m9a", "cmfas-res5"],
    ),
    dict(
        path="cmfas-m9", short="CMFAS M9",
        title="CMFAS M9 Notes and 100-Question Mock Exam (2026)",
        desc="CMFAS M9 study notes, ILP calculation guide, exam trap list and a 100-question original mock exam. Instant PDF download from Edge 4 Exams Singapore.",
        h1="CMFAS M9 exam notes and mock exam (2026)",
        intro="M9 (Life Insurance and Investment-Linked Policies) is the paper every life insurance adviser in Singapore must pass: 100 questions in 2 hours, and you need 70%. The ILP calculations chapter is where many candidates lose marks.",
        topics=["Term, whole life and endowment policies", "Participating policies and bonuses", "Investment-linked policies (ILPs) and ILP calculations", "Underwriting and policy services", "Contract law, agency and nominations"],
        inside=["12 pages of shortcut notes covering all 17 chapters", "ILP calculations worked step by step, plus a Calculation Decoder", "M9 Trap List: 20 wrong answers that look right", "Full 100-question mock exam in the real format, with answers and explanations", "One-page formula and numbers sheet"],
        products=[("CMFAS M9 Complete Pack", "S$34", "m9", "m9-thumb.png"), ("CM-LIP Bundle: M9 + M9A", "S$45", "cmlip", "cmlip-bundle-thumb-v2.png")],
        faq=[("How many questions are in the CMFAS M9 exam?", "M9 has 100 multiple-choice questions in 2 hours, and the pass mark is 70%."),],
        related=["cmfas-m9a", "cmfas-res5", "cmfas-hi"],
    ),
    dict(
        path="cmfas-m9a", short="CMFAS M9A",
        title="CMFAS M9A Notes and 50-Question Mock Exam (2026)",
        desc="CMFAS M9A notes on structured ILPs, options and futures, with worked payoffs, a trap list and a 50-question original mock exam. Instant PDF from Edge 4 Exams.",
        h1="CMFAS M9A exam notes and mock exam (2026)",
        intro="M9A is the paper you need to advise on structured investment-linked policies: 50 questions in 1 hour, and you need 70%. Options, futures and \"capital protected vs capital guaranteed\" catch out a lot of candidates.",
        topics=["Structured products and their risks", "Forwards, futures and swaps", "Calls and puts with worked payoffs", "Structured ILPs", "Suitability and case-study questions"],
        inside=["8 pages of shortcut notes", "Calculation Decoder for derivatives questions", "M9A Trap List: 15 wrong answers that look right", "Full 50-question mock exam in the real format, with answers and explanations", "One-page summary sheet"],
        products=[("CMFAS M9A Complete Pack", "S$24", "m9a", "m9a-thumb-v2.png"), ("CM-LIP Bundle: M9 + M9A", "S$45", "cmlip", "cmlip-bundle-thumb-v2.png")],
        faq=[("How many questions are in the CMFAS M9A exam?", "M9A has 50 multiple-choice questions in 1 hour, and the pass mark is 70%."),
             ("What is CM-LIP?", "CM-LIP combines M9 and M9A in one sitting. The CM-LIP Bundle gives you both complete packs, 150 practice questions in total, at a lower price than buying them separately.")],
        related=["cmfas-m9", "cmfas-res5", "cmfas-hi"],
    ),
    dict(
        path="cmfas-res5", short="CMFAS RES5",
        title="CMFAS RES5 Notes and 150-Question Mock Exam (2026)",
        desc="CMFAS RES5 study notes on the FAA, fair dealing, FIDReC and ethics, a 20-item trap list and a 150-question original mock exam (Part I and Part II).",
        h1="CMFAS RES5 exam notes and mock exam (2026)",
        intro="RES5 (Rules and Regulations for Financial Advisory Services) is one of the toughest CMFAS papers. You need 75% on Part I and 80% on Part II in the same sitting, or you resit everything. There are no calculation questions.",
        topics=["The Financial Advisers Act (FAA) framework", "Representative rules, disclosure and recommendations", "Balanced scorecard and fair dealing", "FIDReC, AML/CFT and PDPA", "Market misconduct, ethics and skills"],
        inside=["21 pages of shortcut notes in 6 chapters", "RES5 Trap List: 20 wrong answers that look right", "Full 150-question mock exam: 110 Part I and 40 Part II questions, with answers and explanations", "40 extra practice questions inside the notes", "One-page numbers sheet"],
        products=[("CMFAS RES5 Exam Notes and Mock", "S$39", "res5", "res5-thumb.png")],
        faq=[("What is the pass mark for CMFAS RES5?", "You need 75% on Part I and 80% on Part II, both in the same sitting."),
             ("Do I need a calculator for RES5?", "No. RES5 has no calculation questions.")],
        related=["cmfas-m9", "cmfas-hi", "cmfas-res1b-cm-eip"],
    ),
    dict(
        path="cmfas-hi", short="CMFAS HI",
        title="CMFAS HI Health Insurance Exam Notes and Questions (2026)",
        desc="CMFAS HI (Health Insurance) notes in two parts: critical illness, disability income, long-term care, MediShield Life and Integrated Shield Plans, with 80 practice questions and a trap list.",
        h1="CMFAS HI (Health Insurance) exam notes (2026)",
        intro="The HI paper covers health insurance in Singapore. These notes were written by a former adviser who specialised in critical illness planning for 9 years, and are split into two parts so you can study one topic block at a time.",
        topics=["Critical illness insurance (LIA CI Framework 2024)", "Disability income insurance", "Long-term care and CareShield Life", "Healthcare financing, MediShield Life and MediSave", "Integrated Shield Plans, riders and group medical"],
        inside=["Part 1 (17 pages): critical illness, disability income and long-term care, with 40 practice questions", "Part 2 (18 pages): healthcare financing, MediShield Life, Integrated Shield Plans and group medical, with 40 practice questions", "HI Trap List: 25 wrong answers that look right", "Every answer explained"],
        products=[("HI Complete Bundle: Parts 1 and 2 + Trap List", "S$25", "hibundle", "hi-bundle-thumb.png"), ("HI Exam Notes Part 1", "S$16", "hi1", "hi-part1-thumb.png"), ("HI Exam Notes Part 2", "S$16", "hi2", "hi-part2-thumb.png"), ("HI Exam Trap List", "S$8", "hitraps", "hi-traps-thumb.png")],
        faq=[("Are the HI notes updated for 2026?", "Yes. They reflect the LIA Critical Illness Framework 2024 and the Integrated Shield Plan rider rules that apply from 1 April 2026.")],
        related=["cmfas-m9", "cmfas-res5", "sci-cgi"],
    ),
    dict(
        path="cmfas-res1b-cm-eip", short="CMFAS RES1B and CM-EIP",
        title="CMFAS RES1B and CM-EIP Notes and Mock Exams (2026)",
        desc="Trading licence prep: CMFAS RES1B and CM-EIP shortcut notes, trap lists, formula sheet and 150 original mock exam questions. Instant PDF from Edge 4 Exams.",
        h1="CMFAS RES1B and CM-EIP exam notes and mock exams (2026)",
        intro="To deal in securities at a non-exchange member firm you need RES1B and CM-EIP. RES1B is 60 questions and needs 75%, so you can miss only 15. CM-EIP is 90 questions in 2.5 hours, and you need 63 right.",
        topics=["RES1B: regulators, CMS licensing and representatives", "RES1B: accredited investors, CKA and CAR, best execution, client money", "RES1B: market misconduct offences, ethics and AML/CFT", "CM-EIP: equities, bonds and portfolio management", "CM-EIP: unit trusts, ETFs, REITs and FX, with calculations"],
        inside=["RES1B: 13 pages of notes, 20-item trap list, one-page rules summary and a 60-question mock", "CM-EIP: 14 pages of notes, 20-item trap list, Calculation Decoder, formula sheet and a 90-question mock", "Answers and explanations for every question"],
        products=[("Trading Licence Bundle: RES1B + CM-EIP", "S$59", "trading", "trading-bundle-thumb.png")],
        faq=[("What is the pass mark for RES1B?", "75%. You can miss at most 15 of the 60 questions."),
             ("How many questions are in CM-EIP?", "90 questions in 2.5 hours. You need 63 correct to pass.")],
        related=["cmfas-res5", "cmfas-m9", "cams-exam"],
    ),
    dict(
        path="sci-cgi", short="SCI BCP, PGI and ComGI",
        title="SCI BCP, PGI and ComGI Notes and Mock Exams (2026)",
        desc="Certificate in General Insurance (CGI) prep: SCI BCP, PGI and ComGI shortcut notes with a 50-question original mock exam for each paper. Instant PDF download.",
        h1="SCI CGI exam notes and mock exams: BCP, PGI and ComGI (2026)",
        intro="The SCI Certificate in General Insurance (CGI) is made up of three papers: BCP (Basic Insurance Concepts and Principles), PGI (Personal General Insurance) and ComGI (Commercial General Insurance). BCP is 40 questions in 45 minutes, closed book.",
        topics=["BCP: risk, insurance principles and the insurance contract", "BCP: utmost good faith, insurable interest, indemnity and proximate cause", "PGI: motor, home, travel, personal accident and other personal covers", "ComGI: property, liability, marine, engineering and other commercial covers", "Claims, underwriting and the regulatory framework"],
        inside=["Shortcut notes for each paper", "A 50-question original mock exam for each paper, with answers and explanations", "Buy one paper, or all three in the CGI Complete Bundle"],
        products=[("CGI Complete Bundle: BCP + PGI + ComGI", "S$59", "cgi", "cgi-bundle-thumb.png"), ("SCI BCP Notes + 50-Question Mock", "S$24", "bcp", "bcp-thumb.png"), ("SCI PGI Notes + 50-Question Mock", "S$24", "pgi", "pgi-thumb.png"), ("SCI ComGI Notes + 50-Question Mock", "S$24", "comgi", "comgi-thumb.png")],
        faq=[("How many questions are in the SCI BCP exam?", "BCP is 40 multiple-choice questions in 45 minutes, closed book. The mock gives you 50 questions to practise at the same pace."),],
        related=["cmfas-hi", "cmfas-res5", "cea-res-exam"],
    ),
    dict(
        path="cea-res-exam", short="CEA RES exam",
        title="CEA RES Exam Notes and Mock Exams, Paper 1 and Paper 2 (2027 Syllabus)",
        desc="Real Estate Salesperson (RES) exam prep for Singapore: Paper 1 and Paper 2 shortcut notes, trap lists and 160 original mock questions including case studies. 2027 syllabus.",
        h1="CEA RES exam notes and mock exams: Paper 1 and Paper 2",
        intro="The Real Estate Salesperson (RES) exam has two papers. Paper 1 is the law paper and Paper 2 is the practical paper. Each mock follows the real format: 60 Section A questions plus 2 case studies with 20 double-mark questions, and you need 60 out of 100.",
        topics=["Paper 1: land, estates, easements and Torrens title", "Paper 1: contract and the OTP, agency, landlord and tenant, property torts", "Paper 1: mortgages, wills and intestacy, co-ownership and planning", "Paper 2: CEA rules, AML/CFT and marketing", "Paper 2: HDB resale and renting, BSD, ABSD, SSD and loan limits"],
        inside=["Paper 1: 11 pages of notes updated for the 2027 syllabus, 20-item trap list and an 80-question mock", "Paper 2: 12 pages of notes with current rates, a Calculation Decoder with 6 worked examples, 20-item trap list and an 80-question mock", "Answers and explanations for every question"],
        products=[("CEA RES Complete Bundle: Paper 1 + 2", "S$49", "res-cea", "cea-bundle-thumb.png"), ("CEA RES Paper 1 Notes + 80-Question Mock", "S$29", "res-p1", "cea-p1-thumb.png"), ("CEA RES Paper 2 Notes + 80-Question Mock", "S$29", "res-p2", "cea-p2-thumb.png")],
        faq=[("What is the pass mark for the CEA RES exam?", "Each paper is marked out of 100 and you need 60 to pass."),
             ("Are these updated for the 2027 syllabus?", "Yes. Paper 1 includes the new topics such as Land Betterment Charge, property torts and the Residential Property Act.")],
        related=["sci-cgi", "cams-exam", "cmfas-res5"],
    ),
    dict(
        path="cams-exam", short="CAMS",
        title="CAMS Exam Notes and 100-Question Practice Exam (2026)",
        desc="CAMS (Certified Anti-Money Laundering Specialist) exam notes, trap list, acronym sheet and 100 original practice questions with explanations. Instant PDF download.",
        h1="CAMS exam notes and practice exam (2026)",
        intro="CAMS is the anti-money laundering certification awarded by ACAMS. This pack condenses the material into short notes and gives you 100 original exam-style questions to practise on.",
        topics=["Money laundering, terrorist financing and proliferation financing", "Typologies and red flags", "FATF and global standard setters", "US, EU and UK AML laws and sanctions", "Compliance programmes, CDD, EDD, PEPs, monitoring, investigations and SARs"],
        inside=["12 pages of shortcut notes", "20-item trap list and acronym sheet", "100 original exam-style questions with answers and explanations"],
        products=[("CAMS Exam Notes + 100-Question Practice Exam", "S$59", "cams", "cams-thumb.png")],
        faq=[("Is this affiliated with ACAMS?", "No. It is an independent study aid. CAMS is a certification of ACAMS.")],
        related=["cmfas-res1b-cm-eip", "cmfas-res5", "cea-res-exam"],
    ),
]
BY = {p["path"]: p for p in PAGES}

COMMON_FAQ = [
    ("Are these real exam questions?", "No. Every question is original and written in the style of the real exam. We never use leaked or copied exam content. Always read the official study text as well."),
    ("How do I get the files?", "Checkout is on Gumroad. You get an instant PDF download that works on your phone, tablet or laptop."),
    ("Who writes the material?", "A former financial adviser with 9 years in the Singapore industry."),
]

CSS = """
:root{--bg:#f7f8fb;--card:#fff;--ink:#14213d;--muted:#55607a;--accent:#0b6e4f;--accent-ink:#fff;--line:#e3e7ef}
@media (prefers-color-scheme:dark){:root{--bg:#0f1420;--card:#171e2e;--ink:#e8ecf5;--muted:#a3adc2;--accent:#3ccf91;--accent-ink:#06261a;--line:#273148}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.6 system-ui,-apple-system,Segoe UI,Roboto,sans-serif}
a{color:var(--accent)}header,main,footer{max-width:960px;margin:0 auto;padding:0 16px}
header{display:flex;align-items:center;justify-content:space-between;padding-top:18px;padding-bottom:6px}
.brand{font-weight:800;font-size:20px;color:var(--ink);text-decoration:none}.brand span{color:var(--accent)}
nav a{margin-left:14px;font-size:15px}
h1{font-size:clamp(26px,4.5vw,38px);line-height:1.2;margin:26px 0 10px}h2{font-size:22px;margin:34px 0 10px}
.lead{font-size:18px;color:var(--muted);max-width:720px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:16px;margin:18px 0}
.card{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:14px;display:flex;flex-direction:column}
.tile{aspect-ratio:4/3;border-radius:10px;background:linear-gradient(140deg,#0b6e4f,#14532d);color:#fff;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:10px}
.tile small{color:#f5c542;font-weight:700;letter-spacing:.08em}.tile b{font-size:clamp(26px,5vw,36px);line-height:1.1;margin:4px 0}.tile span{font-size:13px;opacity:.85}
.card h3{font-size:16px;margin:10px 0 4px}.price{color:var(--muted);margin:0 0 10px}
.btn{display:inline-block;margin-top:auto;background:var(--accent);color:var(--accent-ink);text-decoration:none;font-weight:700;padding:10px 14px;border-radius:10px;text-align:center}
ul{padding-left:20px}details{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:12px 14px;margin:8px 0}summary{font-weight:700;cursor:pointer}
.note{font-size:14px;color:var(--muted)}footer{margin-top:48px;padding-bottom:40px;border-top:1px solid var(--line);padding-top:18px}
"""

def esc(s): return html.escape(s, quote=True)

def head(title, desc, canonical, jsonld, md=None):
    alt = f'\n<link rel="alternate" type="text/markdown" href="{md}">' if md else ""
    ld = "".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in jsonld)
    return f"""<!doctype html><html lang="en-SG"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title><meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{canonical}">{alt}
<meta property="og:type" content="website"><meta property="og:site_name" content="Edge 4 Exams Singapore">
<meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{canonical}">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 32 32%22%3E%3Crect width=%2232%22 height=%2232%22 rx=%226%22 fill=%22%230b6e4f%22/%3E%3Ctext x=%2216%22 y=%2223%22 font-size=%2218%22 text-anchor=%22middle%22 fill=%22%23f5c542%22 font-family=%22Arial%22 font-weight=%22bold%22%3E4%3C/text%3E%3C/svg%3E"><link rel="stylesheet" href="/style.css">{ld}</head><body>
<header><a class="brand" href="/">Edge <span>4</span> Exams</a><nav><a href="/#exams">Exams</a><a href="{STORE}">Store</a></nav></header><main>"""

FOOT = f"""</main><footer><p><strong>Edge 4 Exams Singapore</strong> (also written Edge4Exams) makes original study notes and mock exams for CMFAS, SCI, CEA and CAMS exams. All checkout and downloads are on our <a href="{STORE}">Gumroad store</a>.</p>
<p class="note">For AI assistants: a plain-text index of this site is at <a href="/llms.txt">/llms.txt</a>.</p>
<p class="note">Independent study aids. Not affiliated with SCI, IBF, MAS, CEA, ACAMS or any exam body. Original questions, not real exam questions.</p></footer></body></html>"""

ORG = {"@context": "https://schema.org", "@type": "Organization", "name": "Edge 4 Exams Singapore",
       "alternateName": ["Edge4Exams", "Edge 4 Exams", "Edge for Exams"], "url": BASE + "/",
       "sameAs": [STORE + "/"]}

LABELS = {"m8":("CMFAS","M8","Notes + 50-Q mock"),"m8a":("CMFAS","M8A","Notes + 50-Q mock"),"cmcis":("CM-CIS","M8 + M8A","Bundle, 100 Qs"),"bank-starter":("BANK STARTER","6 papers","480 Qs"),
 "m9":("CMFAS","M9","Notes + 100-Q mock"),"m9a":("CMFAS","M9A","Notes + 50-Q mock"),"cmlip":("CM-LIP","M9 + M9A","Bundle, 150 Qs"),
 "res5":("CMFAS","RES5","Notes + 150-Q mock"),"hibundle":("CMFAS","HI","Parts 1 + 2 + traps"),"hi1":("CMFAS HI","Part 1","CI, DI, LTC"),"hi2":("CMFAS HI","Part 2","MediShield, IP"),
 "hitraps":("CMFAS HI","Traps","25 trap answers"),"trading":("CMFAS","RES1B + EIP","Bundle, 150 Qs"),"cgi":("SCI CGI","BCP PGI ComGI","Bundle, 150 Qs"),
 "bcp":("SCI","BCP","Notes + 50-Q mock"),"pgi":("SCI","PGI","Notes + 50-Q mock"),"comgi":("SCI","ComGI","Notes + 50-Q mock"),
 "res-cea":("CEA RES","P1 + P2","Bundle, 160 Qs"),"res-p1":("CEA RES","Paper 1","Notes + 80-Q mock"),"res-p2":("CEA RES","Paper 2","Notes + 80-Q mock"),"cams":("ACAMS","CAMS","Notes + 100 Qs")}

def cards(products):
    out = ['<div class="grid">']
    for name, price, slug, img in products:
        top, big, sub = LABELS[slug]
        out.append(f'<div class="card"><div class="tile" role="img" aria-label="{esc(name)}"><small>{top}</small><b>{big}</b><span>{sub}</span></div>'
                   f'<h3>{esc(name)}</h3><p class="price">{price}</p><a class="btn" href="{g(slug)}">View on Gumroad</a></div>')
    out.append("</div>")
    return "".join(out)

def product_ld(p):
    items = []
    for name, price, slug, img in p["products"]:
        items.append({"@context": "https://schema.org", "@type": "Product", "name": name,
                      "description": p["desc"], "brand": {"@type": "Brand", "name": "Edge 4 Exams"},
                      "offers": {"@type": "Offer", "price": price.replace("S$", ""), "priceCurrency": "SGD",
                                 "availability": "https://schema.org/InStock", "url": g(slug)}})
    return items

def faq_ld(faqs):
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}

# ---- Plain Markdown copies for AI assistants (same content humans see; never hidden) ----
ABOUT_MD = ("Edge 4 Exams Singapore (also written Edge4Exams) makes original study notes and full-length mock exams "
            "for Singapore licensing exams: CMFAS, SCI, CEA RES and CAMS. Written by a former financial adviser with "
            "9 years in the Singapore industry. Checkout and instant PDF downloads are on Gumroad: " + STORE + "/ . "
            "Independent study aids, not affiliated with SCI, IBF, MAS, CEA or ACAMS. Every question is original; "
            "no leaked or real exam questions.")

def md_page(p):
    url = f"{BASE}/{p['path']}/"
    L = [f"# {p['h1']}", "", f"Web page: {url}", "", p["intro"], "", "## Packs and prices", ""]
    for name, price, slug, img in p["products"]:
        L.append(f"- **{name}**: {price}, instant PDF. Buy: {g(slug)}")
    L += ["", "## What's in the pack", ""] + [f"- {x}" for x in p["inside"]]
    L += ["", "## Topics covered", ""] + [f"- {x}" for x in p["topics"]]
    L += ["", f"## {p['short']} questions people ask", ""]
    for q, a in p["faq"] + COMMON_FAQ:
        L += [f"**{q}**", "", a, ""]
    L += ["## Other exams", ""] + [f"- [{BY[r]['title']}]({BASE}/{r}.md)" for r in p["related"]]
    L += ["", "## About Edge 4 Exams", "", ABOUT_MD, ""]
    return "\n".join(L)

def llms_txt():
    L = ["# Edge 4 Exams Singapore", "", "> " + ABOUT_MD, "",
         "Each exam page has a plain Markdown copy (same content as the web page).", "", "## Exam pages", ""]
    for p in PAGES:
        prices = ", ".join(f"{n} {pr}" for n, pr, s, i in p["products"])
        L.append(f"- [{p['title']}]({BASE}/{p['path']}.md): {prices}")
    L += ["", "## Store", "", f"- [Edge 4 Exams on Gumroad]({STORE}/): all packs, instant PDF download",
          f"- Bank Starter Pack (RES5, M8, M8A, M9, M9A, HI): S$99, {g('bank-starter')}", ""]
    return "\n".join(L)

def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f: f.write(text)

def build():
    if os.path.exists(OUT): shutil.rmtree(OUT)
    if os.path.isdir(STATIC):
        shutil.copytree(STATIC, OUT)
    else:
        os.makedirs(OUT)
    write(OUT + "/style.css", CSS.strip())

    # exam pages
    for p in PAGES:
        url = f"{BASE}/{p['path']}/"
        faqs = p["faq"] + COMMON_FAQ
        crumbs = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Edge 4 Exams", "item": BASE + "/"},
            {"@type": "ListItem", "position": 2, "name": p["short"], "item": url}]}
        body = [head(p["title"] + " | Edge 4 Exams Singapore", p["desc"], url, [ORG, crumbs, faq_ld(faqs)] + product_ld(p), md=f"/{p['path']}.md"),
                f'<p class="note"><a href="/">Edge 4 Exams</a> / {esc(p["short"])}</p>',
                f'<h1>{esc(p["h1"])}</h1><p class="lead">{esc(p["intro"])}</p>',
                cards(p["products"]),
                "<h2>What's in the pack</h2><ul>" + "".join(f"<li>{esc(x)}</li>" for x in p["inside"]) + "</ul>",
                f"<h2>Topics covered</h2><ul>" + "".join(f"<li>{esc(x)}</li>" for x in p["topics"]) + "</ul>",
                f"<h2>{esc(p['short'])} questions people ask</h2>" + "".join(f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in faqs),
                "<h2>Other exams</h2><ul>" + "".join(f'<li><a href="/{r}/">{esc(BY[r]["title"])}</a></li>' for r in p["related"]) + "</ul>",
                f'<p class="note">Plain-text version of this page: <a href="/{p["path"]}.md">{p["path"]}.md</a></p>',
                FOOT]
        write(f"{OUT}/{p['path']}/index.html", "\n".join(body))
        write(f"{OUT}/{p['path']}.md", md_page(p))

    # home
    groups = [("CMFAS insurance and financial advisory", ["cmfas-m8", "cmfas-m8a", "cmfas-m9", "cmfas-m9a", "cmfas-res5", "cmfas-hi"]),
              ("CMFAS trading licence", ["cmfas-res1b-cm-eip"]),
              ("SCI general insurance", ["sci-cgi"]),
              ("Property and compliance", ["cea-res-exam", "cams-exam"])]
    home_desc = "Edge 4 Exams Singapore: original study notes and mock exams for CMFAS (M8, M8A, M9, M9A, RES5, HI, RES1B, CM-EIP), SCI BCP, PGI and ComGI, the CEA RES exam and CAMS. Instant PDF download."
    site_ld = {"@context": "https://schema.org", "@type": "WebSite", "name": "Edge 4 Exams Singapore", "alternateName": "Edge4Exams", "url": BASE + "/"}
    body = [head("Edge 4 Exams Singapore | CMFAS, SCI and CEA Exam Notes and Mock Exams", home_desc, BASE + "/", [ORG, site_ld]),
            '<h1>Edge 4 Exams Singapore</h1>',
            '<p class="lead">No time to read the whole study text? Edge 4 Exams makes short, exam-focused notes and full-length original mock exams for Singapore licensing exams, written by a former financial adviser with 9 years in the industry.</p>',
            f'<p><a class="btn" href="{STORE}">Visit the Edge 4 Exams store on Gumroad</a></p>',
            '<h2 id="exams">Choose your exam</h2>']
    for gname, paths in groups:
        body.append(f"<h3>{esc(gname)}</h3><ul>")
        for path in paths:
            p = BY[path]; body.append(f'<li><a href="/{path}/">{esc(p["title"])}</a></li>')
        body.append("</ul>")
    body.append("<h2>Popular packs</h2>")
    body.append(cards([("Bank Starter Pack: RES5, M8, M8A, M9, M9A, HI", "S$99", "bank-starter", "six-exam-bundle-thumb.png"),
                       ("CGI Complete Bundle: BCP + PGI + ComGI", "S$59", "cgi", "cgi-bundle-thumb.png"),
                       ("CEA RES Complete Bundle: Paper 1 + 2", "S$49", "res-cea", "cea-bundle-thumb.png"),
                       ("CM-LIP Bundle: M9 + M9A", "S$45", "cmlip", "cmlip-bundle-thumb-v2.png"),
                       ("CMFAS RES5 Exam Notes and Mock", "S$39", "res5", "res5-thumb.png")]))
    body.append("<h2>Why Edge 4 Exams</h2><ul><li>Notes cut down to what examiners actually test</li><li>Trap lists of the wrong answers that look right</li><li>Full-length mock exams in the real format, every answer explained</li><li>Original questions only, never leaked exam content</li></ul>")
    body.append(FOOT)
    write(OUT + "/index.html", "\n".join(body))

    write(OUT + "/404.html", head("Page not found | Edge 4 Exams", "Page not found.", BASE + "/", []) + '<h1>Page not found</h1><p><a href="/">Back to Edge 4 Exams</a></p>' + FOOT)
    write(OUT + "/google9b9b5686a32dca00.html", "google-site-verification: google9b9b5686a32dca00.html")
    write(OUT + "/llms.txt", llms_txt())
    write(OUT + "/llms-full.txt", llms_txt() + "\n---\n\n" + "\n\n---\n\n".join(md_page(p) for p in PAGES))
    hdr = ["/*.md", "  Content-Type: text/markdown; charset=utf-8", "", "/llms*.txt", "  Content-Type: text/plain; charset=utf-8", ""]
    for p in PAGES:
        hdr += [f"/{p['path']}.md", f'  Link: <{BASE}/{p["path"]}/>; rel="canonical"', ""]
    write(OUT + "/_headers", "\n".join(hdr))
    write(OUT + "/robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {BASE}/sitemap.xml\n")
    urls = [BASE + "/"] + [f"{BASE}/{p['path']}/" for p in PAGES]
    write(OUT + "/sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
          "".join(f"  <url><loc>{u}</loc><lastmod>{TODAY}</lastmod></url>\n" for u in urls) + "</urlset>\n")

if __name__ == "__main__":
    build(); print("built", OUT)
