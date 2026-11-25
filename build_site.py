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
TODAY = "2026-11-25"

def g(slug):
    return f"{STORE}/l/{slug}"

# Each exam page. Only facts already stated in the live listings are used.
PAGES = [
    dict(
        path="psle-math", short="PSLE Math", common_faq=False, topics_label="Methods covered", faq_label="PSLE Math questions parents ask",
        title="PSLE Math Heuristics Pack for P6: 27 Methods with Bar Models",
        desc="P6 PSLE Math heuristics pack: 27 problem-solving methods, each with a worked example, bar model diagrams, common mistakes, practice questions and a full answer key. Instant PDF download.",
        h1="PSLE Math heuristics pack for P6 (27 methods)",
        intro="Most PSLE Math word problems can be solved with one of 27 methods. This pack teaches each one with a fully worked example and a bar model drawn to the exact numbers, then gives your child a practice question to try alone.",
        topics=["Models and before-after: part-whole, comparison, constant total, constant difference, constant part",
                "Fractions, ratio and percentage: equal fractions, remainder concept, repeated identity, equal stage, percentage change",
                "Number methods: excess and shortage, supposition, grouping, guess and check, working backwards",
                "Patterns, geometry and speed: systematic listing, patterns, overlapping areas, meeting and catching up, averages",
                "Advanced PSLE methods: units and parts, percentage transfer, simultaneous concept, number \u00d7 value, supposition with a penalty, work rate, gap and difference"],
        inside=["27 problem-solving heuristics, each with a fully worked PSLE-style example",
                "14 bar models and diagrams, drawn to the exact numbers in each question",
                "\"Spot it when\" clue words, so your child knows which method to use",
                "The most common mistake for each method",
                "27 practice questions with a full answer key"],
        products=[("P6 Math Heuristics Pack: 27 Methods with Bar Models", "S$29", "p6-math-heuristics", None)],
        free=("Free sample: 3 PSLE Math methods with bar models", "free-psle-math-sample", "Not sure yet? Try 3 of the 27 methods first, each with a worked example, bar model and practice question. Free 4-page PDF."),
        faq=[("Are these real PSLE questions?", "No. Every question is original and uses the problem-solving heuristics taught in Singapore primary schools. We never use real or copied exam papers."),
             ("Who is it for?", "P6 students preparing for PSLE Math, and P5 students who are starting on word-problem heuristics."),
             ("How should my child use it?", "One method a day for about four weeks: read the worked example together, cover the solution, let your child redo it alone, then try the practice question."),
             ("How do I get the file?", "Checkout is on Gumroad. You get an instant PDF download you can print or use on a tablet.")],
        related=[],
    ),
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

# ---------------------------------------------------------------------------
# Site sections. PSLE is kept separate from the professional licensing exams:
# its own look (cream hero), its own nav, footer and About text.
PSLE_PATHS = {"psle-math"}
def is_psle(path): return path in PSLE_PATHS

PRO_GROUPS = [("CMFAS insurance and financial advisory", ["cmfas-m8", "cmfas-m8a", "cmfas-m9", "cmfas-m9a", "cmfas-res5", "cmfas-hi"]),
              ("CMFAS trading licence", ["cmfas-res1b-cm-eip"]),
              ("SCI general insurance", ["sci-cgi"]),
              ("Property and compliance", ["cea-res-exam", "cams-exam"])]

# Images live in static/img (copied to /img/). Product thumbnails are the real Gumroad thumbnails.
SLUG_IMG = {"p6-math-heuristics": "psle-math-thumb.webp"}
def img_for(slug, img):
    return "/img/" + (SLUG_IMG.get(slug) or (img or "").replace(".png", ".webp"))

OG = {"cmfas-m8": "og-m8.jpg", "cmfas-m8a": "og-m8a.jpg", "cmfas-m9": "og-m9.jpg", "cmfas-m9a": "og-m9a.jpg",
      "cmfas-res5": "og-res5.jpg", "cmfas-hi": "og-hi.jpg", "cmfas-res1b-cm-eip": "og-res1b.jpg", "sci-cgi": "og-cgi.jpg",
      "cea-res-exam": "og-cea.jpg", "cams-exam": "og-cams.jpg", "psle-math": "og-psle.jpg"}
OG_SIZE = {"og-home.jpg": (1200, 630), "og-psle.jpg": (1200, 675)}

# Public marketing images already used on Carousell/Instagram (never paid pages).
TEASER = {"cmfas-hi": ("/img/teaser-hi-traps.webp", "CMFAS HI exam traps: four wrong answers that look right, with the correct answer beside each", "A peek at the HI Trap List: the wrong answers that look right, and the truth beside each one."),
          "cmfas-m9a": ("/img/teaser-m9a-calls-puts.webp", "CMFAS M9A trick: cAll points up, pUt points down", "One of the shortcuts in the M9A pack: never mix up calls and puts again.")}

CSS = """
:root{--bg:#f6f8f7;--card:#fff;--ink:#0f2a2a;--muted:#4b6363;--line:#dfe8e6;--teal:#0f6e6e;--teal-2:#0b5a5a;--tint:#e9f3f2;--cream:#fbf6e9;--accent:#0b6e4f;--accent-dark:#14532d;--accent-ink:#fff;--gold:#f5c542;--gold-ink:#1f1a05;--teal-text:#0f6e6e;--shadow:0 10px 30px rgba(15,42,42,.10)}
@media (prefers-color-scheme:dark){:root{--bg:#0d1716;--card:#13201f;--ink:#e6f0ef;--muted:#a3b8b6;--line:#243433;--tint:#122423;--cream:#1d1a12;--accent:#3ccf91;--accent-dark:#2aa874;--accent-ink:#06261a;--teal-text:#6fd3c8;--shadow:0 10px 30px rgba(0,0,0,.35)}}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.6 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;-webkit-font-smoothing:antialiased}
img{max-width:100%;height:auto;display:block}
a{color:var(--accent)}
.wrap,main{max-width:1080px;margin:0 auto;padding:0 20px}
.site-head{background:var(--teal);color:#fff}
.site-head .wrap{display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap;padding-top:12px;padding-bottom:12px}
.brand{display:flex;align-items:center;gap:10px;font-weight:800;font-size:20px;color:#fff;text-decoration:none;letter-spacing:-.01em}
.brand img{width:34px;height:34px;border-radius:9px}
.brand span{color:var(--gold)}
.brand .chip{font-size:12px;letter-spacing:.08em;background:var(--gold);color:var(--gold-ink);padding:2px 8px;border-radius:6px;margin-left:2px}
nav{display:flex;gap:18px;flex-wrap:wrap}
nav a{color:#e3f2f2;font-size:15px;font-weight:600;text-decoration:none}
nav a:hover{color:var(--gold)}
.btn{display:inline-block;background:var(--accent);color:var(--accent-ink);text-decoration:none;font-weight:700;padding:12px 18px;border-radius:10px;text-align:center;border:0}
.btn:hover{background:var(--accent-dark)}
.btn-gold{background:var(--gold);color:var(--gold-ink)}.btn-gold:hover{background:#ffd75e}
.btn-ghost{background:transparent;color:#fff;border:1.5px solid rgba(255,255,255,.6)}.btn-ghost:hover{background:rgba(255,255,255,.08)}
/* home hero */
.hero{background:linear-gradient(160deg,var(--teal) 0%,var(--teal-2) 100%);color:#fff;padding:44px 0 88px;overflow:hidden}
.hero .wrap{display:grid;grid-template-columns:1.15fr .85fr;gap:28px;align-items:center}
.hero h1{font-size:clamp(32px,5.2vw,54px);line-height:1.06;margin:0 0 16px;letter-spacing:-.025em}
.hero .lead{color:#d6ecec;font-size:clamp(17px,2.1vw,20px);margin:0 0 22px;max-width:620px}
.badges{display:flex;flex-wrap:wrap;gap:8px;list-style:none;padding:0;margin:0 0 26px}
.badges li{border:1.5px solid rgba(255,255,255,.3);border-radius:999px;padding:5px 12px;font-size:14px;color:#eef8f8}
.cta{display:flex;flex-wrap:wrap;gap:12px}
.fan{position:relative;height:340px}
.fan .book{position:absolute;width:56%}
.fan .b1{left:0;top:54px;transform:rotate(-9deg)}
.fan .b2{left:22%;top:0;z-index:2}
.fan .b3{left:44%;top:66px;transform:rotate(8deg);z-index:3}
/* booklet mockup: real thumbnail as the cover, with page edges behind */
.book{position:relative;aspect-ratio:1}
.book::before,.book::after{content:"";position:absolute;inset:0;border-radius:10px;background:#fff;border:1px solid #d9e3e1}
.book::before{transform:translate(9px,9px)}
.book::after{transform:translate(5px,5px)}
.book img{position:relative;z-index:1;width:100%;height:100%;object-fit:cover;border-radius:10px;box-shadow:0 14px 34px rgba(0,0,0,.28)}
/* trust strip */
.trust{position:relative;margin-top:-52px;background:var(--card);border:1px solid var(--line);border-radius:18px;box-shadow:var(--shadow);display:grid;grid-template-columns:repeat(4,1fr);text-align:center}
.trust div{padding:18px 12px;border-left:1px solid var(--line)}
.trust div:first-child{border-left:0}
.trust b{display:block;font-size:clamp(20px,2.6vw,26px);color:var(--teal-text);letter-spacing:-.01em}
.trust span{font-size:14px;color:var(--muted)}
h1{font-size:clamp(28px,4.4vw,42px);line-height:1.12;margin:0 0 12px;letter-spacing:-.02em}
h2{font-size:clamp(23px,3vw,30px);margin:56px 0 6px;letter-spacing:-.015em}
h3{letter-spacing:-.01em}
.sub{color:var(--muted);margin:0 0 20px}
.lead{font-size:18px;color:var(--muted);max-width:720px}
/* exam cards */
.group{margin:26px 0 8px;font-size:13px;font-weight:800;letter-spacing:.09em;text-transform:uppercase;color:var(--teal-text)}
.exams{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:14px}
.exam{display:flex;gap:14px;align-items:center;background:var(--card);border:1px solid var(--line);border-radius:14px;padding:12px;text-decoration:none;color:var(--ink);transition:transform .15s,box-shadow .15s,border-color .15s}
.exam:hover{transform:translateY(-2px);box-shadow:var(--shadow);border-color:#b9d6d3}
.exam img{width:68px;height:68px;border-radius:10px;flex:none}
.exam b{display:block;font-size:17px;line-height:1.25}
.exam span{display:block;font-size:14px;color:var(--muted)}
.exam em{font-style:normal;font-size:14px;font-weight:700;color:var(--accent)}
/* product cards */
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(210px,1fr));gap:18px;margin:18px 0}
.card{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:18px 18px 16px;display:flex;flex-direction:column;transition:transform .15s,box-shadow .15s}
.card:hover{transform:translateY(-2px);box-shadow:var(--shadow)}
.card .book{width:82%;margin:4px auto 18px}
.card h3{font-size:16px;margin:0 0 6px;line-height:1.35}
.price{color:var(--ink);font-weight:800;font-size:18px;margin:0 0 14px}
.card .btn{margin-top:auto}
/* look inside */
.peek{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,400px));gap:20px;margin:18px 0}
figure{margin:0;background:var(--card);border:1px solid var(--line);border-radius:16px;overflow:hidden}
figure img{width:100%;aspect-ratio:1;object-fit:cover}
figcaption{padding:14px 16px;font-size:15px;color:var(--muted)}
/* steps */
.steps{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:16px;list-style:none;padding:0;margin:18px 0;counter-reset:s}
.steps li{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:20px;counter-increment:s}
.steps li::before{content:counter(s);display:flex;align-items:center;justify-content:center;width:34px;height:34px;border-radius:50%;background:var(--gold);color:var(--gold-ink);font-weight:800;margin-bottom:10px}
.steps b{display:block;font-size:17px;margin-bottom:4px}
.steps span{color:var(--muted);font-size:15px}
.why{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:14px;list-style:none;padding:0;margin:18px 0}
.btn-outline{background:transparent;color:var(--accent);border:2px solid var(--accent)}
.btn-outline:hover{background:var(--accent);color:var(--accent-ink)}
.free{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:12px 20px;background:var(--card);border:1px dashed var(--gold);border-left:5px solid var(--gold);border-radius:14px;padding:14px 18px;margin:28px 0 0}
.free p{margin:0;max-width:620px}
.free .btn{margin-top:0}
.why li{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:16px 18px;font-weight:600}
.why li::before{content:"";display:block;width:28px;height:4px;border-radius:2px;background:var(--gold);margin-bottom:10px}
/* exam page */
.crumbs{font-size:14px;color:var(--muted);margin:18px 0 0}
.crumbs a{color:var(--muted)}
.phero{background:var(--tint);border-bottom:1px solid var(--line);padding:30px 0 40px}
.phero .wrap{display:grid;grid-template-columns:1.3fr .7fr;gap:36px;align-items:center}
.phero .book{width:min(300px,100%);margin:0 auto}
.buy{display:flex;flex-wrap:wrap;align-items:center;gap:14px;margin-top:20px}
.buy .amount{font-size:28px;font-weight:800;letter-spacing:-.01em}
.buy small{display:block;width:100%;color:var(--muted);font-size:14px}
.cols{display:grid;grid-template-columns:1fr 1fr;gap:28px}
.ticks{list-style:none;padding:0;margin:14px 0}
.ticks li{position:relative;padding:10px 0 10px 34px;border-bottom:1px dashed var(--line)}
.ticks li::before{content:"";position:absolute;left:0;top:12px;width:22px;height:22px;border-radius:50%;background:var(--teal) url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='M6 12.5l4 4 8-9' fill='none' stroke='%23f5c542' stroke-width='3' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E") center/16px no-repeat}
.peek-one{max-width:420px}
details{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:12px 16px;margin:8px 0}
summary{font-weight:700;cursor:pointer}
.note{font-size:14px;color:var(--muted)}
/* PSLE: separate, warmer look */
.psle .phero{background:var(--cream)}
.psle .site-head{background:#0f2a2a}
.bar-fig{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:22px;max-width:560px}
@media (prefers-color-scheme:dark){.bar-fig{background:#f7f3e8}}
/* footer */
.site-foot{margin-top:72px;background:var(--card);border-top:1px solid var(--line)}
.site-foot .wrap{padding-top:32px;padding-bottom:40px}
.fcols{display:grid;grid-template-columns:1.4fr 1fr 1fr;gap:28px}
.fcols h4{margin:0 0 8px;font-size:14px;letter-spacing:.06em;text-transform:uppercase;color:var(--teal-text)}
.fcols ul{list-style:none;padding:0;margin:0}
.fcols li{margin:4px 0;font-size:15px}
@media (max-width:860px){
 .hero .wrap,.phero .wrap,.cols,.fcols{grid-template-columns:1fr}
 .fan{height:250px;max-width:380px;width:100%;margin:6px auto 0}
 .trust{grid-template-columns:repeat(2,1fr)}
 .trust div:nth-child(3){border-left:0}
 .trust div:nth-child(n+3){border-top:1px solid var(--line)}
 .phero .book{width:200px}
}
@media (max-width:560px){
 .fan{height:210px;max-width:300px}
 .fan .book{width:50%}
 .fan .b1{left:4%}.fan .b2{left:25%}.fan .b3{left:46%}
 .grid{grid-template-columns:repeat(2,1fr);gap:12px}
 .card{padding:12px}
 .card .book{width:88%;margin-bottom:14px}
 .card h3{font-size:14px}
 .price{font-size:16px;margin-bottom:10px}
 .card .btn{padding:10px 8px;font-size:14px}
}
"""

def esc(s): return html.escape(s, quote=True)

def head(title, desc, canonical, jsonld, md=None, og="og-home.jpg", psle=False, hero=""):
    alt = f'\n<link rel="alternate" type="text/markdown" href="{md}">' if md else ""
    ld = "".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in jsonld)
    w, h = OG_SIZE.get(og, (1200, 675))
    if psle:
        nav = f'<a href="/psle-math/">PSLE Math</a><a href="/psle-math/#inside">What\'s inside</a><a href="{g("p6-math-heuristics")}">Buy the pack</a>'
        chip = '<span class="chip">PSLE</span>'
    else:
        nav = f'<a href="/#exams">Exams</a><a href="/#how">How it works</a><a href="{STORE}">Store</a>'
        chip = ""
    return f"""<!doctype html><html lang="en-SG"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title><meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{canonical}">{alt}
<meta name="theme-color" content="#0f6e6e">
<meta property="og:type" content="website"><meta property="og:site_name" content="Edge 4 Exams Singapore"><meta property="og:locale" content="en_SG">
<meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{canonical}"><meta property="og:image" content="{BASE}/img/{og}"><meta property="og:image:width" content="{w}"><meta property="og:image:height" content="{h}">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="{BASE}/img/{og}">
<link rel="icon" type="image/png" sizes="32x32" href="/img/favicon-32.png"><link rel="apple-touch-icon" href="/img/apple-touch-icon.png">
<link rel="stylesheet" href="/style.css">{ld}</head><body{' class="psle"' if psle else ''}>
<header class="site-head"><div class="wrap"><a class="brand" href="{'/psle-math/' if psle else '/'}"><img src="/img/logo-64.png" alt="" width="34" height="34">Edge <span>4</span> Exams{chip}</a><nav>{nav}</nav></div></header>{hero}<main>"""

