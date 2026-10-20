#!/usr/bin/env python3
"""Validate sticker pack files against WhatsApp sticker requirements."""
import json
import sys
from pathlib import Path

from PIL import Image

PACKS = Path(__file__).resolve().parent.parent / "packs"
MAX_STICKER_BYTES = 100 * 1024
MAX_TRAY_BYTES = 50 * 1024
MIN_STICKERS, MAX_STICKERS = 3, 30


def check_pack(manifest_path: Path) -> list[str]:
    errors = []
    pack_dir = manifest_path.parent
    try:
        manifest = json.loads(manifest_path.read_text())
    except json.JSONDecodeError as e:
        return [f"{manifest_path}: invalid JSON ({e})"]

    for key in ("id", "name", "version", "isPremium"):
        if key not in manifest:
            errors.append(f"{manifest_path}: missing '{key}'")

    tray = pack_dir / "tray.png"
    if not tray.exists():
        errors.append(f"{pack_dir}: missing tray.png")
    else:
        with Image.open(tray) as img:
            if img.size != (96, 96):
                errors.append(f"{tray}: must be 96x96, is {img.size}")
        if tray.stat().st_size > MAX_TRAY_BYTES:
            errors.append(f"{tray}: over 50 KB")

    stickers = sorted((pack_dir / "stickers").glob("*.webp"))
    if not MIN_STICKERS <= len(stickers) <= MAX_STICKERS:
        errors.append(f"{pack_dir}: {len(stickers)} stickers, need 3 to 30")
    for s in stickers:
        with Image.open(s) as img:
            if img.size != (512, 512) or img.format != "WEBP":
                errors.append(f"{s}: must be 512x512 WebP")
        if s.stat().st_size > MAX_STICKER_BYTES:
            errors.append(f"{s}: over 100 KB")
    return errors


def main() -> int:
    manifests = sorted(PACKS.glob("*/*/manifest.json"))
    if not manifests:
        print("No packs found.")
        return 0
    errors = [e for m in manifests for e in check_pack(m)]
    for e in errors:
        print(e)
    print(f"Checked {len(manifests)} pack(s), {len(errors)} error(s).")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
