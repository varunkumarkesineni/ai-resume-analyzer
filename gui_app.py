import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import os
import re
import sqlite3
import subprocess
import sys

try:
    import pandas as pd
    import numpy as np
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    import nltk
    from nltk.corpus import stopwords
    from nltk.stem import WordNetLemmatizer
    nltk.download("stopwords", quiet=True)
    nltk.download("wordnet",   quiet=True)
    DEPS_OK = True
except ImportError:
    DEPS_OK = False

try:
    import PyPDF2
    PDF_OK = True
except ImportError:
    PDF_OK = False

try:
    import docx
    DOCX_OK = True
except ImportError:
    DOCX_OK = False

try:
    import anthropic
    CLAUDE_OK = True
except ImportError:
    CLAUDE_OK = False


# ── Colours & fonts ───────────────────────────────────────────────────
BG        = "#0D1117"
PANEL     = "#161B22"
CARD      = "#1C2128"
BORDER    = "#30363D"
TEAL      = "#00B4D8"
MINT      = "#02C39A"
WHITE     = "#E6EDF3"
GREY      = "#8B949E"
RED       = "#F85149"
AMBER     = "#F0883E"
FONT_H    = ("Segoe UI", 13, "bold")
FONT_B    = ("Segoe UI", 11)
FONT_S    = ("Segoe UI", 10)
FONT_MONO = ("Consolas", 10)

JOB_ROLES = [
    {"job_id": "J001", "job_title": "Data Analyst",       "company": "TCS",      "exp_required": 2,
     "jd": "Python Pandas NumPy SQL MySQL data analysis ETL Power BI Tableau dashboard KPI Excel VLOOKUP machine learning scikit-learn"},
    {"job_id": "J002", "job_title": "ML Engineer",         "company": "Infosys",  "exp_required": 3,
     "jd": "Python scikit-learn TensorFlow machine learning NLP TF-IDF cosine similarity NLTK SQL MySQL PostgreSQL Git GitHub AWS SageMaker MLOps"},
    {"job_id": "J003", "job_title": "BI Developer",        "company": "Wipro",    "exp_required": 2,
     "jd": "Power BI Tableau advanced dashboard DAX measures KPI SQL MySQL ETL transformation Excel pivot tables Python Pandas analytics reporting"},
    {"job_id": "J004", "job_title": "Python Developer",    "company": "HCL",      "exp_required": 1,
     "jd": "Python OOP data structures algorithms REST API JSON SQL MySQL Git GitHub agile Django Flask AWS Docker"},
    {"job_id": "J005", "job_title": "Data Science Intern", "company": "Deloitte", "exp_required": 0,
     "jd": "Python Pandas NumPy data analysis machine learning scikit-learn classification regression SQL MySQL Matplotlib Seaborn NLP TF-IDF"},
]

STOP_WORDS  = None
LEMMATIZER  = None

def init_nlp():
    global STOP_WORDS, LEMMATIZER
    if DEPS_OK:
        STOP_WORDS = set(stopwords.words("english"))
        LEMMATIZER = WordNetLemmatizer()