def foot(psle=False):
    if psle:
        return f"""</main><footer class="site-foot"><div class="wrap"><div class="fcols">
<div><h4>Edge 4 Exams · PSLE</h4><p class="note">Clear, worked methods for PSLE Math, drawn as bar models and diagrams. Checkout and instant PDF download on Gumroad.</p></div>
<div><h4>PSLE</h4><ul><li><a href="/psle-math/">PSLE Math heuristics (P6)</a></li><li><a href="{g('p6-math-heuristics')}">Buy the pack</a></li></ul></div>
<div><h4>More</h4><ul><li><a href="/">Edge 4 Exams home</a></li><li><a href="/llms.txt">Plain-text index (llms.txt)</a></li></ul></div></div>
<p class="note">Independent study aid. Not affiliated with MOE or SEAB. Original questions, not real exam questions.</p></div></footer></body></html>"""
    exam_links = "".join(f'<li><a href="/{p}/">{esc(BY[p]["short"])}</a></li>' for _, ps in PRO_GROUPS for p in ps)
    return f"""</main><footer class="site-foot"><div class="wrap"><div class="fcols">
<div><h4>Edge 4 Exams Singapore</h4><p class="note"><strong>Edge 4 Exams</strong> (also written Edge4Exams) makes short notes, trap lists and full-length original mock exams for Singapore licensing exams. Written by a former financial adviser with 9 years in the industry. Checkout and downloads are on our <a href="{STORE}">Gumroad store</a>.</p></div>
<div><h4>Exams</h4><ul>{exam_links}</ul></div>
<div><h4>More</h4><ul><li><a href="{STORE}">Store</a></li><li><a href="/llms.txt">Plain-text index (llms.txt)</a></li><li><a href="/psle-math/">Primary school: PSLE Math</a></li></ul></div></div>
<p class="note">Independent study aids. Not affiliated with SCI, IBF, MAS, CEA, ACAMS or any exam body. Original questions, not real exam questions.</p></div></footer></body></html>"""

