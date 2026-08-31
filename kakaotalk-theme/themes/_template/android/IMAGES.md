# 이미지 넣는 곳 (안드로이드)

이 폴더(`themes/<테마-id>/android/drawable-xxhdpi`, 3x 기준)에 아래 파일명 그대로 PNG를 넣으면 카카오톡이 이름으로 찾아 씁니다.
**파일명이 곧 API**입니다. 오타가 나면 그냥 기본 이미지가 나오고 오류는 안 뜹니다.

- 기준 밀도는 xxhdpi(3x). 이것만 넣어도 나머지 해상도는 안드로이드가 축소해서 씁니다.
- 더 선명하게 하려면 같은 위치에 `drawable-xxxhdpi`(4x) 폴더를 추가로 만드세요.
- 말풍선처럼 늘어나야 하는 이미지는 반드시 **9-patch(`.9.png`)** 로 만듭니다.
- 넣지 않은 항목은 카카오톡 기본 이미지가 그대로 쓰입니다. 전부 채울 필요 없습니다.

## 1. 배경

| 파일명 | 용도 | 권장 크기 |
|---|---|---|
| `thm_general_default_bg.png` | 앱 전체(친구목록·채팅목록·더보기) 배경 | 1080 × 2400 |
| `thm_chatroom_bg.png` | 대화방 배경 | 1080 × 2400 |
| `thm_main_tab_bg.png` | 하단 탭 바 배경 | 1080 × 168 |
| `thm_actionbar_bg.png` | 상단 바 배경 | 1080 × 168 |

> 배경 이미지를 쓸 때는 공용 `colors.xml` 에서 해당 영역의 배경색을
> `@color/palette_transparent` 로 바꿔야 이미지가 가려지지 않습니다.
> (모든 테마에 영향을 주므로, 한 테마만 그렇게 하려면 그 테마의
> `android/values/colors.xml` 에 해당 항목만 덮어써도 됩니다.)

## 2. 말풍선 (9-patch 필수)

| 파일명 | 용도 |
|---|---|
| `thm_chatroom_bubble_me.9.png` | 내 말풍선 |
| `thm_chatroom_bubble_me_pressed.9.png` | 내 말풍선 눌림 |
| `thm_chatroom_bubble_you.9.png` | 상대 말풍선 |
| `thm_chatroom_bubble_you_pressed.9.png` | 상대 말풍선 눌림 |

9-patch 제작 요령: 상/좌 검은 선 = 늘어나는 구간, 하/우 검은 선 = 글자가 들어갈 영역.
꼬리 부분은 늘어나는 구간에서 반드시 제외하세요.

## 3. 하단 탭 아이콘 (각 normal / selected 한 쌍, 96 × 96)

`thm_main_tab_friends_normal.png` / `..._selected.png`
`thm_main_tab_chatroom_normal.png` / `..._selected.png`
`thm_main_tab_openchat_normal.png` / `..._selected.png`
`thm_main_tab_shopping_normal.png` / `..._selected.png`
`thm_main_tab_more_normal.png` / `..._selected.png`

## 4. 기타

| 파일명 | 용도 | 권장 크기 |
|---|---|---|
| `thm_general_profile_default_image.png` | 기본 프로필 이미지 | 300 × 300 |
| `thm_chatroom_send_button.png` | 전송 버튼 | 96 × 96 |
| `thm_chatroom_edit_bg.9.png` | 입력창 배경 (9-patch) | - |
| `thm_theme_preview.png` | 테마 설정 화면 미리보기 | 720 × 1280 |

---

`values/colors.xml` 언급이 나오면 그건 모든 테마가 공유하는
`android/app/src/main/res/values/colors.xml` 이고, 색 값 자체는
이 테마의 `theme.json` 에서 바꿉니다.