def extract_text_from_file(path):
    ext = os.path.splitext(path)[1].lower()
    if ext == ".pdf" and PDF_OK:
        text = ""
        with open(path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text += page.extract_text() or ""
        return text
    if ext == ".docx" and DOCX_OK:
        doc = docx.Document(path)
        return "\n".join(p.text for p in doc.paragraphs)
    if ext == ".txt":
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    return ""

def clean_text(text):
    if not DEPS_OK or STOP_WORDS is None:
        return str(text).lower()
    text = str(text).lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    tokens = [LEMMATIZER.lemmatize(t) for t in text.split() if t not in STOP_WORDS]
    return " ".join(tokens)

def score_resume(resume_text):
    if not DEPS_OK:
        return []
    jd_texts = [j["jd"] for j in JOB_ROLES]
    all_texts = [clean_text(resume_text)] + [clean_text(jd) for jd in jd_texts]
    vec = TfidfVectorizer(max_features=300, ngram_range=(1, 2), sublinear_tf=True, stop_words="english")
    matrix = vec.fit_transform(all_texts)
    sims   = cosine_similarity(matrix[0:1], matrix[1:])[0]

    results = []
    for i, job in enumerate(JOB_ROLES):
        score = round(sims[i] * 100, 1)
        if score >= 60:   level, color = "Excellent Match", MINT
        elif score >= 40: level, color = "Good Match",      TEAL
        elif score >= 20: level, color = "Partial Match",   AMBER
        else:             level, color = "Low Match",       RED
        results.append({**job, "score": score, "level": level, "color": color})

    results.sort(key=lambda x: x["score"], reverse=True)
    return results

def extract_resume_keywords(text):
    tech = ["python","pandas","numpy","sql","mysql","machine learning","scikit","tensorflow",
            "power bi","tableau","nlp","tfidf","aws","gcp","git","rest api","excel","etl",
            "matplotlib","seaborn","docker","flask","django","java","javascript","react",
            "deep learning","classification","regression","clustering","nlp","bert","oop"]
    found = [k for k in tech if k in text.lower()]
    return found[:20]


class ResumeAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Resume Analyzer — Varun Kumar Kesineni")
        self.root.geometry("1100x760")
        self.root.configure(bg=BG)
        self.root.resizable(True, True)

        self.resume_text  = ""
        self.resume_path  = ""
        self.match_results = []

        init_nlp()
        self._build_ui()

    def _build_ui(self):
        # ── Header ────────────────────────────────────────────────
        hdr = tk.Frame(self.root, bg=PANEL, height=64)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)

        tk.Label(hdr, text="⬡", font=("Segoe UI", 22), bg=PANEL, fg=TEAL).pack(side="left", padx=18, pady=12)
        tk.Label(hdr, text="AI Resume Analyzer", font=("Segoe UI", 16, "bold"), bg=PANEL, fg=WHITE).pack(side="left", pady=12)
        tk.Label(hdr, text="v2.0  |  TF-IDF · NLP · Cosine Similarity",
                 font=FONT_S, bg=PANEL, fg=GREY).pack(side="left", padx=12, pady=12)

        tk.Label(hdr, text="Varun Kumar Kesineni",
                 font=FONT_S, bg=PANEL, fg=TEAL).pack(side="right", padx=20, pady=12)

        # ── Tab bar ───────────────────────────────────────────────
        tab_bar = tk.Frame(self.root, bg=PANEL, height=40)
        tab_bar.pack(fill="x")
        tab_bar.pack_propagate(False)

        self.tabs      = {}
        self.tab_frames= {}
        for name in ["Analyzer", "Rankings", "AI Rewrite", "SQL Queries", "About"]:
            btn = tk.Button(tab_bar, text=name, font=FONT_S, bg=PANEL, fg=GREY,
                            bd=0, padx=16, cursor="hand2",
                            activebackground=PANEL, activeforeground=WHITE,
                            command=lambda n=name: self._switch_tab(n))
            btn.pack(side="left", fill="y")
            self.tabs[name] = btn

        sep = tk.Frame(self.root, bg=BORDER, height=1)
        sep.pack(fill="x")

        # ── Content area ──────────────────────────────────────────
        content = tk.Frame(self.root, bg=BG)
        content.pack(fill="both", expand=True)

        for name in ["Analyzer", "Rankings", "AI Rewrite", "SQL Queries", "About"]:
            f = tk.Frame(content, bg=BG)
            self.tab_frames[name] = f

        self._build_analyzer()
        self._build_rankings()
        self._build_ai_rewrite()
        self._build_sql()
        self._build_about()

        self._switch_tab("Analyzer")

    def _switch_tab(self, name):
        for n, f in self.tab_frames.items():
            f.pack_forget()
        for n, b in self.tabs.items():
            b.config(fg=GREY, bg=PANEL)
        self.tab_frames[name].pack(fill="both", expand=True)
        self.tabs[name].config(fg=WHITE, bg=CARD)

    # ── ANALYZER TAB ──────────────────────────────────────────────
    def _build_analyzer(self):
        f = self.tab_frames["Analyzer"]

        left = tk.Frame(f, bg=BG, width=360)
        left.pack(side="left", fill="y", padx=20, pady=20)
        left.pack_propagate(False)

        right = tk.Frame(f, bg=BG)
        right.pack(side="left", fill="both", expand=True, pady=20, padx=(0, 20))

        # Upload card
        self._card(left, "Upload Resume", self._build_upload_card)
        # Keywords card
        self.kw_frame = self._card(left, "Extracted Keywords", lambda f: setattr(self, "_kw_inner", f))

        # Results card
        res_card = tk.Frame(right, bg=CARD, bd=0)
        res_card.pack(fill="both", expand=True)
        self._border(res_card)

        tk.Label(res_card, text="Job Match Results", font=FONT_H, bg=CARD, fg=WHITE).pack(anchor="w", padx=16, pady=(12, 4))
        tk.Label(res_card, text="Upload your resume to see match scores against 5 live job roles",
                 font=FONT_S, bg=CARD, fg=GREY).pack(anchor="w", padx=16, pady=(0, 10))

        self.results_frame = tk.Frame(res_card, bg=CARD)
        self.results_frame.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        self._show_placeholder()

    def _build_upload_card(self, f):
        drop = tk.Frame(f, bg="#0D1117", relief="flat", bd=1)
        drop.pack(fill="x", pady=(0, 12))

        tk.Label(drop, text="📄", font=("Segoe UI", 28), bg="#0D1117", fg=TEAL).pack(pady=(18, 4))
        tk.Label(drop, text="Drop or browse your resume", font=FONT_S, bg="#0D1117", fg=GREY).pack()
        tk.Label(drop, text="PDF · DOCX · TXT supported", font=("Segoe UI", 9), bg="#0D1117", fg=BORDER).pack(pady=(2, 14))

        tk.Button(drop, text="Browse File", font=FONT_S, bg=TEAL, fg=BG,
                  relief="flat", padx=20, pady=6, cursor="hand2",
                  command=self._browse_file).pack(pady=(0, 16))

        self.file_label = tk.Label(f, text="No file selected", font=FONT_S, bg=CARD, fg=GREY)
        self.file_label.pack(anchor="w")

        self.analyze_btn = tk.Button(f, text="Analyze Resume  →", font=FONT_B,
                                     bg=MINT, fg=BG, relief="flat", padx=16, pady=8,
                                     cursor="hand2", state="disabled",
                                     command=self._run_analysis)
        self.analyze_btn.pack(fill="x", pady=(10, 0))

        self.status_label = tk.Label(f, text="", font=FONT_S, bg=CARD, fg=TEAL)
        self.status_label.pack(pady=(6, 0))

    def _browse_file(self):
        path = filedialog.askopenfilename(
            title="Select Resume",
            filetypes=[("Resume files", "*.pdf *.docx *.txt"), ("All files", "*.*")]
        )
        if not path:
            return
        self.resume_path = path
        fname = os.path.basename(path)
        self.file_label.config(text=f"✓  {fname}", fg=MINT)
        self.analyze_btn.config(state="normal")
        self.status_label.config(text="Ready to analyze", fg=TEAL)

        text = extract_text_from_file(path)
        if not text:
            self.resume_text = self.file_label.cget("text")
        else:
            self.resume_text = text

    def _run_analysis(self):
        if not self.resume_text and not self.resume_path:
            messagebox.showwarning("No Resume", "Please upload a resume first.")
            return
        self.analyze_btn.config(state="disabled", text="Analyzing...")
        self.status_label.config(text="Running TF-IDF matching...", fg=AMBER)
        threading.Thread(target=self._do_analysis, daemon=True).start()

    def _do_analysis(self):
        text = self.resume_text or open(self.resume_path, encoding="utf-8", errors="ignore").read()
        results = score_resume(text)
        keywords = extract_resume_keywords(text)
        self.match_results = results
        self.root.after(0, lambda: self._show_results(results, keywords))

    def _show_results(self, results, keywords):
        for w in self.results_frame.winfo_children():
            w.destroy()

        for r in results:
            row = tk.Frame(self.results_frame, bg=PANEL, pady=0)
            row.pack(fill="x", pady=4)

            # Score circle
            circ = tk.Frame(row, bg=PANEL, width=62, height=62)
            circ.pack(side="left", padx=12, pady=10)
            circ.pack_propagate(False)
            tk.Label(circ, text=f"{r['score']:.0f}", font=("Segoe UI", 16, "bold"),
                     bg=r["color"], fg=BG, width=4, height=2, relief="flat").pack(expand=True, fill="both")

            info = tk.Frame(row, bg=PANEL)
            info.pack(side="left", fill="both", expand=True, pady=10)

            tk.Label(info, text=f"{r['job_title']}  —  {r['company']}",
                     font=FONT_H, bg=PANEL, fg=WHITE).pack(anchor="w")
            tk.Label(info, text=f"{r['level']}  ·  {r['exp_required']}+ yrs exp required",
                     font=FONT_S, bg=PANEL, fg=r["color"]).pack(anchor="w")

            # Bar
            bar_bg = tk.Frame(row, bg=BORDER, height=6, width=200)
            bar_bg.pack(side="right", padx=16, pady=20)
            bar_bg.pack_propagate(False)
            fill_w = max(4, int(200 * r["score"] / 100))
            tk.Frame(bar_bg, bg=r["color"], width=fill_w, height=6).place(x=0, y=0)

        self.analyze_btn.config(state="normal", text="Analyze Resume  →")
        self.status_label.config(text=f"Analysis complete — {len(results)} roles matched", fg=MINT)

        # Update keywords
        if hasattr(self, "_kw_inner"):
            for w in self._kw_inner.winfo_children():
                w.destroy()
            wrap = tk.Frame(self._kw_inner, bg=CARD)
            wrap.pack(fill="x")
            for kw in keywords:
                tag = tk.Label(wrap, text=kw, font=("Segoe UI", 9), bg=PANEL,
                               fg=TEAL, padx=8, pady=3, relief="flat")
                tag.pack(side="left", padx=3, pady=3)

        self.match_results = results
        self._refresh_rankings(results)

    def _show_placeholder(self):
        tk.Label(self.results_frame, text="No results yet\nUpload a resume and click Analyze",
                 font=FONT_B, bg=CARD, fg=GREY, justify="center").pack(expand=True, pady=60)

    # ── RANKINGS TAB ──────────────────────────────────────────────
    def _build_rankings(self):
        f = self.tab_frames["Rankings"]
        tk.Label(f, text="Candidate Rankings", font=("Segoe UI", 15, "bold"),
                 bg=BG, fg=WHITE).pack(anchor="w", padx=20, pady=(20, 4))
        tk.Label(f, text="Sorted by final weighted score across all job roles",
                 font=FONT_S, bg=BG, fg=GREY).pack(anchor="w", padx=20, pady=(0, 12))

        cols = ("Rank", "Job Title", "Company", "Required Exp", "TF-IDF Score", "Match Level")
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Dark.Treeview", background=CARD, foreground=WHITE,
                        fieldbackground=CARD, rowheight=32, font=FONT_S)
        style.configure("Dark.Treeview.Heading", background=PANEL, foreground=TEAL,
                        font=("Segoe UI", 10, "bold"), relief="flat")
        style.map("Dark.Treeview", background=[("selected", TEAL)], foreground=[("selected", BG)])

        frame = tk.Frame(f, bg=BG)
        frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        self.tree = ttk.Treeview(frame, columns=cols, show="headings",
                                 style="Dark.Treeview", height=18)
        widths = [60, 180, 120, 130, 130, 150]
        for col, w in zip(cols, widths):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=w, anchor="center")

        sb = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        self.tree.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")

        tk.Label(f, text="Run analysis in the Analyzer tab to populate rankings",
                 font=FONT_S, bg=BG, fg=GREY).pack(pady=6)

    def _refresh_rankings(self, results):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for i, r in enumerate(results, 1):
            self.tree.insert("", "end", values=(
                i, r["job_title"], r["company"],
                f"{r['exp_required']}+ yrs",
                f"{r['score']}%",
                r["level"],
            ))

    # ── AI REWRITE TAB ────────────────────────────────────────────
    def _build_ai_rewrite(self):
        f = self.tab_frames["AI Rewrite"]

        top = tk.Frame(f, bg=BG)
        top.pack(fill="x", padx=20, pady=(20, 8))

        tk.Label(top, text="AI Resume Rewriter", font=("Segoe UI", 15, "bold"),
                 bg=BG, fg=WHITE).pack(side="left")
        tk.Label(top, text="Powered by Claude", font=FONT_S, bg=BG, fg=TEAL).pack(side="left", padx=12)

        ctrl = tk.Frame(f, bg=BG)
        ctrl.pack(fill="x", padx=20, pady=(0, 12))

        tk.Label(ctrl, text="Target Role:", font=FONT_S, bg=BG, fg=GREY).pack(side="left")
        self.role_var = tk.StringVar(value="Data Analyst")
        roles = ["Data Analyst", "ML Engineer", "BI Developer", "Python Developer", "Data Science Intern"]
        role_menu = ttk.Combobox(ctrl, textvariable=self.role_var, values=roles,
                                 width=22, font=FONT_S, state="readonly")
        role_menu.pack(side="left", padx=(6, 20))

        tk.Label(ctrl, text="API Key:", font=FONT_S, bg=BG, fg=GREY).pack(side="left")
        self.api_entry = tk.Entry(ctrl, font=FONT_S, bg=CARD, fg=WHITE,
                                  insertbackground=WHITE, show="•", width=34, relief="flat")
        self.api_entry.pack(side="left", padx=(6, 12))
        self.api_entry.insert(0, "sk-ant-...")

        self.rewrite_btn = tk.Button(ctrl, text="Generate AI Resume  ✦",
                                     font=FONT_B, bg=TEAL, fg=BG, relief="flat",
                                     padx=16, pady=6, cursor="hand2",
                                     command=self._run_rewrite)
        self.rewrite_btn.pack(side="left")

        panes = tk.Frame(f, bg=BG)
        panes.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # Input pane
        left_pane = tk.Frame(panes, bg=CARD)
        left_pane.pack(side="left", fill="both", expand=True, padx=(0, 8))
        tk.Label(left_pane, text="Your Resume Text", font=FONT_S, bg=CARD, fg=GREY).pack(anchor="w", padx=10, pady=(8, 2))
        self.input_text = scrolledtext.ScrolledText(left_pane, font=FONT_MONO, bg="#0D1117",
                                                     fg=WHITE, insertbackground=WHITE,
                                                     wrap="word", relief="flat", bd=0)
        self.input_text.pack(fill="both", expand=True, padx=6, pady=(0, 8))
        self.input_text.insert("1.0", "Paste your resume text here, or upload a file in the Analyzer tab first...")

        # Output pane
        right_pane = tk.Frame(panes, bg=CARD)
        right_pane.pack(side="left", fill="both", expand=True, padx=(8, 0))

        out_top = tk.Frame(right_pane, bg=CARD)
        out_top.pack(fill="x")
        tk.Label(out_top, text="AI-Rewritten Resume", font=FONT_S, bg=CARD, fg=GREY).pack(side="left", padx=10, pady=(8, 2))
        tk.Button(out_top, text="Copy", font=FONT_S, bg=PANEL, fg=TEAL,
                  relief="flat", cursor="hand2", padx=8,
                  command=self._copy_output).pack(side="right", padx=8, pady=4)

        self.output_text = scrolledtext.ScrolledText(right_pane, font=FONT_MONO, bg="#0D1117",
                                                      fg=WHITE, insertbackground=WHITE,
                                                      wrap="word", relief="flat", bd=0,
                                                      state="disabled")
        self.output_text.pack(fill="both", expand=True, padx=6, pady=(0, 8))

        self.rewrite_status = tk.Label(f, text="", font=FONT_S, bg=BG, fg=TEAL)
        self.rewrite_status.pack(pady=4)

    def _run_rewrite(self):
        resume_text = self.input_text.get("1.0", "end").strip()
        if not resume_text or resume_text.startswith("Paste your resume"):
            if self.resume_text:
                resume_text = self.resume_text
                self.input_text.delete("1.0", "end")
                self.input_text.insert("1.0", resume_text)
            else:
                messagebox.showwarning("No Resume", "Paste your resume text in the left panel or upload a file in Analyzer tab.")
                return

        api_key = self.api_entry.get().strip()
        if not api_key or api_key == "sk-ant-...":
            messagebox.showwarning("API Key Required", "Enter your Anthropic API key.\nGet one free at: console.anthropic.com")
            return

        role = self.role_var.get()
        self.rewrite_btn.config(state="disabled", text="Generating...")
        self.rewrite_status.config(text="Claude is rewriting your resume...", fg=AMBER)

        threading.Thread(target=self._do_rewrite, args=(resume_text, role, api_key), daemon=True).start()

    def _do_rewrite(self, resume_text, role, api_key):
        try:
            import anthropic as ant
            client = ant.Anthropic(api_key=api_key)

            prompt = f"""You are an expert resume writer for the Indian tech industry.
Rewrite the following resume to be highly optimized for a {role} position.

Requirements:
- Professional, industry-standard format
- Strong action verbs and quantified achievements
- ATS-optimized keywords for {role} roles
- Highlight Python, SQL, data analytics, and relevant technical skills
- Keep it to 1 page worth of content
- Format clearly: PROFESSIONAL SUMMARY, TECHNICAL SKILLS, PROJECTS, EDUCATION, CERTIFICATIONS
- Make bullet points impactful with numbers (%, X times faster, N+ records, etc.)
- Tailor specifically for Indian tech companies (TCS, Infosys, Wipro, HCL, Deloitte)

Original Resume:
{resume_text}

Return ONLY the rewritten resume. No commentary or explanations."""

            message = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1500,
                messages=[{"role": "user", "content": prompt}]
            )
            result = message.content[0].text
            self.root.after(0, lambda: self._show_rewrite(result))
        except Exception as e:
            self.root.after(0, lambda: self._rewrite_error(str(e)))

    def _show_rewrite(self, text):
        self.output_text.config(state="normal")
        self.output_text.delete("1.0", "end")
        self.output_text.insert("1.0", text)
        self.output_text.config(state="disabled")
        self.rewrite_btn.config(state="normal", text="Generate AI Resume  ✦")
        self.rewrite_status.config(text="Resume rewritten successfully!", fg=MINT)

    def _rewrite_error(self, err):
        self.rewrite_btn.config(state="normal", text="Generate AI Resume  ✦")
        self.rewrite_status.config(text=f"Error: {err[:80]}", fg=RED)

    def _copy_output(self):
        text = self.output_text.get("1.0", "end").strip()
        if text:
            self.root.clipboard_clear()
            self.root.clipboard_append(text)
            self.rewrite_status.config(text="Copied to clipboard!", fg=MINT)

    # ── SQL QUERIES TAB ───────────────────────────────────────────
    def _build_sql(self):
        f = self.tab_frames["SQL Queries"]
        tk.Label(f, text="SQL Query Runner", font=("Segoe UI", 15, "bold"),
                 bg=BG, fg=WHITE).pack(anchor="w", padx=20, pady=(20, 4))
        tk.Label(f, text="Run queries against the resume_analyzer.db SQLite database",
                 font=FONT_S, bg=BG, fg=GREY).pack(anchor="w", padx=20, pady=(0, 10))

        ctrl = tk.Frame(f, bg=BG)
        ctrl.pack(fill="x", padx=20, pady=(0, 8))

        presets = {
            "Top 5 per Job":        "SELECT j.job_title, c.candidate_name, m.match_score, m.final_score, m.final_rank FROM match_results m JOIN candidates c ON m.resume_id=c.resume_id JOIN job_roles j ON m.job_id=j.job_id WHERE m.final_rank<=5 ORDER BY j.job_title, m.final_rank;",
            "Match Distribution":   "SELECT match_level, COUNT(*) AS count, ROUND(AVG(final_score),1) AS avg_score FROM match_results GROUP BY match_level ORDER BY avg_score DESC;",
            "Skill Gap":            "SELECT skill, SUM(has_skill) AS have, SUM(gap) AS missing, ROUND(SUM(gap)*100.0/COUNT(*),1) AS gap_pct FROM skill_gap GROUP BY skill ORDER BY gap_pct DESC;",
            "Shortlisted":          "SELECT c.candidate_name, j.job_title, m.final_score FROM match_results m JOIN candidates c ON m.resume_id=c.resume_id JOIN job_roles j ON m.job_id=j.job_id WHERE m.is_shortlisted=1 ORDER BY m.final_score DESC;",
            "Experience Analysis":  "SELECT CASE WHEN c.experience_years=0 THEN 'Fresher' WHEN c.experience_years<=2 THEN '1-2 yrs' WHEN c.experience_years<=4 THEN '3-4 yrs' ELSE '5+ yrs' END AS exp_group, COUNT(DISTINCT c.resume_id) AS candidates, ROUND(AVG(m.final_score),1) AS avg_score FROM match_results m JOIN candidates c ON m.resume_id=c.resume_id GROUP BY exp_group ORDER BY avg_score DESC;",
        }

        tk.Label(ctrl, text="Preset:", font=FONT_S, bg=BG, fg=GREY).pack(side="left")
        self.preset_var = tk.StringVar()
        preset_menu = ttk.Combobox(ctrl, textvariable=self.preset_var,
                                   values=list(presets.keys()), width=22,
                                   font=FONT_S, state="readonly")
        preset_menu.pack(side="left", padx=(6, 12))
        preset_menu.bind("<<ComboboxSelected>>",
                         lambda e: self.sql_input.delete("1.0", "end") or
                                   self.sql_input.insert("1.0", presets[self.preset_var.get()]))

        tk.Button(ctrl, text="Run Query  ▶", font=FONT_B, bg=TEAL, fg=BG,
                  relief="flat", padx=14, pady=5, cursor="hand2",
                  command=self._run_sql).pack(side="left")

        self.sql_status = tk.Label(ctrl, text="", font=FONT_S, bg=BG, fg=TEAL)
        self.sql_status.pack(side="left", padx=12)

        panes = tk.Frame(f, bg=BG)
        panes.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        sql_in = tk.Frame(panes, bg=CARD)
        sql_in.pack(fill="x", pady=(0, 8))
        tk.Label(sql_in, text="SQL Query", font=FONT_S, bg=CARD, fg=GREY).pack(anchor="w", padx=10, pady=(8, 2))
        self.sql_input = scrolledtext.ScrolledText(sql_in, font=FONT_MONO, height=5,
                                                    bg="#0D1117", fg=WHITE,
                                                    insertbackground=WHITE, wrap="none",
                                                    relief="flat", bd=0)
        self.sql_input.pack(fill="x", padx=6, pady=(0, 8))
        self.sql_input.insert("1.0", "SELECT * FROM candidates LIMIT 10;")

        sql_out = tk.Frame(panes, bg=CARD)
        sql_out.pack(fill="both", expand=True)
        tk.Label(sql_out, text="Results", font=FONT_S, bg=CARD, fg=GREY).pack(anchor="w", padx=10, pady=(8, 2))
        self.sql_output = scrolledtext.ScrolledText(sql_out, font=FONT_MONO,
                                                     bg="#0D1117", fg=WHITE,
                                                     insertbackground=WHITE,
                                                     wrap="none", relief="flat", bd=0,
                                                     state="disabled")
        self.sql_output.pack(fill="both", expand=True, padx=6, pady=(0, 8))

    def _run_sql(self):
        query = self.sql_input.get("1.0", "end").strip()
        if not query:
            return
        db = "outputs/resume_analyzer.db"
        if not os.path.exists(db):
            self.sql_status.config(text="DB not found. Run pipeline first.", fg=RED)
            return
        try:
            conn = sqlite3.connect(db)
            import pandas as pd
            df = pd.read_sql_query(query, conn)
            conn.close()
            result = df.to_string(index=False)
            self.sql_output.config(state="normal")
            self.sql_output.delete("1.0", "end")
            self.sql_output.insert("1.0", result)
            self.sql_output.config(state="disabled")
            self.sql_status.config(text=f"{len(df)} rows returned", fg=MINT)
        except Exception as e:
            self.sql_output.config(state="normal")
            self.sql_output.delete("1.0", "end")
            self.sql_output.insert("1.0", f"Error: {e}")
            self.sql_output.config(state="disabled")
            self.sql_status.config(text="Query failed", fg=RED)

    # ── ABOUT TAB ─────────────────────────────────────────────────
    def _build_about(self):
        f = self.tab_frames["About"]
        c = tk.Frame(f, bg=BG)
        c.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(c, text="⬡", font=("Segoe UI", 48), bg=BG, fg=TEAL).pack()
        tk.Label(c, text="AI Resume Analyzer", font=("Segoe UI", 22, "bold"), bg=BG, fg=WHITE).pack(pady=(4, 2))
        tk.Label(c, text="v2.0  |  TF-IDF · NLP · Cosine Similarity · Claude AI", font=FONT_S, bg=BG, fg=GREY).pack()

        tk.Frame(c, bg=BORDER, height=1, width=400).pack(pady=20)

        info = [
            ("Developer",   "Varun Kumar Kesineni"),
            ("College",     "CMR College of Engineering & Technology"),
            ("Degree",      "B.Tech Computer Science  (2024–2028)"),
            ("Email",       "kesinenivarunkumar715@gmail.com"),
            ("GitHub",      "github.com/varunkumarkesineni"),
            ("LinkedIn",    "linkedin.com/in/varun-kumar-kesineni-80a427326"),
        ]
        for label, value in info:
            row = tk.Frame(c, bg=BG)
            row.pack(fill="x", pady=3)
            tk.Label(row, text=f"{label}:", font=FONT_S, bg=BG, fg=GREY, width=12, anchor="e").pack(side="left")
            tk.Label(row, text=value, font=FONT_S, bg=BG, fg=WHITE).pack(side="left", padx=8)

        tk.Frame(c, bg=BORDER, height=1, width=400).pack(pady=20)
        tk.Label(c, text="Tech Stack: Python · scikit-learn · NLTK · TF-IDF · SQLite · Tkinter · Claude API",
                 font=FONT_S, bg=BG, fg=TEAL).pack()

    # ── Helpers ───────────────────────────────────────────────────
    def _card(self, parent, title, build_fn):
        frame = tk.Frame(parent, bg=CARD, bd=0)
        frame.pack(fill="x", pady=(0, 12))
        self._border(frame)
        tk.Label(frame, text=title, font=FONT_H, bg=CARD, fg=WHITE).pack(anchor="w", padx=14, pady=(10, 6))
        inner = tk.Frame(frame, bg=CARD)
        inner.pack(fill="both", expand=True, padx=12, pady=(0, 12))
        build_fn(inner)
        return frame

    def _border(self, widget):
        widget.config(highlightthickness=1, highlightbackground=BORDER)


if __name__ == "__main__":
    if not DEPS_OK:
        print("Missing dependencies. Run: pip install -r requirements.txt")
        sys.exit(1)
    root = tk.Tk()
    app  = ResumeAnalyzerApp(root)
    root.mainloop()