ORG = {"@context": "https://schema.org", "@type": "Organization", "name": "Edge 4 Exams Singapore",
       "alternateName": ["Edge4Exams", "Edge 4 Exams", "Edge for Exams"], "url": BASE + "/",
       "logo": BASE + "/img/logo-512.png", "sameAs": [STORE + "/"]}

LABELS = {"m8":("CMFAS","M8","Notes + 50-Q mock"),"m8a":("CMFAS","M8A","Notes + 50-Q mock"),"cmcis":("CM-CIS","M8 + M8A","Bundle, 100 Qs"),"bank-starter":("BANK STARTER","6 papers","480 Qs"),
 "m9":("CMFAS","M9","Notes + 100-Q mock"),"m9a":("CMFAS","M9A","Notes + 50-Q mock"),"cmlip":("CM-LIP","M9 + M9A","Bundle, 150 Qs"),
 "res5":("CMFAS","RES5","Notes + 150-Q mock"),"hibundle":("CMFAS","HI","Parts 1 + 2 + traps"),"hi1":("CMFAS HI","Part 1","CI, DI, LTC"),"hi2":("CMFAS HI","Part 2","MediShield, IP"),
 "hitraps":("CMFAS HI","Traps","25 trap answers"),"trading":("CMFAS","RES1B + EIP","Bundle, 150 Qs"),"cgi":("SCI CGI","BCP PGI ComGI","Bundle, 150 Qs"),
 "bcp":("SCI","BCP","Notes + 50-Q mock"),"pgi":("SCI","PGI","Notes + 50-Q mock"),"comgi":("SCI","ComGI","Notes + 50-Q mock"),
 "res-cea":("CEA RES","P1 + P2","Bundle, 160 Qs"),"res-p1":("CEA RES","Paper 1","Notes + 80-Q mock"),"res-p2":("CEA RES","Paper 2","Notes + 80-Q mock"),"cams":("ACAMS","CAMS","Notes + 100 Qs"),
 "p6-math-heuristics":("PSLE","P6 Math","27 methods, bar models")}

