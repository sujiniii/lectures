# 카카오톡 테마 만들기

안드로이드(APK)와 iOS(.ktheme) 테마를 같은 색 팔레트로 함께 관리하는 프로젝트입니다.
이미지는 준비되는 대로 정해진 폴더에 파일명만 맞춰 넣으면 됩니다.

```
kakaotalk-theme/
├─ android/                    안드로이드 테마 APK (Gradle)
│  └─ app/src/main/res/
│     ├─ values/palette.xml    ← 색은 전부 여기서 시작
│     ├─ values/colors.xml     ← 카카오톡이 읽는 thm_* 색 (palette 참조만)
│     └─ drawable-xxhdpi/      ← 안드로이드 이미지 (IMAGES.md 참고)
├─ ios/
│  ├─ theme/theme.json         ← iOS 색 + 이미지 매핑
│  ├─ theme/images/            ← iOS 이미지 (README.md 참고)
│  └─ scripts/build.sh         ← .ktheme 로 묶기
├─ tools/sync_colors.py        palette.xml → theme.json 색 동기화
└─ assets/source/              PSD·AI 등 작업 원본 (APK 에는 안 들어감)
```

## 1. 색 정하기

`android/app/src/main/res/values/palette.xml` **한 파일만** 고칩니다.
`colors.xml` 의 `thm_*` 는 전부 이 팔레트를 참조하므로, 여기서 배경색 하나 바꾸면
관련된 화면이 한꺼번에 따라옵니다.

배경 이미지를 쓸 화면은 해당 배경색을 `@color/palette_transparent` 로 바꿔야
이미지가 색에 가려지지 않습니다.

색을 고친 뒤 iOS 쪽에 반영:

```bash
python3 tools/sync_colors.py            # 바뀔 내용 확인
python3 tools/sync_colors.py --write    # 반영
```

## 2. 이미지 넣기

- 안드로이드: `android/app/src/main/res/drawable-xxhdpi/IMAGES.md`
- iOS: `ios/theme/images/README.md`

두 문서에 **파일명 · 용도 · 권장 크기**가 표로 정리되어 있습니다.
파일명이 곧 식별자라서 오타가 나면 오류 없이 그냥 기본 이미지가 나옵니다.
넣지 않은 항목은 카카오톡 기본값이 쓰이므로, 배경과 말풍선만 넣어도 테마가 됩니다.

## 3. 빌드

**안드로이드**

```bash
cd android
./gradlew assembleRelease
# app/build/outputs/apk/release/ 에 APK 생성 → 기기에 설치 후
# 카카오톡 > 더보기 > 설정 > 테마 에서 선택
```

테마 이름·제작자·버전은 `android/gradle.properties` 에서 바꿉니다.
패키지명은 `com.kakao.talk.theme.<themeId>` 로 자동 구성됩니다.

> Gradle wrapper 는 포함돼 있지 않습니다. Android Studio 로 `android/` 를 열면
> 자동 생성되고, CLI 만 쓴다면 `gradle wrapper` 를 한 번 실행하세요.
> 배포용 APK 는 `app/build.gradle` 의 release `signingConfig` 를 본인 키로 교체해야 합니다.

**iOS**

```bash
cd ios
./scripts/build.sh
# build/<테마이름>.ktheme 생성 → AirDrop/메일로 아이폰에 보낸 뒤 카카오톡으로 열기
```

빌드 스크립트가 JSON 문법과 이미지 누락을 먼저 검사합니다.

## 확인이 필요한 부분

리소스 이름과 규격 값은 카카오톡 버전에 따라 바뀝니다. 뼈대는 관례를 따라 잡아뒀지만,
실제 적용 전에 **카카오 공식 테마 제작 가이드의 리소스 목록**과 대조하는 것을 권합니다.

- `values/colors.xml` 의 `thm_*` 목록 — 자주 쓰이는 항목만 담았습니다. 최신 가이드에
  있는데 여기 없는 이름은 추가하면 되고, 정의 안 한 이름은 기본값이 쓰여 앱이 깨지지는 않습니다.
- `AndroidManifest.xml` 의 `com.kakao.talk.theme.*` 메타데이터 키와
  `values/strings.xml` 의 `thm_theme_spec_version`(현재 `10`).
- `ios/theme/theme.json` 의 키 이름 — iOS `.ktheme` 내부 규격은 공개 문서가 적어
  적용해 보며 맞춰야 할 수 있습니다.

실제 기기에서 한 번 적용해 보면 어긋난 이름이 바로 드러납니다. 배경 → 말풍선 → 탭 아이콘
순서로 하나씩 넣어가며 확인하는 게 가장 빠릅니다.
