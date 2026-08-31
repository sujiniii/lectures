# 카카오톡 테마

테마를 **여러 개** 만들어 나가기 위한 저장소입니다.
테마 하나 = `themes/` 아래 폴더 하나. 빌드 설정은 건드리지 않습니다.

```
kakaotalk-theme/
├─ themes/                     ← 테마는 전부 여기. 폴더 하나가 테마 하나
│  ├─ _template/                 새 테마의 시작점 (빌드 제외)
│  ├─ mytheme/
│  │  ├─ theme.json              이름·버전·팔레트 색 18개
│  │  ├─ android/drawable-xxhdpi/  안드로이드 이미지
│  │  └─ ios/images/               iOS 이미지
│  └─ mono/                     예시 다크 테마
│
├─ android/                    모든 테마가 공유하는 빌드 (테마별 flavor 자동 생성)
│  └─ app/src/main/res/values/colors.xml   thm_* 60여 개 → 팔레트 매핑
├─ ios/
│  ├─ mapping.json             iOS 색 키 → 팔레트 매핑
│  └─ images.json              iOS 이미지 슬롯 → 파일명
└─ tools/
   ├─ new_theme.sh             새 테마 만들기
   ├─ validate.py              색·이미지·이름 검사
   └─ build_ios.py             .ktheme 빌드
```

**핵심은 공유되는 것과 테마마다 다른 것을 나눈 것입니다.** 카카오톡이 실제로 읽는
색 이름은 화면별로 60개가 넘지만, 그건 어느 테마든 똑같습니다. 그래서 그 매핑은
`colors.xml`·`mapping.json` 에 한 번만 두고, 테마마다 바뀌는 건 **팔레트 색 18개와
이미지뿐**입니다. 테마를 20개 만들어도 매핑은 여전히 한 벌입니다.

## 새 테마 만들기

```bash
tools/new_theme.sh sunset "노을"
```

`themes/sunset/` 이 생깁니다. 그다음:

1. `themes/sunset/theme.json` 의 `colors` 18개 수정 (설명은 `themes/README.md`)
2. 이미지 넣기 — 파일명·크기는 각 폴더의 `IMAGES.md` 참고
3. `python3 tools/validate.py sunset`

이미지 없이 색만 바꿔도 테마가 됩니다. 배경 2장 + 말풍선 2장이면 충분히 테마 같아집니다.

## 빌드

```bash
# 안드로이드 — 테마 전부
cd android && ./gradlew assembleRelease
# 안드로이드 — 하나만
cd android && ./gradlew assembleSunsetRelease
# 어떤 테마가 인식됐는지 확인
cd android && ./gradlew listThemes

# iOS — 테마 전부 (하나만: 뒤에 테마-id)
python3 tools/build_ios.py
```

결과물:
- 안드로이드 `android/app/build/outputs/apk/<테마-id>/release/` → 설치 후
  카카오톡 > 더보기 > 설정 > 테마 에서 선택
- iOS `build/ios/<테마-id>.ktheme` → AirDrop/메일로 보낸 뒤 카카오톡으로 열기

패키지명은 `com.kakao.talk.theme.<테마-id>` 로 자동 구성되므로 테마끼리 충돌하지 않고
한 기기에 여러 개를 같이 설치할 수 있습니다.

> Gradle wrapper 는 포함돼 있지 않습니다. Android Studio 로 `android/` 를 열면
> 자동 생성되고, CLI 만 쓴다면 `gradle wrapper` 를 한 번 실행하세요.
> 배포용 APK 는 `app/build.gradle` 의 release `signingConfig` 를 본인 키로 교체해야 합니다.

## 색을 새로 추가하고 싶다면

팔레트에 키를 하나 늘리려면 두 곳만 고칩니다.

1. `themes/_template/theme.json` 의 `colors` (검사 기준이 여기입니다)
2. 그 키를 쓸 곳 — `android/.../colors.xml` 의 `thm_*`, `ios/mapping.json`

기존 테마들에도 같은 키를 넣어야 `validate.py` 가 통과합니다.

## 확인이 필요한 부분

리소스 이름과 규격 값은 카카오톡 버전에 따라 바뀝니다. 뼈대는 관례를 따라 잡아뒀지만,
실제 적용 전에 **카카오 공식 테마 제작 가이드의 리소스 목록**과 대조하는 것을 권합니다.

- `android/.../colors.xml` 의 `thm_*` 목록 — 자주 쓰이는 항목만 담았습니다. 가이드에
  있는데 없는 이름은 추가하면 되고, 정의 안 한 이름은 기본값이 쓰여 앱이 깨지지는 않습니다.
- `AndroidManifest.xml` 의 `com.kakao.talk.theme.*` 메타데이터 키와
  `values/strings.xml` 의 `thm_theme_spec_version`(현재 `10`).
- `ios/mapping.json`·`images.json` 의 키 이름 — iOS `.ktheme` 내부 규격은 공개 문서가
  적어 적용해 보며 맞춰야 할 수 있습니다.

여기서 이름이 틀려도 오류는 안 나고 조용히 기본값이 나옵니다. 이름을 고칠 일이 생기면
공유 매핑 파일 한 곳만 고치면 모든 테마에 반영됩니다.