def book(slug, img, alt, eager=False, cls=""):
    return (f'<div class="book{(" " + cls) if cls else ""}"><img src="{img_for(slug, img)}" alt="{esc(alt)}" width="480" height="480"'
            f'{"" if eager else " loading=\"lazy\""} decoding="async"></div>')

def cards(products):
    out = ['<div class="grid">']
    for name, price, slug, img in products:
        out.append(f'<div class="card">{book(slug, img, name + " cover")}'
                   f'<h3>{esc(name)}</h3><p class="price">{price}</p><a class="btn" href="{g(slug)}">View on Gumroad</a></div>')
    out.append("</div>")
    return "".join(out)

def exam_card(path):
    p = BY[path]; name, price, slug, img = p["products"][0]
    low = min(int(x[1].replace("S$", "")) for x in p["products"])
    sub = LABELS[slug][2]
    return (f'<a class="exam" href="/{path}/"><img src="{img_for(slug, img)}" alt="" width="68" height="68" loading="lazy" decoding="async">'
            f'<div><b>{esc(p["short"])}</b><span>{esc(sub)}</span><em>from S${low}</em></div></a>')

def product_ld(p):
    items = []
    for name, price, slug, img in p["products"]:
        items.append({"@context": "https://schema.org", "@type": "Product", "name": name,
                      "description": p["desc"], "image": BASE + img_for(slug, img),
                      "brand": {"@type": "Brand", "name": "Edge 4 Exams"},
                      "offers": {"@type": "Offer", "price": price.replace("S$", ""), "priceCurrency": "SGD",
                                 "availability": "https://schema.org/InStock", "url": g(slug)}})
    return items

def faq_ld(faqs):
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}

# ---- Plain Markdown copies for AI assistants (same content humans see; never hidden) ----
ABOUT_PRO = ("Edge 4 Exams Singapore (also written Edge4Exams) makes short notes, trap lists and full-length original mock exams "
             "for Singapore licensing exams: CMFAS, SCI, CEA RES and CAMS. Written by a former financial adviser with 9 years in the "
             "Singapore industry. Checkout and instant PDF downloads are on Gumroad: " + STORE + "/ . "
             "Independent study aids, not affiliated with SCI, IBF, MAS, CEA or ACAMS. Every question is original; no leaked or real exam questions.")
ABOUT_PSLE = ("Edge 4 Exams also makes PSLE Math material for Primary 6: problem-solving methods with worked examples and bar models. "
              "Checkout and instant PDF download on Gumroad. Independent study aid, not affiliated with MOE or SEAB. Every question is original.")
ABOUT_MD = ABOUT_PRO  # kept for compatibility

def page_faqs(p):
    return p["faq"] + (COMMON_FAQ if p.get("common_faq", True) else [])

def md_page(p):
    url = f"{BASE}/{p['path']}/"
    L = [f"# {p['h1']}", "", f"Web page: {url}", "", p["intro"], "", "## Packs and prices", ""]
    for name, price, slug, img in p["products"]:
        L.append(f"- **{name}**: {price}, instant PDF. Buy: {g(slug)}")
    if p.get("free"):
        L += ["", f"**{p['free'][0]}** (free, S$0+): {p['free'][2]} Download: {g(p['free'][1])}"]
    L += ["", "## What's in the pack", ""] + [f"- {x}" for x in p["inside"]]
    L += ["", f"## {p.get('topics_label', 'Topics covered')}", ""] + [f"- {x}" for x in p["topics"]]
    L += ["", f"## {p.get('faq_label', p['short'] + ' questions people ask')}", ""]
    for q, a in page_faqs(p):
        L += [f"**{q}**", "", a, ""]
    if p["related"]:
        L += ["## Other exams", ""] + [f"- [{BY[r]['title']}]({BASE}/{r}.md)" for r in p["related"]] + [""]
    L += ["## About", "", ABOUT_PSLE if is_psle(p["path"]) else ABOUT_PRO, ""]
    return "\n".join(L)

