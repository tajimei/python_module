import importlib
import importlib.metadata
import sys
from types import ModuleType
from typing import Any

REQUIRED: dict[str, str] = {
    "pandas": "Data manipulation ready",
    "numpy": "Numerical computation ready",
    "matplotlib": "Visualization ready",
}

OUTPUT_FILE: str = "matrix_analysis.png"
DATA_POINTS: int = 1000


def get_version(package: str) -> str | None:
    """Return the installed version of a package, or None if missing."""
    try:
        return importlib.metadata.version(package)
    except importlib.metadata.PackageNotFoundError:
        return None


def check_dependencies() -> list[str]:
    """Print the status of each dependency and return the missing ones."""
    missing: list[str] = []
    print("Checking dependencies:")
    for package, message in REQUIRED.items():
        version: str | None = get_version(package)
        if version is None:
            print(f"[MISSING] {package} - not installed")
            missing.append(package)
        else:
            print(f"[OK] {package} ({version}) - {message}")
    return missing


def detect_manager() -> str:
    """Guess which tool created the current environment."""
    if sys.prefix == sys.base_prefix:
        return "global Python (no virtual environment)"
    if "pypoetry" in sys.prefix:
        return "Poetry-managed virtual environment"
    return "virtual environment (pip / venv)"


def show_manager_comparison() -> None:
    """Explain the difference between pip and Poetry."""
    print("Environment in use:")
    print(f"  Python: {sys.executable}")
    print(f"  Prefix: {sys.prefix}")
    print(f"  Type:   {detect_manager()}")
    print()
    print("pip vs Poetry:")
    print("  pip    -> requirements.txt, you create and activate")
    print("            the venv yourself, versions are resolved")
    print("            at install time")
    print("  Poetry -> pyproject.toml + poetry.lock, the venv is")
    print("            created for you, exact versions are locked")
    print("            so every install is identical")


def show_install_help(missing: list[str]) -> None:
    """Show how to install the missing packages."""
    print()
    print(f"Missing dependencies: {', '.join(missing)}")
    print("The program cannot run without them.")
    print()
    print("Install with pip:")
    print("  pip install -r requirements.txt")
    print("  python3 loading.py")
    print()
    print("Install with Poetry:")
    print("  poetry install")
    print("  poetry run python loading.py")


def load(name: str) -> ModuleType:
    """Import a module by name once dependencies are confirmed."""
    return importlib.import_module(name)


def generate_data(np: Any, pd: Any) -> Any:
    """Simulate Matrix data with numpy and wrap it in a DataFrame."""
    rng: Any = np.random.default_rng(42)
    signal: Any = rng.normal(loc=0.0, scale=1.0, size=DATA_POINTS)
    return pd.DataFrame(
        {
            "step": np.arange(DATA_POINTS),
            "signal": signal,
            "anomaly": np.abs(signal) > 2.5,
        }
    )


def analyze(df: Any) -> Any:
    """Compute summary statistics and a moving average."""
    df["moving_avg"] = df["signal"].rolling(window=50).mean()
    print(f"  Mean:      {df['signal'].mean():.4f}")
    print(f"  Std dev:   {df['signal'].std():.4f}")
    print(f"  Anomalies: {int(df['anomaly'].sum())}")
    return df


def visualize(df: Any) -> None:
    """Plot the signal and save it to a PNG file."""
    matplotlib: ModuleType = load("matplotlib")
    matplotlib.use("Agg")
    plt: ModuleType = load("matplotlib.pyplot")
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(df["step"], df["signal"], linewidth=0.6,
            color="#2e8b57", label="Signal")
    ax.plot(df["step"], df["moving_avg"], linewidth=2,
            color="#111111", label="Moving average (50)")
    anomalies: Any = df[df["anomaly"]]
    ax.scatter(anomalies["step"], anomalies["signal"],
               color="#c0392b", s=15, label="Anomalies", zorder=3)
    ax.set_title("Matrix Data Analysis")
    ax.set_xlabel("Step")
    ax.set_ylabel("Signal")
    ax.legend()
    fig.tight_layout()
    fig.savefig(OUTPUT_FILE)
    plt.close(fig)


def main() -> None:
    """Entry point."""
    print("LOADING STATUS: Loading programs...")
    print()
    missing: list[str] = check_dependencies()
    print()
    show_manager_comparison()
    if missing:
        show_install_help(missing)
        sys.exit(1)

    try:
        np: ModuleType = load("numpy")
        pd: ModuleType = load("pandas")
        print()
        print("Analyzing Matrix data...")
        print(f"Processing {DATA_POINTS} data points...")
        df: Any = analyze(generate_data(np, pd))
        print("Generating visualization...")
        visualize(df)
    except Exception as error:
        print(f"ERROR: analysis failed: {error}")
        sys.exit(1)

    print()
    print("Analysis complete!")
    print(f"Results saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()