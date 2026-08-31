#!/usr/bin/env python3
"""themes/<id> 를 iOS .ktheme 파일로 묶는다.

팔레트 18개 + 공용 매핑(ios/mapping.json) -> 카카오톡이 읽는 색 키로 펼친 뒤
이미지와 함께 zip 으로 묶고 확장자를 .ktheme 로 바꾼다.

    python3 tools/build_ios.py           # 전체 테마
    python3 tools/build_ios.py sunset    # 특정 테마
"""
import json
import pathlib
import shutil
import sys
import tempfile
import zipfile

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from validate import ROOT, load_json, theme_dirs, validate  # noqa: E402

OUT_DIR = ROOT / "build" / "ios"


def build(theme_dir):
    cfg = load_json(theme_dir / "theme.json")
    mapping = load_json(ROOT / "ios" / "mapping.json")
    image_slots = load_json(ROOT / "ios" / "images.json")
    images_dir = theme_dir / "ios" / "images"

    # 팔레트를 화면별 색 키로 펼친다.
    colors = {
        ios_key: cfg["colors"][palette_key]
        for ios_key, palette_key in mapping.items()
        if not ios_key.startswith("_")
    }

    # 실제로 있는 이미지만 남긴다. 없는 슬롯은 카카오톡 기본 이미지가 쓰인다.
    images = {
        slot: filename
        for slot, filename in image_slots.items()
        if not slot.startswith("_") and (images_dir / filename).exists()
    }

    payload = {
        "name": cfg["name"],
        "author": cfg["author"],
        "version": cfg["version"],
        "colors": colors,
        "images": images,
    }
    if "bubbleInsets" in cfg:
        payload["bubbleInsets"] = cfg["bubbleInsets"]

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUT_DIR / f"{theme_dir.name}.ktheme"

    with tempfile.TemporaryDirectory() as tmp:
        staging = pathlib.Path(tmp)
        (staging / "theme.json").write_text(
            json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        if images:
            shutil.copytree(images_dir, staging / "images", ignore=shutil.ignore_patterns("*.md", ".*"))

        # .ktheme 는 확장자만 바꾼 zip. theme.json 이 최상위에 와야 한다.
        with zipfile.ZipFile(out_path, "w", zipfile.ZIP_DEFLATED) as zf:
            for path in sorted(staging.rglob("*")):
                if path.is_file():
                    zf.write(path, path.relative_to(staging))

    return out_path, len(images)


def main():
    only = sys.argv[1] if len(sys.argv) > 1 else None
    dirs = theme_dirs(only)
    if not dirs:
        raise SystemExit("themes/ 에 테마가 없습니다.")

    failed = False
    for theme_dir in dirs:
        errors, warnings = validate(theme_dir)
        if errors:
            print(f"[건너뜀] {theme_dir.name} — 검사 실패")
            for msg in errors:
                print(f"    오류  {msg}")
            failed = True
            continue
        for msg in warnings:
            print(f"    경고  {theme_dir.name}: {msg}")
        out_path, n = build(theme_dir)
        print(f"[완성] {out_path.relative_to(ROOT)}  (이미지 {n}개)")

    if not failed:
        print("\nAirDrop 이나 메일로 아이폰에 보낸 뒤 카카오톡으로 열면 적용됩니다.")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
