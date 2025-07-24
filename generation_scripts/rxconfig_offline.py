import reflex as rx
import os

# Offline mode configuration
config = rx.Config(
    app_name="local_llama",
    # Disable telemetry for offline mode
    telemetry_enabled=False,
    # Environment
    env=rx.Env.DEV,
    # Database URL (use SQLite for offline)
    db_url=os.getenv("DATABASE_URL", "sqlite:///local_llama_offline.db"),
)

# Offline mode settings
OFFLINE_MODE = os.getenv("OFFLINE_MODE", "false").lower() == "true"

if OFFLINE_MODE:
    print("Running in OFFLINE MODE")