def llms_txt():
    L = ["# Edge 4 Exams Singapore", "", "> " + ABOUT_PRO, "",
         "Each page has a plain Markdown copy (same content as the web page).", "", "## Professional licensing exams", ""]
    for p in PAGES:
        if is_psle(p["path"]): continue
        prices = ", ".join(f"{n} {pr}" for n, pr, s, i in p["products"])
        if p.get("free"): prices += f"; {p['free'][0]} free (S$0+), {g(p['free'][1])}"
        L.append(f"- [{p['title']}]({BASE}/{p['path']}.md): {prices}")
    L += ["", f"- Bank Starter Pack (RES5, M8, M8A, M9, M9A, HI): S$99, {g('bank-starter')}", "", "## PSLE (primary school)", "", ABOUT_PSLE, ""]
    for p in PAGES:
        if not is_psle(p["path"]): continue
        prices = ", ".join(f"{n} {pr}" for n, pr, s, i in p["products"])
        if p.get("free"): prices += f"; {p['free'][0]} free (S$0+), {g(p['free'][1])}"
        L.append(f"- [{p['title']}]({BASE}/{p['path']}.md): {prices}")
    L += ["", "## Store", "", f"- [Edge 4 Exams on Gumroad]({STORE}/): all packs, instant PDF download", ""]
    return "\n".join(L)

def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f: f.write(text)

