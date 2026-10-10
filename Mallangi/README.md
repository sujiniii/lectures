# Mallangi — 손가락 끝 추적 데모 (iOS)

전면 카메라 화면에서 손가락 끝마다 분홍색 원을 그리는 데모입니다. (Vision `VNDetectHumanHandPoseRequest`, 최대 2손)

## 구성

| 파일 | 역할 |
|---|---|
| `Mallangi/HandTracker.swift` | 카메라 프레임 → Vision → 손가락 끝 좌표 |
| `Mallangi/HandCameraViewController.swift` | 카메라 미리보기 + 원 그리기 |
| `Mallangi/ContentView.swift` | SwiftUI 연결 |
| `Mallangi/MallangiApp.swift` | 앱 진입점 |
| `Mallangi.xcodeproj` | Xcode 프로젝트 (카메라 권한 문구, 세로 고정, Bundle ID `com.sujin.mallangi` 설정 완료) |

## 실행 (Mac, Xcode 16 이상)

1. 이 폴더의 `Mallangi.xcodeproj`를 더블클릭해서 열기
2. **TARGETS → Mallangi → Signing & Capabilities → Team**에서 내 Apple ID의 *(Personal Team)* 선택
   - Bundle ID가 이미 사용 중이라고 나오면 `com.sujin.mallangi2`처럼 바꾸기
3. 아이폰 연결 → '이 컴퓨터 신뢰' → 설정 › 개인정보 보호 및 보안 › **개발자 모드** 켜기
4. 상단 실행 기기를 내 아이폰으로 고르고 **▶ (⌘R)**
5. 처음엔 "신뢰하지 않는 개발자" 경고 → 설정 › 일반 › **VPN 및 기기 관리**에서 신뢰 후 다시 실행

## 막힐 때

- 원이 자주 사라짐: `HandTracker.swift`의 `minConfidence`를 `0.3` → `0.2`
- 무료 Apple ID로 설치한 앱은 7일 후 만료 → Xcode에서 다시 실행
