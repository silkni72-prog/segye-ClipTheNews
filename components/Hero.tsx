import Link from 'next/link';

export function Hero() {
  return (
    <section className="py-20 px-8 bg-gradient-to-b from-white to-gray-50">
      <div className="max-w-4xl mx-auto text-center">
        <h1 className="text-5xl md:text-6xl font-bold text-gray-900 mb-6">
          뉴스를 10초 세로 영상으로
        </h1>
        <p className="text-xl md:text-2xl text-gray-600 mb-10 max-w-2xl mx-auto">
          URL 입력만으로 소셜 미디어용 뉴스 영상을 자동 생성하세요
        </p>
        <Link href="/generate">
          <button className="px-10 py-5 bg-gradient-to-r from-blue-500 to-purple-600 text-white rounded-xl text-lg font-semibold hover:shadow-2xl hover:scale-105 transition-all duration-200">
            지금 시작하기
          </button>
        </Link>
      </div>
    </section>
  );
}