def exam_page(p):
    path = p["path"]; psle = is_psle(path)
    url = f"{BASE}/{path}/"
    faqs = page_faqs(p)
    crumbs = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Edge 4 Exams", "item": BASE + "/"},
        {"@type": "ListItem", "position": 2, "name": p["short"], "item": url}]}
    name, price, slug, img = p["products"][0]
    home_href = "/psle-math/" if psle else "/"
    crumb = '' if psle else f'<p class="crumbs"><a href="{home_href}">Edge 4 Exams</a> / {esc(p["short"])}</p>'
    phero = (f'<section class="phero"><div class="wrap"><div>{crumb}'
             f'<h1>{esc(p["h1"])}</h1><p class="lead">{esc(p["intro"])}</p>'
             f'<div class="buy"><span class="amount">{price}</span><a class="btn btn-gold" href="{g(slug)}">Get the {esc(LABELS[slug][1])} pack</a>'
             f'<small>{esc(name)} · instant PDF download on Gumroad</small></div></div>'
             f'<div>{book(slug, img, name + " cover", eager=True)}</div></div></section>')
    body = [head(p["title"] + " | Edge 4 Exams", p["desc"], url, [ORG, crumbs, faq_ld(faqs)] + product_ld(p),
                 md=f"/{path}.md", og=OG.get(path, "og-home.jpg"), psle=psle, hero=phero)]
    if p.get("free"):
        fname, fslug, fblurb = p["free"]
        body.append(f'<div class="free"><p><strong>{esc(fname)}</strong><br>{esc(fblurb)}</p><a class="btn btn-outline" href="{g(fslug)}">Get the free sample</a></div>')
    if len(p["products"]) > 1:
        body += ['<h2>Choose your pack</h2><p class="sub">Buy the full set or a single part.</p>', cards(p["products"])]
    body.append(f'<div class="cols" id="inside"><div><h2>What\'s in the pack</h2><ul class="ticks">' + "".join(f"<li>{esc(x)}</li>" for x in p["inside"]) + "</ul></div>"
                f'<div><h2>{esc(p.get("topics_label", "Topics covered"))}</h2><ul class="ticks">' + "".join(f"<li>{esc(x)}</li>" for x in p["topics"]) + "</ul></div></div>")
    if psle:
        body.append('<h2>See how a method looks</h2><p class="sub">Every method comes with a bar model drawn to the exact numbers, like this one.</p>'
                    '<div class="bar-fig"><img src="/img/psle-bar-model.svg" alt="Bar model: Ali has 3 units, Ben has 1 unit plus 24 dollars, together 360 dollars. How much does Ben have?" width="520" height="250" loading="lazy"></div>')
    if path in TEASER:
        src, alt, cap = TEASER[path]
        body.append(f'<h2>Look inside</h2><figure class="peek-one"><img src="{src}" alt="{esc(alt)}" width="720" height="720" loading="lazy" decoding="async"><figcaption>{esc(cap)}</figcaption></figure>')
    body.append(f"<h2>{esc(p.get('faq_label', p['short'] + ' questions people ask'))}</h2>" + "".join(f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in faqs))
    if p["related"]:
        body.append('<h2>Other exams</h2><div class="exams" style="margin-top:16px">' + "".join(exam_card(r) for r in p["related"]) + "</div>")
    body.append(f'<p class="note" style="margin-top:36px">Plain-text version of this page: <a href="/{path}.md">{path}.md</a></p>')
    body.append(foot(psle))
    return "\n".join(body)

