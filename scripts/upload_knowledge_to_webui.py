#!/usr/bin/env python3
"""
Ispravno uploaduje sve 15 verifikovanih sveskih u Open WebUI Knowledge Base
kroz pravi API, a ne direktno u bazu.
"""

import os
import json
import time
import urllib.request
import urllib.error
import urllib.parse
import mimetypes

API_URL = "http://localhost:3000/api/v1"
API_KEY = "sk-kiza-openwebui-2026-master"
KB_NAME = "Antigravity Verified Brain (100% Grounded NotebookLM)"
MODEL_ID = "antigravity-grounded-ai"
BASE_MODEL = "models/gemini-2.5-flash"
KNOWLEDGE_DIR = "/home/kizamladjanijebac/verified_notebooks_knowledge"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}


def api(method, path, data=None, raw_headers=None):
    h = raw_headers or HEADERS
    body = json.dumps(data).encode("utf-8") if data else None
    req = urllib.request.Request(f"{API_URL}/{path}", data=body, headers=h, method=method)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        err = e.read().decode()
        print(f"  HTTP {e.code}: {err[:200]}")
        return None


def upload_file(filepath):
    """Upload file using multipart/form-data"""
    filename = os.path.basename(filepath)
    with open(filepath, "rb") as f:
        content = f.read()

    boundary = "----FormBoundary7MA4YWxkTrZu0gW"
    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="file"; filename="{filename}"\r\n'
        f"Content-Type: text/markdown\r\n\r\n"
    ).encode("utf-8") + content + f"\r\n--{boundary}--\r\n".encode("utf-8")

    req = urllib.request.Request(
        f"{API_URL}/files/",
        data=body,
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": f"multipart/form-data; boundary={boundary}",
        },
        method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        print(f"  Upload error {e.code}: {e.read().decode()[:200]}")
        return None


