import os
import time
from typing import Optional, Dict, List
import logging
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

ACTIVE_MODELS: List[str] = [
    "gemini-3.8-flash",
    "gemini-flash-latest",
    "gemini-3.5-flash",
    "gemini-3.5-flash-lite",
    "gemini-3.6-flash"
]

class VaultLockError(RuntimeError):
    """Raised when API keys are exhausted or locked, requiring user password."""
    pass

class GeminiClient:
    """
    Client for interacting with Google's modern Gemini models via google-genai.
    Includes key rotation and password-protected vault security.
    """
    VAULT_HASH_PATH = os.path.expanduser("~/.key_vault.hash")

    def __init__(self, model_name: Optional[str] = None, api_keys: Optional[str] = None):
        selected_model = model_name or os.getenv("GEMINI_MODEL") or "gemini-3.8-flash"
        if selected_model.startswith("models/"):
            selected_model = selected_model.replace("models/", "")
        self.model_name = selected_model
        
        # Load API keys
        keys_env = api_keys or os.getenv("GEMINI_API_KEYS") or os.getenv("GEMINI_API_KEY")
        mock_env = os.getenv("MOCK_GEMINI_JUDGE", "false").lower() == "true"

        if not keys_env:
            if mock_env:
                logger.warning("No GEMINI_API_KEY found, running in MOCK mode per MOCK_GEMINI_JUDGE=true.")
                self.api_keys = ["MOCK_KEY"]
                self.mock_mode = True
            else:
                self._trigger_vault_lock("GEMINI_API_KEY nedostaje!")
        else:
            self.api_keys = [k.strip() for k in keys_env.split(",") if k.strip()]
            self.mock_mode = False

        self.current_key_index = 0
        self.client = None
        self._configure_client()

    def _trigger_vault_lock(self, reason: str):
        """Halts system and requires user password to unlock or change keys."""
        msg = (
            f"🔒 VAULT ZAKLJUČAN! Razlog: {reason}\n"
            f"Svi API ključevi su nedostupni ili je konfiguracija zaključana.\n"
            f"Sistem se NE MOŽE menjati niti nastaviti bez unosa vaše šifre!\n"
            f"Pokrenite: python3 unlock_vault.py za unos šifre i novih ključeva."
        )
        logger.error(msg)
        raise VaultLockError(msg)

    def _configure_client(self):
        if getattr(self, "mock_mode", False):
            self.client = None
            logger.info("GeminiClient: Initialized in MOCK MODE")
            return

        from google import genai
        current_key = self.api_keys[self.current_key_index]
        self.client = genai.Client(api_key=current_key)

        masked_key = current_key[:6] + "..." + current_key[-4:] if len(current_key) > 12 else "****"
        logger.info(f"Configured GeminiClient with active key: {masked_key} | Model: {self.model_name}")

    def _rotate_key(self) -> bool:
        if len(self.api_keys) <= 1:
            logger.warning("Samo jedan API ključ je dostupan. Rotacija nije moguća.")
            return False
            
        self.current_key_index = (self.current_key_index + 1) % len(self.api_keys)
        logger.warning(f"🔄 Rotiram API ključ na indeks #{self.current_key_index + 1}")
        self._configure_client()
        return True

    def generate_content(self, prompt: str, generation_config: Optional[Dict] = None) -> str:
        if getattr(self, "mock_mode", False):
            if "reply PASSED if it aligns" in prompt or "Evaluate if the CONTENT meets" in prompt:
                return "PASSED"
            return "Mock response from Gemini Client"

        # Model candidates list: primary model first, followed by remaining active models
        models_to_try = [self.model_name] + [m for m in ACTIVE_MODELS if m != self.model_name]
        
        last_exception = None
        for model_candidate in models_to_try:
            for attempt in range(2):
                try:
                    resp = self.client.models.generate_content(
                        model=model_candidate,
                        contents=prompt
                    )
                    if resp and resp.text:
                        return resp.text
                except Exception as e:
                    last_exception = e
                    err_msg = str(e)
                    logger.warning(f"Attempt with model {model_candidate} failed: {err_msg.splitlines()[0]}")
                    if "429" in err_msg or "RESOURCE_EXHAUSTED" in err_msg or "403" in err_msg:
                        if self._rotate_key():
                            continue
                        time.sleep(1.5)
                    elif "503" in err_msg or "UNAVAILABLE" in err_msg:
                        # High demand spike, immediately try next model candidate
                        break
                    elif "404" in err_msg or "NOT_FOUND" in err_msg:
                        # Outdated/deprecated model, try next active model
                        break
                    else:
                        time.sleep(1.0)

        self._trigger_vault_lock(f"Svi Gemini modeli i ključevi su iscrpljeni ili blokirani! Poslednja greška: {last_exception}")

    def judge_content(self, content: str, criteria: str) -> bool:
        prompt = f"""
You are an impartial Judge AI.

CRITERIA:
{criteria}

CONTENT TO EVALUATE:
{content}

INSTRUCTIONS:
Evaluate if the CONTENT meets the CRITERIA.
If it meets ALL criteria, reply exactly with: PASSED
If it fails ANY criteria, reply exactly with: FAILED
Do not add any other text.
"""
        try:
            raw_result = self.generate_content(prompt)
            if not raw_result:
                raise ValueError("Empty response from Gemini")
            
            result = raw_result.strip().upper()
            logger.info(f"Gemini Real Verdict: {result}")
            return "PASSED" in result
        except Exception as e:
            logger.error(f"Gemini Judge Error: {e}")
            return False

