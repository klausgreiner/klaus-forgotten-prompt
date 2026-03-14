from pathlib import Path

RUNS_DIR = Path(__file__).resolve().parent.parent.parent / ".agent_tips"


def _level_tips_path(level: int) -> Path:
    return RUNS_DIR / f"level{level}_tips.txt"


def _ensure_runs_dir() -> Path:
    RUNS_DIR.mkdir(parents=True, exist_ok=True)
    return RUNS_DIR


def get_level_tips(level: int) -> str:
    path = _level_tips_path(level)
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8").strip()


def save_level_tips(level: int, tips: str) -> Path:
    _ensure_runs_dir()
    path = _level_tips_path(level)
    path.write_text(tips.strip(), encoding="utf-8")
    return path
