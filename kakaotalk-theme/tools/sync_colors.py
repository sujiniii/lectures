#!/usr/bin/env python3
"""안드로이드 palette.xml 을 기준으로 iOS theme.json 의 색을 맞춘다.

두 플랫폼 색을 손으로 두 번 고치면 반드시 어긋나므로, palette.xml 하나만
고치고 이 스크립트를 돌리면 된다.

    python3 tools/sync_colors.py            # 바뀔 내용만 보여줌
    python3 tools/sync_colors.py --write    # 실제로 반영
"""
import argparse
import json
import pathlib
import re
import sys
import xml.etree.ElementTree as ET

ROOT = pathlib.Path(__file__).resolve().parent.parent
PALETTE = ROOT / "android/app/src/main/res/values/palette.xml"
THEME_JSON = ROOT / "ios/theme/theme.json"

# iOS 키 -> palette.xml 의 색 이름
MAPPING = {
    "background": "palette_bg",
    "backgroundElevated": "palette_bg_elevated",
    "backgroundSunken": "palette_bg_sunken",
    "text": "palette_text",
    "textSecondary": "palette_text_secondary",
    "textDisabled": "palette_text_disabled",
    "accent": "palette_accent",
    "accentPressed": "palette_accent_pressed",
    "textOnAccent": "palette_text_on_accent",
    "divider": "palette_divider",
    "scrim": "palette_scrim",
    "navigationBarBackground": "palette_bg",
    "navigationBarTitle": "palette_text",
    "tabBarBackground": "palette_bg",
    "tabBarItemNormal": "palette_text_secondary",
    "tabBarItemSelected": "palette_text",
    "chatRoomBackground": "palette_bg_sunken",
    "bubbleMeBackground": "palette_bubble_me",
    "bubbleMeText": "palette_bubble_me_text",
    "bubbleYouBackground": "palette_bubble_you",
    "bubbleYouText": "palette_bubble_you_text",
    "chatTimeText": "palette_text_disabled",
    "chatUnreadCountText": "palette_accent_pressed",
    "inputBarBackground": "palette_bg",
    "inputText": "palette_text",
    "inputPlaceholder": "palette_text_disabled",
    "badgeBackground": "palette_badge",
    "badgeText": "palette_badge_text",
}


def read_palette():
    root = ET.parse(PALETTE).getroot()
    return {c.get("name"): (c.text or "").strip() for c in root.findall("color")}


def to_ios(value):
    """#AARRGGBB 중 완전 불투명이면 #RRGGBB 로 줄인다."""
    if not re.fullmatch(r"#[0-9A-Fa-f]{6,8}", value):
        raise ValueError(f"색 형식이 이상함: {value}")
    if len(value) == 9 and value[1:3].upper() == "FF":
        return "#" + value[3:].upper()
    return "#" + value[1:].upper()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true", help="파일에 실제로 반영")
    args = ap.parse_args()

    palette = read_palette()
    theme = json.loads(THEME_JSON.read_text(encoding="utf-8"))
    colors = theme.setdefault("colors", {})

    changes = []
    for ios_key, palette_key in MAPPING.items():
        if palette_key not in palette:
            print(f"palette.xml 에 {palette_key} 가 없습니다 — 건너뜀", file=sys.stderr)
            continue
        new = to_ios(palette[palette_key])
        old = colors.get(ios_key)
        if old != new:
            changes.append((ios_key, old, new))
            colors[ios_key] = new

    if not changes:
        print("이미 동일합니다.")
        return

    for key, old, new in changes:
        print(f"  {key}: {old} -> {new}")

    if args.write:
        THEME_JSON.write_text(
            json.dumps(theme, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        print(f"\n{len(changes)}개 반영: {THEME_JSON.relative_to(ROOT)}")
    else:
        print("\n--write 를 붙이면 반영됩니다.")


if __name__ == "__main__":
    main()
