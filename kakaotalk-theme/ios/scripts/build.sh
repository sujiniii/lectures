#!/usr/bin/env bash
# theme/ 폴더를 .ktheme (zip) 으로 묶는다.
#   사용법: ./scripts/build.sh [출력이름]
set -euo pipefail

cd "$(dirname "$0")/.."

SRC="theme"
OUT_DIR="build"
NAME="${1:-}"

if [[ ! -f "$SRC/theme.json" ]]; then
  echo "theme/theme.json 이 없습니다." >&2
  exit 1
fi

# 이름을 안 주면 theme.json 의 name 을 쓴다 (공백은 _ 로).
if [[ -z "$NAME" ]]; then
  NAME=$(python3 -c "import json,sys; print(json.load(open('$SRC/theme.json'))['name'])")
fi
NAME="${NAME// /_}"

# JSON 이 깨졌으면 여기서 걸러진다. 기기에 넣고 나서 알면 늦다.
python3 -m json.tool "$SRC/theme.json" > /dev/null

# theme.json 에 적힌 이미지가 실제로 있는지 확인
python3 - "$SRC" <<'PY'
import json, os, sys
src = sys.argv[1]
data = json.load(open(os.path.join(src, "theme.json")))
missing = [
    v for k, v in data.get("images", {}).items()
    if not k.startswith("_") and not os.path.exists(os.path.join(src, "images", v))
]
if missing:
    print("경고: theme.json 에 적혔지만 images/ 에 없는 파일 -> " + ", ".join(missing))
PY

rm -rf "$OUT_DIR"
mkdir -p "$OUT_DIR"

# .ktheme 는 확장자만 바꾼 zip. 최상위에 theme.json 이 오도록 theme/ 내부에서 압축한다.
( cd "$SRC" && zip -r -q -X "../$OUT_DIR/$NAME.ktheme" . -x '.*' -x '*/.*' -x 'images/README.md' )

echo "완성: $OUT_DIR/$NAME.ktheme"
echo "AirDrop 이나 메일로 아이폰에 보낸 뒤 카카오톡으로 열면 적용됩니다."
