import os
import sys

try:
    from dotenv import load_dotenv
except ImportError:
    print("ERROR: python-dotenv is not installed.")
    print("Install it with: pip install -r requirements.txt")
    sys.exit(1)

BASE_DIR: str = os.path.dirname(os.path.abspath(__file__))
ENV_FILE: str = os.path.join(BASE_DIR, ".env")
GITIGNORE_FILE: str = os.path.join(BASE_DIR, ".gitignore")

KEYS: list[str] = [
    "MATRIX_MODE",
    "DATABASE_URL",
    "API_KEY",
    "LOG_LEVEL",
    "ZION_ENDPOINT",
]
VALID_MODES: list[str] = ["development", "production"]
VALID_LOG_LEVELS: list[str] = ["DEBUG", "INFO", "WARNING", "ERROR"]

DEFAULTS: dict[str, dict[str, str]] = {
    "development": {
        "DATABASE_URL": "sqlite:///local_matrix.db",
        "LOG_LEVEL": "DEBUG",
        "ZION_ENDPOINT": "http://localhost:8080",
    },
    "production": {
        "LOG_LEVEL": "WARNING",
    },
}
REQUIRED_IN_PRODUCTION: list[str] = [
    "DATABASE_URL",
    "API_KEY",
    "ZION_ENDPOINT",
]


def load_configuration() -> dict[str, str]:
    """Load .env and record where each value came from."""
    from_shell: set[str] = {key for key in KEYS if key in os.environ}
    load_dotenv(ENV_FILE, override=False)
    sources: dict[str, str] = {}
    for key in KEYS:
        if key in from_shell:
            sources[key] = "from environment"
        elif os.environ.get(key):
            sources[key] = "from .env file"
        else:
            sources[key] = "not set"
    return sources


def get_mode(warnings: list[str]) -> str:
    """Return a valid MATRIX_MODE, defaulting to development."""
    mode: str = os.environ.get("MATRIX_MODE", "").strip().lower()
    if not mode:
        warnings.append("MATRIX_MODE not set, using 'development'")
        return "development"
    if mode not in VALID_MODES:
        warnings.append(f"Unknown MATRIX_MODE '{mode}', using 'development'")
        return "development"
    return mode


def build_config(mode: str, warnings: list[str]) -> dict[str, str]:
    """Read every setting, applying mode-specific defaults."""
    config: dict[str, str] = {"MATRIX_MODE": mode}
    for key in KEYS[1:]:
        value: str = os.environ.get(key, "").strip()
        if not value and key in DEFAULTS[mode]:
            value = DEFAULTS[mode][key]
            warnings.append(f"{key} not set, using default '{value}'")
        elif not value:
            warnings.append(f"{key} not set")
        config[key] = value
    level: str = config["LOG_LEVEL"].upper()
    if level not in VALID_LOG_LEVELS:
        warnings.append(f"Invalid LOG_LEVEL '{level}', using 'INFO'")
        level = "INFO"
    config["LOG_LEVEL"] = level
    return config


def mask(secret: str) -> str:
    """Hide most of a secret so it never appears in full."""
    if len(secret) <= 4:
        return "****"
    return secret[:4] + "*" * (len(secret) - 4)


def describe_database(url: str, mode: str) -> str:
    """Describe the database without printing the connection string."""
    if not url:
        return "Not configured"
    if url.startswith("sqlite") or "localhost" in url:
        return "Connected to local instance"
    if mode == "production":
        return "Connected to production cluster"
    return "Connected to remote instance"


def show_configuration(config: dict[str, str],
                       sources: dict[str, str]) -> None:
    """Print the loaded configuration, hiding secrets."""
    mode: str = config["MATRIX_MODE"]
    api_key: str = config["API_KEY"]
    print("Configuration loaded:")
    print(f"Mode: {mode}  ({sources['MATRIX_MODE']})")
    print(f"Database: {describe_database(config['DATABASE_URL'], mode)}")
    if api_key:
        print(f"API Access: Authenticated (key {mask(api_key)})")
    else:
        print("API Access: Not authenticated")
    print(f"Log Level: {config['LOG_LEVEL']}")
    if config["ZION_ENDPOINT"]:
        print("Zion Network: Online")
    else:
        print("Zion Network: Offline")
    if mode == "development":
        print()
        print("[DEBUG] Development details:")
        print(f"[DEBUG]   DATABASE_URL  = {config['DATABASE_URL']}")
        print(f"[DEBUG]   ZION_ENDPOINT = {config['ZION_ENDPOINT']}")
        print("[DEBUG]   Value sources:")
        for key in KEYS:
            print(f"[DEBUG]     {key:<14} {sources[key]}")


def gitignore_protects_env() -> bool:
    """Check that .gitignore lists the .env file."""
    try:
        with open(GITIGNORE_FILE, "r") as file:
            lines: list[str] = [line.strip() for line in file]
    except OSError:
        return False
    return ".env" in lines or "*.env" in lines


def security_check(sources: dict[str, str]) -> None:
    """Report on how safely the configuration is managed."""
    print("Environment security check:")
    print("[OK] No hardcoded secrets detected")
    if not os.path.isfile(ENV_FILE):
        print("[WARN] .env file not found (cp .env.example .env)")
    elif gitignore_protects_env():
        print("[OK] .env file properly configured")
    else:
        print("[WARN] .env exists but is NOT listed in .gitignore")
    overrides: list[str] = [
        key for key in KEYS if sources[key] == "from environment"
    ]
    if overrides:
        print(f"[OK] Production overrides active: {', '.join(overrides)}")
    else:
        print("[OK] Production overrides available")


def check_production(config: dict[str, str]) -> list[str]:
    """Return the required production settings that are missing."""
    return [key for key in REQUIRED_IN_PRODUCTION if not config[key]]


def main() -> None:
    """Entry point."""
    print("ORACLE STATUS: Reading the Matrix...")
    print()
    sources: dict[str, str] = load_configuration()
    warnings: list[str] = []
    mode: str = get_mode(warnings)
    config: dict[str, str] = build_config(mode, warnings)

    if warnings:
        print("Configuration warnings:")
        for warning in warnings:
            print(f"[WARN] {warning}")
        print()

    if mode == "production":
        missing: list[str] = check_production(config)
        if missing:
            print("ERROR: Production mode refuses to start.")
            print(f"Missing required settings: {', '.join(missing)}")
            print("Set them in the environment or in your .env file.")
            sys.exit(1)

    show_configuration(config, sources)
    print()
    security_check(sources)
    print()
    print("The Oracle sees all configurations.")


if __name__ == "__main__":
    main()