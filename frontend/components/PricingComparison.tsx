export function PricingComparison() {
  return (
    <section className="py-20 px-8 bg-gradient-to-b from-gray-50 to-white">
      <div className="max-w-5xl mx-auto">
        <h2 className="text-4xl font-bold text-center text-gray-900 mb-16">
          기능 비교
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {/* 무료 기능 */}
          <div className="p-8 bg-white rounded-2xl shadow-lg border-2 border-blue-500">
            <div className="inline-block px-4 py-2 bg-blue-500 text-white rounded-full text-sm font-semibold mb-4">
              무료
            </div>
            <h3 className="text-2xl font-bold text-gray-900 mb-6">
              기본 기능
            </h3>
            <ul className="space-y-4">
              <li className="flex items-start">
                <span className="text-green-500 mr-3 text-xl">✓</span>
                <span className="text-gray-700">10초 세로형 영상 생성</span>
              </li>
              <li className="flex items-start">
                <span className="text-green-500 mr-3 text-xl">✓</span>
                <span className="text-gray-700">OG 이미지 자동 추출</span>
              </li>
              <li className="flex items-start">
                <span className="text-green-500 mr-3 text-xl">✓</span>
                <span className="text-gray-700">기본 자막 오버레이</span>
              </li>
              <li className="flex items-start">
                <span className="text-green-500 mr-3 text-xl">✓</span>
                <span className="text-gray-700">1080x1920 해상도</span>
              </li>
            </ul>
          </div>

          {/* 확장 기능 (미래) */}
          <div className="p-8 bg-gray-50 rounded-2xl shadow-lg border-2 border-gray-200 opacity-75">
            <div className="inline-block px-4 py-2 bg-purple-500 text-white rounded-full text-sm font-semibold mb-4">
              확장 기능 (예정)
            </div>
            <h3 className="text-2xl font-bold text-gray-900 mb-6">
              프리미엄 기능
            </h3>
            <ul className="space-y-4">
              <li className="flex items-start">
                <span className="text-purple-500 mr-3 text-xl">★</span>
                <span className="text-gray-600">다중 이미지 슬라이드</span>
              </li>
              <li className="flex items-start">
                <span className="text-purple-500 mr-3 text-xl">★</span>
                <span className="text-gray-600">커스텀 폰트 선택</span>
              </li>
              <li className="flex items-start">
                <span className="text-purple-500 mr-3 text-xl">★</span>
                <span className="text-gray-600">AI 음성 나레이션</span>
              </li>
              <li className="flex items-start">
                <span className="text-purple-500 mr-3 text-xl">★</span>
                <span className="text-gray-600">브랜드 워터마크</span>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </section>
  );
}
