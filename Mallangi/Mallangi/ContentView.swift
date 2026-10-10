import SwiftUI

struct ContentView: View {
    var body: some View {
        HandCameraView()
            .ignoresSafeArea()
    }
}

/// UIKit 화면(HandCameraViewController)을 SwiftUI에서 쓰기 위한 연결 코드
struct HandCameraView: UIViewControllerRepresentable {
    func makeUIViewController(context: Context) -> HandCameraViewController {
        HandCameraViewController()
    }

    func updateUIViewController(_ uiViewController: HandCameraViewController, context: Context) {}
}

#Preview {
    ContentView()
}
