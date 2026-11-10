#!/usr/bin/env python3
"""Generise MCP konfiguraciju za Hermes i Antigravity iz configs/connections.json.
Podrazumevano dry-run. --write pravi backup (.bak) i upisuje.
NISAM testirao protiv zivih instalacija; pokreni prvo bez --write."""
import argparse, json, os, re, shutil, sys
from pathlib import Path

BUNDLE = Path(__file__).resolve().parent.parent
PATH_VARS = {"BUNDLE_DIR": str(BUNDLE), "PROJECTS_DIR": os.environ.get("PROJECTS_DIR", str(Path.home() / "projects"))}
VAR = re.compile(r"\$\{([A-Za-z_][A-Za-z0-9_]*)\}")


def expand_paths(s, expand_secrets):
    def sub(m):
        k = m.group(1)
        if k in PATH_VARS:
            return PATH_VARS[k]
        if expand_secrets:
            if k not in os.environ:
                print(f"⚠️  [sync_mcp] Promenljiva ${{{k}}} nije definisana u okruženju, ostavljam placeholder.")
                return f"${{{k}}}"
            return os.environ[k]
        return m.group(0)
    return VAR.sub(sub, s) if isinstance(s, str) else s


def walk(o, f):
    if isinstance(o, dict):
        return {k: walk(v, f) for k, v in o.items()}
    if isinstance(o, list):
        return [walk(v, f) for v in o]
    return f(o)


def build(servers, target):
    out = {}
    for name, s in servers.items():
        s = walk(s, lambda x: expand_paths(x, expand_secrets=(target == "antigravity")))
        if s["type"] == "stdio":
            e = {"command": s["command"], "args": s.get("args", [])}
            if s.get("env"):
                e["env"] = s["env"]
        else:
            if target == "antigravity":
                e = {"serverUrl": s["url"], "disabled": False}
            else:
                e = {"url": s["url"]}
            if s.get("headers"):
                e["headers"] = s["headers"]
        out[name] = e
    return out


def backup(p):
    if p.exists():
        shutil.copy2(p, p.with_suffix(p.suffix + ".bak"))


def do_antigravity(servers, path, write):
    data = build(servers, "antigravity")
    p = Path(path).expanduser()
    cur = json.loads(p.read_text()) if p.exists() else {}
    cur.setdefault("mcpServers", {}).update(data)
    txt = json.dumps(cur, indent=2)
    shown = re.sub(r'("Authorization":\s*")[^"]+', r'\1***', txt)
    print(f"--- Antigravity -> {p}\n{shown}\n")
    if write:
        p.parent.mkdir(parents=True, exist_ok=True)
        backup(p)
        p.write_text(txt)
        os.chmod(p, 0o600)


def do_hermes(servers, path, write):
    try:
        import yaml
    except ImportError:
        sys.exit("Za Hermes target treba PyYAML: pip install pyyaml (ili rucno iskopiraj configs/hermes_config.example.yaml)")
    data = build(servers, "hermes")
    p = Path(path).expanduser()
    cur = yaml.safe_load(p.read_text()) if p.exists() else {}
    cur = cur or {}
    cur.setdefault("mcp_servers", {}).update(data)
    txt = yaml.safe_dump(cur, sort_keys=False)
    print(f"--- Hermes -> {p}\n{txt}\n(UPOZORENJE: --write ponovo serijalizuje YAML; komentari u configu se gube, backup se pravi)\n")
    if write:
        backup(p)
        p.write_text(txt)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", choices=["hermes", "antigravity", "both"], default="both")
    ap.add_argument("--source", default=str(BUNDLE / "configs" / "connections.json"))
    ap.add_argument("--hermes-path", default="~/.hermes/config.yaml")
    ap.add_argument("--antigravity-path", default="~/.gemini/antigravity/mcp_config.json")
    ap.add_argument("--write", action="store_true")
    a = ap.parse_args()
    servers = json.loads(Path(a.source).read_text())["servers"]
    if a.target in ("antigravity", "both"):
        do_antigravity(servers, a.antigravity_path, a.write)
    if a.target in ("hermes", "both"):
        do_hermes(servers, a.hermes_path, a.write)
    print("Upisano." if a.write else "Dry-run. Dodaj --write za upis.")


if __name__ == "__main__":
    main()
