import UIKit
import AVFoundation

/// 전면 카메라 화면을 보여주고, 손가락 끝마다 작은 원을 그리는 화면.
final class HandCameraViewController: UIViewController {

    private let tracker = HandTracker()
    private var previewLayer: AVCaptureVideoPreviewLayer!
    private let overlay = CAShapeLayer()

    /// 손가락 끝 원의 반지름 (pt)
    private let dotRadius: CGFloat = 10

    override func viewDidLoad() {
        super.viewDidLoad()
        view.backgroundColor = .black

        // 1) 카메라 미리보기
        previewLayer = AVCaptureVideoPreviewLayer(session: tracker.session)
        previewLayer.videoGravity = .resizeAspectFill
        view.layer.addSublayer(previewLayer)

        // 2) 원을 그릴 투명 레이어 (미리보기 위에 겹침)
        overlay.fillColor = UIColor.systemPink.cgColor
        overlay.strokeColor = UIColor.white.cgColor
        overlay.lineWidth = 2
        view.layer.addSublayer(overlay)

        // 3) 손가락 끝 좌표가 오면 원 다시 그리기
        tracker.onTips = { [weak self] tips in
            self?.drawTips(tips)
        }

        // 4) 카메라 권한 확인 후 시작
        startIfAuthorized()
    }

    override func viewDidLayoutSubviews() {
        super.viewDidLayoutSubviews()
        previewLayer.frame = view.bounds
        overlay.frame = view.bounds
    }

    private func startIfAuthorized() {
        let tracker = self.tracker
        switch AVCaptureDevice.authorizationStatus(for: .video) {
        case .authorized:
            tracker.start()
        case .notDetermined:
            AVCaptureDevice.requestAccess(for: .video) { granted in
                if granted { tracker.start() }
            }
        default:
            print("카메라 권한이 거부됨: 설정 > 개인정보 보호 > 카메라에서 허용 필요")
        }
    }

    /// 카메라 기준 정규화 좌표(0~1) → 화면 좌표로 바꿔 원을 그림.
    /// layerPointConverted가 화면 회전·전면 카메라 좌우 반전·화면 잘림(aspectFill)을 함께 처리함.
    private func drawTips(_ normalizedTips: [CGPoint]) {
        let path = UIBezierPath()
        for np in normalizedTips {
            let p = previewLayer.layerPointConverted(fromCaptureDevicePoint: np)
            path.append(UIBezierPath(arcCenter: p, radius: dotRadius,
                                     startAngle: 0, endAngle: .pi * 2, clockwise: true))
        }
        CATransaction.begin()
        CATransaction.setDisableActions(true)   // 원이 미끄러지는 기본 애니메이션 끄기
        overlay.path = path.cgPath
        CATransaction.commit()
    }
}
