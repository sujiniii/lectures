#!/usr/bin/env bash
# 새 테마 폴더를 _template 에서 복사해 만든다.
#   사용법: tools/new_theme.sh <테마-id> ["테마 이름"]
set -euo pipefail

cd "$(dirname "$0")/.."

ID="${1:-}"
DISPLAY_NAME="${2:-}"

if [[ -z "$ID" ]]; then
  echo "사용법: tools/new_theme.sh <테마-id> [\"테마 이름\"]" >&2
  echo "  테마-id: 영문 소문자로 시작, 소문자·숫자만 (패키지명이 됩니다)" >&2
  exit 1
fi

if [[ ! "$ID" =~ ^[a-z][a-z0-9]*$ ]]; then
  echo "테마 id 는 영문 소문자로 시작하고 소문자·숫자만 쓸 수 있습니다: '$ID'" >&2
  exit 1
fi

DEST="themes/$ID"
if [[ -e "$DEST" ]]; then
  echo "이미 있습니다: $DEST" >&2
  exit 1
fi

cp -R themes/_template "$DEST"

# 이름을 안 주면 id 를 그대로 쓴다.
python3 - "$DEST/theme.json" "${DISPLAY_NAME:-$ID}" <<'PY'
import json, sys
path, name = sys.argv[1], sys.argv[2]
with open(path, encoding="utf-8") as f:
    cfg = json.load(f)
cfg["name"] = name
with open(path, "w", encoding="utf-8") as f:
    json.dump(cfg, f, indent=2, ensure_ascii=False)
    f.write("\n")
PY

cat <<MSG
만들었습니다: $DEST

  1. $DEST/theme.json 의 colors 18개를 원하는 톤으로 수정
  2. 이미지를 넣습니다 (파일명은 각 폴더의 IMAGES.md 참고)
       $DEST/android/drawable-xxhdpi/
       $DEST/ios/images/
  3. python3 tools/validate.py $ID
  4. 빌드
       안드로이드: cd android && ./gradlew assemble${ID^}Release
       iOS:        python3 tools/build_ios.py $ID
MSG
