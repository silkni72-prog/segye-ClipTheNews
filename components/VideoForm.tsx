'use client';

import { useState } from 'react';
import { LoadingSpinner } from './LoadingSpinner';

type Status = 'idle' | 'loading' | 'success' | 'error';
type VideoMode = 'nyt_question' | 'guardian_observe';

interface VideoResponse {
  video_url?: string;
  message: string;
  script?: string;
  title?: string;
  summary?: string;
  job_id?: string;
  status?: string;
  progress?: number;
}

export function VideoForm() {
  const [newsUrl, setNewsUrl] = useState('');
  const [mode, setMode] = useState<VideoMode>('nyt_question');
  const [status, setStatus] = useState<Status>('idle');
  const [result, setResult] = useState<VideoResponse | null>(null);
  const [errorMessage, setErrorMessage] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!newsUrl) {
      setErrorMessage('뉴스 URL을 입력해주세요.');
      return;
    }

    setStatus('loading');
    setErrorMessage('');
    setResult(null);

    try {
      const response = await fetch('/api/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          news_url: newsUrl,
          mode: mode,
        }),
      });

      const data: VideoResponse = await response.json();

      if (!response.ok) {
        throw new Error(data.message || '처리에 실패했습니다.');
      }

      setStatus('success');
      setResult(data);
    } catch (error) {
      setStatus('error');
      setErrorMessage(
        error instanceof Error ? error.message : '영상 생성 중 오류가 발생했습니다.'
      );
    }
  };

  const handleReset = () => {
    setStatus('idle');
    setNewsUrl('');
    setMode('nyt_question');
    setResult(null);
    setErrorMessage('');
  };

  return (
    <div className="w-full max-w-3xl mx-auto p-8">
      <div className="bg-white rounded-2xl shadow-xl p-8 border border-gray-100">
        <h2 className="text-3xl font-bold text-gray-900 mb-8 text-center">
          영상 생성하기
        </h2>

        {status === 'loading' && (
          <div className="space-y-6">
            <LoadingSpinner />
            <div className="text-center space-y-2">
              <p className="text-gray-700 font-medium">영상을 생성하는 중입니다...</p>
              <p className="text-gray-500 text-sm">이 작업은 30~60초 정도 소요됩니다.</p>
              <div className="flex justify-center items-center gap-2 text-sm text-gray-600 mt-4">
                <div className="flex items-center gap-1">
                  <span className="inline-block w-2 h-2 bg-blue-500 rounded-full animate-pulse"></span>
                  <span>기사 파싱</span>
                </div>
                <span>→</span>
                <div className="flex items-center gap-1">
                  <span className="inline-block w-2 h-2 bg-purple-500 rounded-full animate-pulse"></span>
                  <span>스크립트 생성</span>
                </div>
                <span>→</span>
                <div className="flex items-center gap-1">
                  <span className="inline-block w-2 h-2 bg-green-500 rounded-full animate-pulse"></span>
                  <span>영상 렌더링</span>
                </div>
              </div>
            </div>
          </div>
        )}

        {status === 'success' && result && (
          <div className="space-y-6">
            <div className="p-6 bg-green-50 rounded-xl border border-green-200">
              <p className="text-green-800 text-lg font-semibold mb-2">
                ✓ {result.message}
              </p>
            </div>

            {result.video_url && (
              <div className="space-y-4">
                <h3 className="font-semibold text-gray-900 text-lg">🎬 생성된 영상</h3>
                <div className="relative rounded-xl overflow-hidden shadow-2xl bg-black">
                  <video 
                    controls 
                    className="w-full"
                    style={{ maxHeight: '600px' }}
                  >
                    <source src={result.video_url} type="video/mp4" />
                    브라우저가 비디오 태그를 지원하지 않습니다.
                  </video>
                </div>
                <a
                  href={result.video_url}
                  download
                  className="inline-flex items-center gap-2 px-4 py-2 bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-lg transition-colors text-sm font-medium"
                >
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                  </svg>
                  영상 다운로드
                </a>
              </div>
            )}

            {result.title && (
              <div className="p-4 bg-blue-50 rounded-lg">
                <h3 className="font-semibold text-blue-900 mb-2">📰 기사 제목</h3>
                <p className="text-blue-800 text-sm">{result.title}</p>
              </div>
            )}

            {result.script && (
              <div className="p-4 bg-purple-50 rounded-lg">
                <h3 className="font-semibold text-purple-900 mb-2">📝 생성된 스크립트</h3>
                <p className="text-purple-800 text-sm leading-relaxed">{result.script}</p>
              </div>
            )}

            {result.summary && (
              <div className="p-4 bg-gray-50 rounded-lg">
                <h3 className="font-semibold text-gray-900 mb-2">📋 요약</h3>
                <p className="text-gray-700 text-sm">{result.summary}</p>
              </div>
            )}

            <button
              onClick={handleReset}
              className="w-full px-6 py-3 bg-gradient-to-r from-blue-500 to-purple-600 text-white rounded-lg font-medium hover:shadow-xl transition-all"
            >
              새로운 뉴스 분석하기
            </button>
          </div>
        )}

        {status === 'error' && (
          <div className="space-y-6">
            <div className="p-6 bg-red-50 rounded-xl border border-red-200">
              <p className="text-red-800 text-lg font-semibold mb-2">
                ✗ 오류가 발생했습니다
              </p>
              <p className="text-red-600 text-sm">{errorMessage}</p>
            </div>
            <button
              onClick={handleReset}
              className="w-full px-6 py-3 bg-gray-100 text-gray-700 rounded-lg font-medium hover:bg-gray-200 transition-colors"
            >
              다시 시도하기
            </button>
          </div>
        )}

        {(status === 'idle' || status === 'error') && (
          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label
                htmlFor="newsUrl"
                className="block text-sm font-semibold text-gray-700 mb-2"
              >
                뉴스 URL
              </label>
              <input
                type="url"
                id="newsUrl"
                value={newsUrl}
                onChange={(e) => setNewsUrl(e.target.value)}
                placeholder="https://example.com/news/article"
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all"
                required
              />
              <p className="mt-2 text-sm text-gray-500">
                뉴스 기사의 URL을 입력하세요
              </p>
            </div>

            <div>
              <label
                htmlFor="mode"
                className="block text-sm font-semibold text-gray-700 mb-2"
              >
                영상 스타일
              </label>
              <select
                id="mode"
                value={mode}
                onChange={(e) => setMode(e.target.value as VideoMode)}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all bg-white"
              >
                <option value="nyt_question">질문형 (NYT 스타일) - 호기심을 자극하는 질문으로 시작</option>
                <option value="guardian_observe">관찰형 (Guardian 스타일) - 분석적이고 차분한 톤</option>
              </select>
              <p className="mt-2 text-sm text-gray-500">
                💡 뉴스 기사를 바탕으로 20초 스크립트를 자동 생성합니다
              </p>
            </div>

            <button
              type="submit"
              disabled={false}
              className="w-full px-8 py-4 bg-gradient-to-r from-blue-500 to-purple-600 text-white rounded-xl text-lg font-semibold hover:shadow-xl hover:scale-[1.02] transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100"
            >
              영상 생성하기
            </button>
          </form>
        )}
      </div>
    </div>
  );
}
