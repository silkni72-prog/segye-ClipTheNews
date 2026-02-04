export function Features() {
  const features = [
    {
      icon: "⚡",
      title: "10초 완성",
      description: "URL 입력 후 자동으로 영상이 생성됩니다"
    },
    {
      icon: "📱",
      title: "세로형 최적화",
      description: "9:16 비율로 소셜 미디어에 완벽 대응"
    },
    {
      icon: "💬",
      title: "자막 자동",
      description: "시나리오 기반 자막을 자동으로 오버레이"
    }
  ];

  return (
    <section className="py-20 px-8 bg-white">
      <div className="max-w-6xl mx-auto">
        <h2 className="text-4xl font-bold text-center text-gray-900 mb-16">
          주요 기능
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {features.map((feature, idx) => (
            <div
              key={idx}
              className="p-8 bg-white rounded-2xl shadow-lg hover:shadow-xl transition-shadow duration-200 border border-gray-100"
            >
              <div className="text-5xl mb-4">{feature.icon}</div>
              <h3 className="text-xl font-semibold text-gray-900 mb-3">
                {feature.title}
              </h3>
              <p className="text-gray-600 leading-relaxed">
                {feature.description}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
