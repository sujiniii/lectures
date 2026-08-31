# 테마 폴더

테마 하나 = 폴더 하나. 각 폴더가 **그 테마의 유일한 진실**입니다.

```
themes/<테마-id>/
├─ theme.json                 이름·버전·팔레트 색 18개
├─ android/drawable-xxhdpi/   안드로이드 이미지 (thm_*.png)
└─ ios/images/                iOS 이미지 (*@3x.png)
```

- `<테마-id>` 는 영문 소문자/숫자만. 안드로이드 패키지명
  `com.kakao.talk.theme.<테마-id>` 와 Gradle flavor 이름이 됩니다.
- `_` 로 시작하는 폴더(`_template`)는 빌드에서 제외됩니다.
- 새 테마: `tools/new_theme.sh <테마-id>`

## 팔레트 색 18개

`theme.json` 의 `colors` 는 이 18개가 전부입니다. 카카오톡이 실제로 읽는
화면별 색 60여 개는 여기서 **자동으로 파생**됩니다 (안드로이드는
`android/app/src/main/res/values/colors.xml`, iOS는 `ios/mapping.json`).
그 매핑은 모든 테마가 공유하므로 테마를 늘려도 복제되지 않습니다.

| 키 | 쓰이는 곳 |
|---|---|
| `background` | 앱 기본 배경 |
| `backgroundElevated` | 섹션 헤더 등 한 겹 떠 있는 면 |
| `backgroundSunken` | 대화방 배경처럼 한 겹 들어간 면 |
| `text` | 기본 글자 |
| `textSecondary` | 보조 글자 (미리보기 메시지, 설명) |
| `textDisabled` | 흐린 글자 (시간, 힌트) |
| `textOnAccent` | 포인트 색 위에 얹는 글자 |
| `accent` | 포인트 색 (전송 버튼, 주요 버튼) |
| `accentPressed` | 포인트 색 눌림 / 링크 / 안읽음 숫자 |
| `divider` | 구분선 |
| `scrim` | 팝업 뒤 어두운 막 |
| `bubbleMe` / `bubbleMeText` | 내 말풍선 배경 / 글자 |
| `bubbleYou` / `bubbleYouText` | 상대 말풍선 배경 / 글자 |
| `badge` / `badgeText` | 안읽음 뱃지 |
| `transparent` | 배경 이미지를 그대로 보이게 할 자리에 지정 |

색 형식은 `#RRGGBB` 또는 `#AARRGGBB`. 두 플랫폼 모두 그대로 씁니다.
