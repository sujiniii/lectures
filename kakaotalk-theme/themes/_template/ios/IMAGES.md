# 이미지 넣는 곳 (iOS)

`ios/images.json` 에 정의된 파일명 그대로 `themes/<테마-id>/ios/images/` 에 넣습니다.
파일이 없는 슬롯은 자동으로 빠지고 카카오톡 기본 이미지가 쓰입니다.

| 파일명 | 용도 | 권장 크기 (@3x) |
|---|---|---|
| `main_bg@3x.png` | 친구목록·채팅목록 배경 | 1242 × 2688 |
| `chatroom_bg@3x.png` | 대화방 배경 | 1242 × 2688 |
| `bubble_me@3x.png` | 내 말풍선 (늘어남 → `bubbleInsets` 로 여백 지정) | 120 × 90 내외 |
| `bubble_you@3x.png` | 상대 말풍선 | 120 × 90 내외 |
| `preview@3x.png` | 테마 미리보기 | 750 × 1334 |

- iOS 는 9-patch 가 없습니다. 말풍선은 일반 PNG 로 만들고 늘어나지 않을
  가장자리 두께를 `theme.json` 의 `bubbleInsets` 에 pt 단위로 적습니다.
- `@3x` 만 넣어도 됩니다. 필요하면 `@2x` 를 같이 넣으세요.
