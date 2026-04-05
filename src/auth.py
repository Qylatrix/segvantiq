"""
src/auth.py — SEGVANTIQ SaaS Authentication Engine
Supports persistent business accounts via Supabase.
Falls back to session-based demo mode if Supabase is not configured.
Includes bcrypt hashing for enterprise-grade security.
"""
import streamlit as st
import bcrypt
from datetime import datetime
from typing import Optional, Dict, Any, Tuple


# ── Demo fallback credentials (used if Supabase/Secrets not configured) ──────
_DEMO_USERS = {
    "demo": {"password": "demo", "business": "Demo Business", "plan": "Free", "email": "demo@segvantiq.com"},
    "qylatrix": {"password": "qylatrix2026", "business": "Qylatrix HQ", "plan": "Enterprise", "email": "pretam@qylatrix.com"},
}


# ── Supabase Setup ───────────────────────────────────────────────────────────
def get_supabase_client():
    """Returns a Supabase client if URL/KEY are in st.secrets, else None."""
    try:
        url = st.secrets.get("SUPABASE_URL")
        key = st.secrets.get("SUPABASE_KEY")
        if url and key:
            from supabase import create_client
            return create_client(url, key)
    except Exception:
        pass
    return None


# ── Password Hashing ─────────────────────────────────────────────────────────
def hash_password(password: str) -> str:
    """Returns a bcrypt hashed string of the password."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def check_password(password: str, hashed: str) -> bool:
    """Verifies a password against a bcrypt hash."""
    try:
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
    except Exception:
        return False


# ── Auth Logic ───────────────────────────────────────────────────────────────
def _get_demo_users() -> dict:
    """Load users from Streamlit secrets, falling back to demo users."""
    try:
        raw = st.secrets.get("users", {})
        if raw:
            return {k: dict(v) for k, v in raw.items()}
    except Exception:
        pass
    # Merge with any session-registered users (demo mode persistence)
    demo_base = _DEMO_USERS.copy()
    demo_base.update(st.session_state.get("session_registered_users", {}))
    return demo_base


def is_authenticated() -> bool:
    """Returns True if the current session has an authenticated user."""
    return st.session_state.get("segvantiq_auth", False)


def get_current_user() -> Optional[Dict[str, Any]]:
    """Returns the logged-in user dict or None."""
    return st.session_state.get("segvantiq_user", None)


def login(username: str, password: str) -> bool:
    """
    Validates credentials against Supabase (if available) or Demo users.
    Returns True on success, False on failure.
    """
    username = username.strip().lower()
    supabase = get_supabase_client()

    if supabase:
        try:
            # Persistent DB check
            response = supabase.table("businesses").select("*").eq("username", username).execute()
            if response.data:
                db_user = response.data[0]
                if check_password(password, db_user["password_hash"]):
                    _set_session_user(db_user)
                    return True
        except Exception as e:
            st.error(f"Database error: {e}")

    # Fallback to Demo/Secret users
    users = _get_demo_users()
    if username in users:
        user_data = users[username]
        # In demo mode, we support both plain text (for demo) and hash
        stored_pw = user_data.get("password", "")
        if stored_pw == password or check_password(password, stored_pw):
            _set_session_user({
                "username": username,
                "business_name": user_data.get("business", username.title()),
                "plan_tier": user_data.get("plan", "Free"),
                "email": user_data.get("email", ""),
            })
            return True

    return False


def register(username: str, password: str, business: str, email: str) -> Tuple[bool, str]:
    """
    Registers a new business in Supabase (persistent) or session state (demo).
    Returns (success, message).
    """
    username = username.strip().lower()
    if len(username) < 3: return False, "Username too short."
    if len(password) < 6: return False, "Password must be 6+ chars."
    if not business:      return False, "Business name is required."

    supabase = get_supabase_client()
    hashed_pw = hash_password(password)

    if supabase:
        try:
            # Check for existing
            exists = supabase.table("businesses").select("id").eq("username", username).execute()
            if exists.data:
                return False, "Username already taken."
            
            # Persistent write
            new_user = {
                "username": username,
                "password_hash": hashed_pw,
                "business_name": business,
                "email": email,
                "plan_tier": "Free"
            }
            res = supabase.table("businesses").insert(new_user).execute()
            if res.data:
                _set_session_user(res.data[0])
                return True, "Success! Your SaaS account is now live."
        except Exception as e:
            return False, f"Registration failed (DB): {e}"

    # Demo Fallback
    demo_users = _get_demo_users()
    if username in demo_users:
        return False, "Username already taken (demo mode)."

    st.session_state.setdefault("session_registered_users", {})[username] = {
        "password": hashed_pw,
        "business": business,
        "plan": "Free",
        "email": email,
    }
    _set_session_user({
        "username": username,
        "business_name": business,
        "plan_tier": "Free",
        "email": email,
    })
    return True, "Account created! Note: Demo accounts are not persistent."


def logout() -> None:
    """Clears the session auth state."""
    for key in ["segvantiq_auth", "segvantiq_user"]:
        st.session_state.pop(key, None)


def require_auth() -> dict:
    """Protected page guard. Redirects to landing if not auth."""
    if not is_authenticated():
        st.switch_page("app.py")
    return get_current_user()  # type: ignore[return-value]


def _set_session_user(db_user: Dict[str, Any]) -> None:
    """Helper to sync DB record with Streamlit session state."""
    st.session_state["segvantiq_auth"] = True
    st.session_state["segvantiq_user"] = {
        "username": db_user["username"],
        "business": db_user.get("business_name", db_user["username"].title()),
        "plan": db_user.get("plan_tier", "Free"),
        "email": db_user.get("email", ""),
        "logged_in_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }
