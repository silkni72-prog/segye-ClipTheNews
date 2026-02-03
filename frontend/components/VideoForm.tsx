'use client';

import { useState } from 'react';
import { LoadingSpinner } from './LoadingSpinner';

type Status = 'idle' | 'loading' | 'success' | 'error';

interface VideoResponse {
  video_url: string;
  message: string;
}

export function VideoForm() {
  const [newsUrl, setNewsUrl] = useState('');
  const [scenario, setScenario] = useState('');
  const [status, setStatus] = useState<Status>('idle');
  const [videoUrl, setVideoUrl] = useState('');
  const [errorMessage, setErrorMessage] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!newsUrl) {
      setErrorMessage('뉴스 URL을 입력해주세요.');
      return;
    }

    setStatus('loading');
    setErrorMessage('');
    setVideoUrl('');

    try {
      const response = await fetch('/api/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          news_url: newsUrl,
          scenario: scenario,
        }),
      });

      const data: VideoResponse = await response.json();

      if (!response.ok) {
        throw new Error(data.message || '영상 생성에 실패했습니다.');
      }

      setStatus('success');
      setVideoUrl(data.video_url);
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
    setScenario('');
    setVideoUrl('');
    setErrorMessage('');
  };

  return (
    <div className="w-full max-w-3xl mx-auto p-8">
      <div className="bg-white rounded-2xl shadow-xl p-8 border border-gray-100">
        <h2 className="text-3xl font-bold text-gray-900 mb-8 text-center">
          영상 생성하기
        </h2>

        {status === 'loading' && <LoadingSpinner />}

        {status === 'success' && (
          <div className="text-center space-y-6">
            <div className="p-6 bg-green-50 rounded-xl border border-green-200">
              <p className="text-green-800 text-lg font-semibold mb-2">
                ✓ 영상이 성공적으로 생성되었습니다!
              </p>
              <p className="text-green-600 text-sm">
                아래 버튼을 클릭하여 영상을 다운로드하세요.
              </p>
            </div>
            <a
              href={`http://localhost:8000${videoUrl}`}
              download
              className="inline-block px-8 py-4 bg-gradient-to-r from-blue-500 to-purple-600 text-white rounded-xl text-lg font-semibold hover:shadow-xl transition-all duration-200"
            >
              영상 다운로드
            </a>
            <button
              onClick={handleReset}
              className="block w-full mt-4 px-6 py-3 bg-gray-100 text-gray-700 rounded-lg font-medium hover:bg-gray-200 transition-colors"
            >
              새로운 영상 만들기
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
                htmlFor="scenario"
                className="block text-sm font-semibold text-gray-700 mb-2"
              >
                시나리오 <span className="text-gray-400 text-xs font-normal">(선택사항)</span>
              </label>
              <textarea
                id="scenario"
                value={scenario}
                onChange={(e) => setScenario(e.target.value)}
                placeholder="비워두면 뉴스 제목 기반으로 자동 생성됩니다"
                maxLength={300}
                rows={4}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all resize-none"
              />
              <div className="mt-2 flex justify-between items-center">
                <p className="text-sm text-gray-500">
                  💡 비워두면 자동으로 생성됩니다
                </p>
                <p className="text-sm text-gray-400">
                  {scenario.length}/300
                </p>
              </div>
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