def home_page():
    home_desc = "Short notes, trap lists and full-length original mock exams for Singapore's CMFAS (M8, M9, RES5, HI and more), SCI, CEA RES and CAMS exams. Instant PDF download."
    site_ld = {"@context": "https://schema.org", "@type": "WebSite", "name": "Edge 4 Exams Singapore", "alternateName": "Edge4Exams", "url": BASE + "/"}
    fan = ('<div class="fan" aria-hidden="true">' + book("res5", "res5-thumb.png", "", eager=True, cls="b1")
           + book("bank-starter", "six-exam-bundle-thumb.png", "", eager=True, cls="b2") + book("m9", "m9-thumb.png", "", eager=True, cls="b3") + "</div>")
    hero = ('<section class="hero"><div class="wrap"><div>'
            '<h1>Pass your licensing exam with less reading</h1>'
            '<p class="lead">Short, exam-focused notes, trap lists and full-length original mock exams for Singapore\'s CMFAS, SCI, CEA and CAMS exams.</p>'
            '<ul class="badges"><li>Original questions only</li><li>Every answer explained</li><li>Instant PDF download</li></ul>'
            f'<div class="cta"><a class="btn btn-gold" href="#exams">Choose your exam</a><a class="btn btn-ghost" href="{STORE}">Visit the store</a></div>'
            f'</div>{fan}</div></section>')
    body = [head("Edge 4 Exams Singapore | CMFAS, SCI, CEA and CAMS Exam Notes and Mock Exams", home_desc, BASE + "/", [ORG, site_ld], og="og-home.jpg", hero=hero),
            '<div class="trust"><div><b>14</b><span>papers covered</span></div><div><b>1,000+</b><span>original practice questions</span></div>'
            '<div><b>9 years</b><span>in the industry, by a former adviser</span></div><div><b>Instant</b><span>PDF on any device</span></div></div>',
            '<h2 id="exams">Choose your exam</h2><p class="sub">Pick your paper to see what\'s inside each pack.</p>']
    for gname, paths in PRO_GROUPS:
        body.append(f'<p class="group">{esc(gname)}</p><div class="exams">' + "".join(exam_card(x) for x in paths) + "</div>")
    body.append('<h2>Look inside</h2><p class="sub">Every pack has a trap list and shortcuts like these.</p><div class="peek">'
                f'<figure><img src="{TEASER["cmfas-hi"][0]}" alt="{esc(TEASER["cmfas-hi"][1])}" width="720" height="720" loading="lazy" decoding="async"><figcaption>Trap lists: the wrong answers that look right, and the truth beside each one.</figcaption></figure>'
                f'<figure><img src="{TEASER["cmfas-m9a"][0]}" alt="{esc(TEASER["cmfas-m9a"][1])}" width="720" height="720" loading="lazy" decoding="async"><figcaption>Shortcuts that stick, like this one from the M9A pack.</figcaption></figure></div>')
    body.append("<h2>Popular packs</h2><p class=\"sub\">Checkout and instant download on Gumroad.</p>")
    body.append(cards([("Bank Starter Pack: RES5, M8, M8A, M9, M9A, HI", "S$99", "bank-starter", "six-exam-bundle-thumb.png"),
                       ("CGI Complete Bundle: BCP + PGI + ComGI", "S$59", "cgi", "cgi-bundle-thumb.png"),
                       ("CEA RES Complete Bundle: Paper 1 + 2", "S$49", "res-cea", "cea-bundle-thumb.png"),
                       ("CM-LIP Bundle: M9 + M9A", "S$45", "cmlip", "cmlip-bundle-thumb-v2.png")]))
    body.append('<h2 id="how">How it works</h2><ol class="steps">'
                '<li><b>Pick your paper</b><span>Each pack covers one exam, or get a bundle for several.</span></li>'
                '<li><b>Download instantly</b><span>Checkout on Gumroad and get the PDF straight away, on your phone, tablet or laptop.</span></li>'
                '<li><b>Study, then test yourself</b><span>Read the shortcut notes and trap list, then sit the full mock exam with every answer explained.</span></li></ol>')
    body.append('<h2>Why Edge 4 Exams</h2><ul class="why"><li>Notes cut down to what examiners actually test</li><li>Trap lists of the wrong answers that look right</li><li>Full-length mock exams in the real format, every answer explained</li><li>Original questions only, never leaked exam content</li></ul>')
    body.append(foot(False))
    return "\n".join(body)

def build():
    if os.path.exists(OUT): shutil.rmtree(OUT)
    if os.path.isdir(STATIC):
        shutil.copytree(STATIC, OUT)
    else:
        os.makedirs(OUT)
    write(OUT + "/style.css", CSS.strip())
    for p in PAGES:
        write(f"{OUT}/{p['path']}/index.html", exam_page(p))
        write(f"{OUT}/{p['path']}.md", md_page(p))
    write(OUT + "/index.html", home_page())
    write(OUT + "/404.html", head("Page not found | Edge 4 Exams", "Page not found.", BASE + "/", []) + '<h1 style="margin-top:40px">Page not found</h1><p><a href="/">Back to Edge 4 Exams</a></p>' + foot(False))
    write(OUT + "/google9b9b5686a32dca00.html", "google-site-verification: google9b9b5686a32dca00.html")
    write(OUT + "/llms.txt", llms_txt())
    write(OUT + "/llms-full.txt", llms_txt() + "\n---\n\n" + "\n\n---\n\n".join(md_page(p) for p in PAGES))
    hdr = ["/*.md", "  Content-Type: text/markdown; charset=utf-8", "", "/llms*.txt", "  Content-Type: text/plain; charset=utf-8", "",
           "/img/*", "  Cache-Control: public, max-age=604800", ""]
    for p in PAGES:
        hdr += [f"/{p['path']}.md", f'  Link: <{BASE}/{p["path"]}/>; rel="canonical"', ""]
    write(OUT + "/_headers", "\n".join(hdr))
    write(OUT + "/robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {BASE}/sitemap.xml\n")
    urls = [BASE + "/"] + [f"{BASE}/{p['path']}/" for p in PAGES]
    write(OUT + "/sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
          "".join(f"  <url><loc>{u}</loc><lastmod>{TODAY}</lastmod></url>\n" for u in urls) + "</urlset>\n")

if __name__ == "__main__":
    build(); print("built", OUT)
