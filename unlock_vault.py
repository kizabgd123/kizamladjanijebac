#!/usr/bin/env python3
"""
Unlock Vault CLI - Sigurnosna zaštita za API ključeve i model konfiguraciju.
Zahteva korisničku šifru pre nego što dozvoli pregled ili izmenu ključeva.
"""

import os
import sys
import hashlib
import getpass
from pathlib import Path

HASH_FILE = Path(os.path.expanduser("~/.key_vault.hash"))
ENV_FILE = Path("/home/kizamladjanijebac/Desktop/judge-guard-core-master/.env")
ROOT_ENV_FILE = Path("/home/kizamladjanijebac/.env")

def hash_password(pwd: str) -> str:
    return hashlib.sha256(pwd.encode('utf-8')).hexdigest()

def is_vault_initialized() -> bool:
    return HASH_FILE.exists()

def set_password():
    print("\n🔐 Postavljanje nove master šifre za Key Vault...")
    pwd1 = getpass.getpass("Unesite željenu master šifru: ")
    pwd2 = getpass.getpass("Potvrdite master šifru: ")
    if pwd1 != pwd2:
        print("❌ Šifre se ne poklapaju! Otkazano.")
        sys.exit(1)
    if len(pwd1) < 4:
        print("❌ Šifra mora imati najmanje 4 karaktera!")
        sys.exit(1)
    
    HASH_FILE.write_text(hash_password(pwd1), encoding="utf-8")
    os.chmod(HASH_FILE, 0o600)
    print("✅ Master šifra je uspešno postavljena i zaštićena u ~/.key_vault.hash!")

def verify_password() -> bool:
    if not is_vault_initialized():
        print("⚠️ Vault šifra još uvek nije postavljena.")
        set_password()
        return True

    saved_hash = HASH_FILE.read_text(encoding="utf-8").strip()
    input_pwd = getpass.getpass("🔑 Unesite vašu master šifru za otključavanje: ")
    if hash_password(input_pwd) == saved_hash:
        print("✅ Šifra je ispravna! Pristup odobren.")
        return True
    else:
        print("❌ POGREŠNA ŠIFRA! Pristup odbijen.")
        return False

def update_keys():
    print("\n🔑 Ažuriranje Gemini API ključeva:")
    new_keys = input("Unesite nove Gemini API ključeve (odvojene zarezom): ").strip()
    if not new_keys:
        print("Otkazano.")
        return

    # Update Desktop .env
    if ENV_FILE.exists():
        content = ENV_FILE.read_text(encoding="utf-8")
        lines = []
        key_found = False
        for line in content.splitlines():
            if line.startswith("GEMINI_API_KEY=") or line.startswith("GEMINI_API_KEYS="):
                lines.append(f"GEMINI_API_KEY={new_keys}")
                lines.append(f"GEMINI_API_KEYS={new_keys}")
                key_found = True
            else:
                lines.append(line)
        if not key_found:
            lines.append(f"GEMINI_API_KEYS={new_keys}")
        ENV_FILE.write_text("\n".join(lines) + "\n", encoding="utf-8")

    # Update root .env
    if ROOT_ENV_FILE.exists():
        content = ROOT_ENV_FILE.read_text(encoding="utf-8")
        lines = []
        for line in content.splitlines():
            if line.startswith("GEMINI_API_KEY=") or line.startswith("GEMINI_API_KEYS="):
                lines.append(f"GEMINI_API_KEY={new_keys}")
                lines.append(f"GEMINI_API_KEYS={new_keys}")
            else:
                lines.append(line)
        ROOT_ENV_FILE.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print("✅ Ključevi su bezbedno ažurirani u .env fajlovima!")

def main():
    print("=" * 55)
    print("🔒 ANTIGRAVITY KEY VAULT & SECURITY MANAGER")
    print("=" * 55)

    if len(sys.argv) > 1 and sys.argv[1] == "init":
        set_password()
        return

    if not verify_password():
        sys.exit(1)

    print("\nIzaberite opciju:")
    print("  1. Ažuriraj Gemini API ključeve")
    print("  2. Promeni master šifru")
    print("  3. Izlaz")
    choice = input("\nIzbor [1/2/3]: ").strip()

    if choice == "1":
        update_keys()
    elif choice == "2":
        set_password()
    else:
        print("Izlaz.")

if __name__ == "__main__":
    main()