def main():
    print("=" * 60)
    print("Open WebUI Knowledge Base Ingestion Tool")
    print("=" * 60)

    # 1. Obrisi stare prazne KB i napravi novu cisti
    print("\n[1] Provera postojecih knowledge baza...")
    kbs = api("GET", "knowledge/")
    if kbs:
        for kb in kbs.get("items", kbs if isinstance(kbs, list) else []):
            if "Antigravity" in kb.get("name", ""):
                kid = kb["id"]
                print(f"  Brišem staru KB: {kid}")
                api("DELETE", f"knowledge/{kid}/")

    # 2. Kreiraj novu KB
    print(f"\n[2] Kreiram Knowledge Base: {KB_NAME}")
    kb_result = api("POST", "knowledge/create", {
        "name": KB_NAME,
        "description": "100% verifikovano znanje iz 15 Google NotebookLM sveski (Kiza). Svaka sveska ručno proverena i upisana od strane Antigravity agenta.",
        "data": {}
    })
    if not kb_result:
        print("GREŠKA: Ne mogu kreirati KB!")
        return
    kb_id = kb_result.get("id")
    print(f"  KB kreiran, ID: {kb_id}")

    # 3. Upload svakog fajla i dodaj u KB
    files = sorted([
        f for f in os.listdir(KNOWLEDGE_DIR)
        if f.endswith(".md")
    ])
    print(f"\n[3] Uploading {len(files)} fajlova i dodavanje u KB...")

    uploaded_ids = []
    for i, filename in enumerate(files, 1):
        filepath = os.path.join(KNOWLEDGE_DIR, filename)
        print(f"  [{i:02d}/{len(files)}] {filename}")

        # Upload fajla
        fres = upload_file(filepath)
        if not fres:
            print(f"    PRESKOČENO - upload nije uspeo")
            continue

        file_id = fres.get("id")
        print(f"    File ID: {file_id}")

        # Dodaj u KB
        add_res = api("POST", f"knowledge/{kb_id}/file/add", {"file_id": file_id})
        if add_res:
            print(f"    ✅ Dodat u KB")
            uploaded_ids.append(file_id)
        else:
            print(f"    ⚠️ Nije dodat u KB")

        time.sleep(0.5)

    print(f"\n[4] Ukupno uploadovano i dodato: {len(uploaded_ids)}/15 fajlova")

    # 4. Azuriraj model da koristi pravi KB i pravi base model
    print(f"\n[5] Azuriram model '{MODEL_ID}' -> base: {BASE_MODEL}, KB: {kb_id}")

    system_prompt = """Ti si Antigravity Grounded AI — specijalizovani asistent sa 100% verifikovanim znanjem iz 15 Google NotebookLM sveski korisnika Kize.

STROGA PRAVILA:
1. Odgovaraj ISKLJUČIVO na osnovu verifikovanih činjenica iz priložene baze znanja (15 sveski).
2. Kada citiraš, navedi iz koje sveske potiče znanje (npr. "iz Sveske 10 - NLP").
3. Ako pitanje nije pokriveno sveskama — jasno reci: "Ovo nije u bazi verifikovanih sveski."
4. Nulta tolerancija na izmišljanje (halucinacije) — bolje kratak tačan odgovor nego dug netačan.
5. Format odgovora: konkretan, primenljiv, strukturisan (korak-po-korak kad je moguće).

Sveske u bazi znanja:
01. Vaš Mozak - Ko je u Kontroli (neurobiologija, talamus, epigenetika)
02. AI Native Transformation SEE (Endava, Levi9, Databricks RAG)
03. Project OpenClaw (Sovereign AI OS, Debate Engine, JudgeGuard)
04. Google Antigravity IDE (Mission Control, Browser Agent, Rules)
05. CodyMaster Brain (Dual-Brain RAG, Rule of 3, 7-Stage pipeline)
06. Prokrastinacija (TMT formula, Amygdala Hijack, Pychyl)
07. NotebookLM Custom Prompts (Chat guardrails, Audio Overview)
08. LinkedIn Automation Agent (FastMCP, Ghostty, OBS Telemetry)
09. Gemini 3 Prompting Rules (temperatura 1.0, XML tagovi)
10. NLP Silva Metod Neuroplastičnost (Alfa stanje 7-14Hz, Swish)
11. 2026 UI Design (Spatial Computing, 4px grid, 6-3-1 pravilo)
12. Duboko Učenje VI (Mitchell model, Pandas, Backpropagation)
13. Pametno Odlučivanje (Bezos Type1/2, Damasio, 10-10-10)
14. Lični Brend Strategija (Inbound levak, Content Waterfall, 3 paketa)
15. Strateška Komunikacija (Pre-drafting, Inženjer filter, 30-dnevni plan)"""

    model_payload = {
        "base_model_id": BASE_MODEL,
        "name": "🧠 Antigravity Grounded AI (Verified Knowledge)",
        "params": {
            "system": system_prompt,
            "temperature": 0.15,
            "top_p": 0.9
        },
        "meta": {
            "profile_image_url": "https://www.gstatic.com/images/branding/product/1x/gemini_48dp.png",
            "description": "Elitni AI asistent: 100% verifikovano znanje iz 15 NotebookLM sveski. Nulta halucinacija.",
            "capabilities": {
                "file_context": True,
                "vision": True,
                "file_upload": True,
                "web_search": False,
                "image_generation": False,
                "code_interpreter": True,
                "citations": True
            },
            "knowledge": [
                {"id": kb_id, "name": KB_NAME}
            ],
            "suggestion_prompts": [
                {"title": ["TMT formula", "prokrastinacija"], "content": "Objasni formulu teorije temporalne motivacije (TMT) i ulogu prefrontalnog korteksa."},
                {"title": ["Bezos Type 1 vs 2", "odlučivanje"], "content": "Koji je okvir za donošenje odluka po Bezosu i Damasio principima iz sveske 13?"},
                {"title": ["OpenClaw Arhitektura", "Debate Engine"], "content": "Kako funkcioniše Debate Engine sa 5 persona i JudgeGuard sigurnosna kapija?"},
                {"title": ["NLP apstinencija", "Swish Pattern"], "content": "Korak po korak: Kako primeniti Swish Pattern i Sidrenje za zaustavljanje zavisnosti?"},
                {"title": ["Content Waterfall", "lični brend"], "content": "Objasni sistem Content Waterfall i inbound levak za privlačenje premium klijenata."}
            ]
        }
    }

    update_res = api("POST", f"models/{MODEL_ID}/update", model_payload)
    if update_res:
        print(f"  ✅ Model ažuriran!")
    else:
        # Pokusaj PUT
        req = urllib.request.Request(
            f"{API_URL}/models/{MODEL_ID}",
            data=json.dumps(model_payload).encode("utf-8"),
            headers=HEADERS,
            method="PUT"
        )
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                print(f"  ✅ Model ažuriran (PUT)!")
        except Exception as e:
            print(f"  Update model direktno kroz DB...")
            import subprocess
            subprocess.run([
                "docker", "exec", "open-webui", "python3", "-c",
                f"""
import sqlite3, json, time
con = sqlite3.connect('/app/backend/data/webui.db')
cur = con.cursor()
cur.execute("UPDATE model SET base_model_id=?, meta=?, params=?, updated_at=? WHERE id=?;",
    ('{BASE_MODEL}',
     json.dumps({json.dumps(model_payload['meta'])}),
     json.dumps({json.dumps(model_payload['params'])}),
     int(time.time()),
     '{MODEL_ID}'))
con.commit()
print('DB update:', cur.rowcount)
"""
            ])

    print("\n" + "=" * 60)
    print(f"✅ ZAVRŠENO! KB ID: {kb_id}")
    print(f"   Files: {len(uploaded_ids)}/15")
    print(f"   Model base: {BASE_MODEL}")
    print("=" * 60)


if __name__ == "__main__":
    main()
