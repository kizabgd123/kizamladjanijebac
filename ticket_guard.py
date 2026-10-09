#!/usr/bin/env bash
""":"
# Python wrapper for dual execution
exec python3 "$0" "$@"
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from typing import Dict, Any, List

TICKETS_DIR = Path("/home/kizamladjanijebac/tickets")

class TicketGuard:
    """
    Deterministic Ticket Verification Gate.
    Verifies that a ticket is 100% completed according to its verification suite.
    If ANY condition fails, execution HALTS with exit code 1.
    """

    def __init__(self, tickets_dir: Path = TICKETS_DIR):
        self.tickets_dir = tickets_dir
        self.tickets_dir.mkdir(parents=True, exist_ok=True)

    def load_ticket(self, ticket_id: str) -> Dict[str, Any]:
        ticket_file = self.tickets_dir / f"{ticket_id}.json"
        if not ticket_file.exists():
            print(f"❌ Tiket nije pronađen: {ticket_file}")
            sys.exit(1)
        with open(ticket_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def save_ticket(self, ticket_id: str, data: Dict[str, Any]):
        ticket_file = self.tickets_dir / f"{ticket_id}.json"
        with open(ticket_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def verify_ticket(self, ticket_id: str) -> bool:
        ticket = self.load_ticket(ticket_id)
        suite = ticket.get("verification_suite", [])
        
        print("\n" + "=" * 60)
        print(f"🎫 TIKET VERIFIKACIJA: [{ticket.get('id')}] {ticket.get('title')}")
        print("=" * 60)
        print(f"Opis: {ticket.get('description', '')}\n")

        all_passed = True
        results = []

        for idx, check in enumerate(suite, 1):
            check_name = check.get("name", f"Provera #{idx}")
            check_type = check.get("type", "command")
            print(f"  [{idx}/{len(suite)}] Proveravam: {check_name} ...", end=" ")

            passed = False
            error_msg = ""

            if check_type == "file_exists":
                target_path = Path(check.get("path", ""))
                if target_path.exists():
                    passed = True
                else:
                    error_msg = f"Fajl ne postoji: {target_path}"

            elif check_type == "file_contains":
                target_path = Path(check.get("path", ""))
                needle = check.get("contains", "")
                if not target_path.exists():
                    error_msg = f"Fajl ne postoji: {target_path}"
                else:
                    try:
                        content = target_path.read_text(encoding="utf-8", errors="ignore")
                        if needle in content:
                            passed = True
                        else:
                            error_msg = f"Fajl {target_path} ne sadrži traženi string: '{needle}'"
                    except Exception as e:
                        error_msg = str(e)

            elif check_type == "command":
                cmd = check.get("command", "")
                expected_code = check.get("expected_exit_code", 0)
                res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                if res.returncode == expected_code:
                    passed = True
                else:
                    error_msg = (
                        f"Komanda nije uspela (kod {res.returncode}, očekivan {expected_code}).\n"
                        f"      Izlaz: {res.stdout.strip()}\n"
                        f"      Greška: {res.stderr.strip()}"
                    )
            else:
                error_msg = f"Nepoznat tip provere: {check_type}"

            if passed:
                print("✅ USPEŠNO")
                results.append({"name": check_name, "status": "PASSED"})
            else:
                print("❌ NEUSPEŠNO")
                print(f"      Razlog: {error_msg}")
                results.append({"name": check_name, "status": "FAILED", "error": error_msg})
                all_passed = False

        print("-" * 60)
        if all_passed:
            ticket["status"] = "VERIFIED_COMPLETE"
            ticket["verification_results"] = results
            self.save_ticket(ticket_id, ticket)
            print(f"🎉 TIKET [{ticket_id}] JE 100% ZAVRŠEN I VERIFIKOVAN!")
            print("=" * 60 + "\n")
            return True
        else:
            ticket["status"] = "VERIFICATION_FAILED"
            ticket["verification_results"] = results
            self.save_ticket(ticket_id, ticket)
            print(f"🛑 BLOKADA: Tiket [{ticket_id}] NIJE u potpunosti završen!")
            print("Rad se NE MOŽE nastaviti dok se sve stavke ne ispune!")
            print("=" * 60 + "\n")
            return False

def main():
    if len(sys.argv) < 2:
        print("Upotreba:")
        print("  python3 ticket_guard.py verify <TICKET-ID>")
        print("  python3 ticket_guard.py list")
        sys.exit(1)

    cmd = sys.argv[1]
    guard = TicketGuard()

    if cmd == "verify":
        if len(sys.argv) < 3:
            print("Navedite ID tiketa: python3 ticket_guard.py verify <TICKET-ID>")
            sys.exit(1)
        ticket_id = sys.argv[2]
        if not guard.verify_ticket(ticket_id):
            sys.exit(1)
        sys.exit(0)

    elif cmd == "list":
        tickets = list(TICKETS_DIR.glob("*.json"))
        if not tickets:
            print("Nema pronađenih tiketa u direktorijumu 'tickets/'.")
            return
        print(f"\n📋 Spisak Tiketa ({len(tickets)}):")
        for t_file in tickets:
            try:
                with open(t_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    status_icon = "✅" if data.get("status") == "VERIFIED_COMPLETE" else "🟡"
                    print(f"  {status_icon} [{data.get('id')}] {data.get('title')} -> {data.get('status')}")
            except Exception:
                print(f"  ❓ {t_file.name}")
        print()

    else:
        print(f"Nepoznata komanda: {cmd}")
        sys.exit(1)

if __name__ == "__main__":
    main()
