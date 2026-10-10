import AVFoundation
import Vision

/// 전면 카메라 프레임을 받아 Vision으로 손 관절을 찾고,
/// 손가락 끝 좌표(카메라 기준 0~1 정규화 좌표)를 넘겨주는 클래스.
final class HandTracker: NSObject, AVCaptureVideoDataOutputSampleBufferDelegate, @unchecked Sendable {

    /// 화면 미리보기(AVCaptureVideoPreviewLayer)와 공유하는 카메라 세션
    nonisolated(unsafe) let session = AVCaptureSession()

    /// 손가락 끝 좌표가 나올 때마다 메인 스레드에서 호출됨
    nonisolated(unsafe) var onTips: (@MainActor @Sendable ([CGPoint]) -> Void)?

    /// 카메라 설정과 프레임 처리를 담당하는 백그라운드 큐
    nonisolated let queue = DispatchQueue(label: "mallangi.hand.tracker")

    /// 손 관절 인식 요청 (최대 2손)
    nonisolated(unsafe) private let request: VNDetectHumanHandPoseRequest = {
        let r = VNDetectHumanHandPoseRequest()
        r.maximumHandCount = 2
        return r
    }()

    /// 원을 그릴 관절: 엄지·검지·중지·약지·소지 끝
    nonisolated(unsafe) private static let tipJoints: [VNHumanHandPoseObservation.JointName] = [
        .thumbTip, .indexTip, .middleTip, .ringTip, .littleTip
    ]

    /// 이 값보다 신뢰도가 낮은 점은 무시 (0~1)
    nonisolated(unsafe) var minConfidence: Float = 0.3

    // MARK: - 시작

    nonisolated func start() {
        queue.async {
            self.configureSession()
            self.session.startRunning()
        }
    }

    nonisolated private func configureSession() {
        session.beginConfiguration()
        defer { session.commitConfiguration() }

        session.sessionPreset = .high

        guard
            let device = AVCaptureDevice.default(.builtInWideAngleCamera, for: .video, position: .front),
            let input = try? AVCaptureDeviceInput(device: device),
            session.canAddInput(input)
        else {
            print("전면 카메라를 열 수 없음")
            return
        }
        session.addInput(input)

        let output = AVCaptureVideoDataOutput()
        output.alwaysDiscardsLateVideoFrames = true   // 처리 못 한 프레임은 버려 지연 누적 방지
        output.setSampleBufferDelegate(self, queue: queue)
        guard session.canAddOutput(output) else {
            print("비디오 출력을 추가할 수 없음")
            return
        }
        session.addOutput(output)
    }

    // MARK: - 프레임마다 호출

    nonisolated func captureOutput(_ output: AVCaptureOutput,
                                   didOutput sampleBuffer: CMSampleBuffer,
                                   from connection: AVCaptureConnection) {
        // 카메라 센서 원본 방향(.up) 그대로 분석 → 결과 좌표가 카메라 기준 좌표가 됨
        let handler = VNImageRequestHandler(cmSampleBuffer: sampleBuffer, orientation: .up, options: [:])
        do {
            try handler.perform([request])
        } catch {
            print("Vision 오류: \(error)")
            return
        }

        var tips: [CGPoint] = []
        for hand in request.results ?? [] {
            guard let points = try? hand.recognizedPoints(.all) else { continue }
            for joint in Self.tipJoints {
                guard let p = points[joint], p.confidence > minConfidence else { continue }
                // Vision은 왼쪽 아래가 원점 → 카메라 좌표(왼쪽 위 원점)로 y 뒤집기
                tips.append(CGPoint(x: p.location.x, y: 1 - p.location.y))
            }
        }

        let callback = onTips
        Task { @MainActor in callback?(tips) }
    }
}
