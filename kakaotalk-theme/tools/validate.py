#!/usr/bin/env python3
"""themes/ 아래 테마들을 검사한다.

기기에 넣어보고 나서 오타를 발견하면 늦으므로, 빌드 전에 걸러낸다.

    python3 tools/validate.py            # 전체
    python3 tools/validate.py sunset     # 특정 테마
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
THEMES = ROOT / "themes"
TEMPLATE = THEMES / "_template" / "theme.json"

HEX = re.compile(r"#(?:[0-9A-Fa-f]{6}|[0-9A-Fa-f]{8})$")
THEME_ID = re.compile(r"^[a-z][a-z0-9]*$")


def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def required_color_keys():
    """팔레트 키의 기준은 _template/theme.json. 목록을 두 곳에 두지 않는다."""
    return set(load_json(TEMPLATE)["colors"])


def check_shared_mappings():
    """공용 매핑이 팔레트에 없는 키를 참조하는지 본다.

    thm_* 를 추가하다 팔레트에 없는 이름을 쓰면 안드로이드는 빌드 에러,
    iOS 는 조용히 색이 빠진다. 테마와 무관한 저장소 차원의 검사다.
    """
    errors = []
    required = required_color_keys()

    colors_xml = ROOT / "android/app/src/main/res/values/colors.xml"
    used = set(re.findall(r"@color/palette_([a-z0-9_]+)", colors_xml.read_text(encoding="utf-8")))
    # palette_background_elevated -> backgroundElevated
    for name in sorted(used):
        camel = re.sub(r"_([a-z0-9])", lambda m: m.group(1).upper(), name)
        if camel not in required:
            errors.append(
                f"colors.xml 이 @color/palette_{name} 을 쓰는데 팔레트에 '{camel}' 가 없습니다"
            )

    mapping = load_json(ROOT / "ios" / "mapping.json")
    for ios_key, palette_key in mapping.items():
        if ios_key.startswith("_"):
            continue
        if palette_key not in required:
            errors.append(
                f"mapping.json 의 '{ios_key}' 가 없는 팔레트 키 '{palette_key}' 를 가리킵니다"
            )

    return errors


def theme_dirs(only=None):
    if not THEMES.is_dir():
        return []
    dirs = sorted(
        d for d in THEMES.iterdir()
        if d.is_dir() and not d.name.startswith("_") and (d / "theme.json").exists()
    )
    if only:
        dirs = [d for d in dirs if d.name == only]
        if not dirs:
            raise SystemExit(f"'{only}' 테마를 themes/ 에서 찾을 수 없습니다.")
    return dirs


def validate(theme_dir):
    """(오류 목록, 경고 목록) 을 돌려준다. 경고는 빌드를 막지 않는다."""
    errors, warnings = [], []
    name = theme_dir.name

    if not THEME_ID.match(name):
        errors.append(
            f"테마 id '{name}': 영문 소문자로 시작하고 소문자·숫자만 써야 합니다 "
            "(안드로이드 패키지명과 Gradle flavor 이름이 됩니다)"
        )

    try:
        cfg = load_json(theme_dir / "theme.json")
    except json.JSONDecodeError as e:
        return [f"theme.json JSON 문법 오류: {e}"], []

    for field in ("name", "author", "version"):
        if not str(cfg.get(field, "")).strip():
            errors.append(f"theme.json 에 '{field}' 가 비어 있습니다")

    colors = cfg.get("colors") or {}
    required = required_color_keys()

    for key in sorted(required - set(colors)):
        errors.append(f"팔레트 색 '{key}' 가 빠졌습니다")
    for key in sorted(set(colors) - required):
        warnings.append(f"팔레트에 없는 색 '{key}' — 아무 데도 쓰이지 않습니다")

    for key, value in sorted(colors.items()):
        if not isinstance(value, str) or not HEX.match(value):
            errors.append(f"색 '{key}' 값이 잘못됨: {value!r} (#RRGGBB 또는 #AARRGGBB)")

    android_dir = theme_dir / "android"
    ios_dir = theme_dir / "ios" / "images"

    pngs = list(android_dir.rglob("*.png")) if android_dir.is_dir() else []
    for png in pngs:
        if not png.name.startswith("thm_"):
            warnings.append(
                f"android/{png.relative_to(android_dir)}: 이름이 thm_ 로 시작하지 않아 "
                "카카오톡이 찾지 못합니다"
            )
    if not pngs and not (list(ios_dir.glob("*.png")) if ios_dir.is_dir() else []):
        warnings.append("이미지가 하나도 없습니다 — 색만 바뀐 테마가 됩니다")

    for slot, filename in load_json(ROOT / "ios" / "images.json").items():
        if slot.startswith("_"):
            continue
        if not (ios_dir / filename).exists():
            warnings.append(f"iOS 이미지 없음: ios/images/{filename} ({slot})")

    return errors, warnings


def main():
    only = sys.argv[1] if len(sys.argv) > 1 else None
    dirs = theme_dirs(only)
    if not dirs:
        raise SystemExit("themes/ 에 테마가 없습니다. tools/new_theme.sh <테마-id> 로 만드세요.")

    failed = False

    shared_errors = check_shared_mappings()
    print(f"[{'실패' if shared_errors else '통과'}] 공용 매핑 (colors.xml, mapping.json)")
    for msg in shared_errors:
        print(f"    오류  {msg}")
    failed |= bool(shared_errors)

    for theme_dir in dirs:
        errors, warnings = validate(theme_dir)
        status = "실패" if errors else "통과"
        print(f"[{status}] {theme_dir.name}")
        for msg in errors:
            print(f"    오류  {msg}")
        for msg in warnings:
            print(f"    경고  {msg}")
        failed |= bool(errors)

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
