from pathlib import Path


def run(track_path: Path) -> None:
    if not track_path.is_dir():
        raise NotADirectoryError(f"Path to track cannot be found: {track_path}")

    print(track_path)


