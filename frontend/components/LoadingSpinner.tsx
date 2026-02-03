export function LoadingSpinner() {
  return (
    <div className="flex flex-col items-center justify-center space-y-4 py-8">
      <div className="relative">
        <div className="animate-spin rounded-full h-20 w-20 border-b-4 border-blue-500"></div>
        <div className="absolute top-0 left-0 animate-ping rounded-full h-20 w-20 border-2 border-blue-300 opacity-20"></div>
      </div>
      <div className="text-center space-y-2">
        <p className="text-gray-700 text-xl font-semibold">영상 생성 중...</p>
        <p className="text-gray-500 text-base">20초 영상을 만들고 있습니다</p>
        <p className="text-gray-400 text-sm">약 40-60초 정도 소요됩니다</p>
      </div>
      <div className="mt-4 w-64 bg-gray-200 rounded-full h-2">
        <div className="bg-blue-500 h-2 rounded-full animate-pulse" style={{width: '60%'}}></div>
      </div>
    </div>
  );
}
