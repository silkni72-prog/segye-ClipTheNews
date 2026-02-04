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

        {status === 'loading' && <LoadingSpinner />}

        {status === 'success' && result && (
          <div className="space-y-6">
            <div className="p-6 bg-green-50 rounded-xl border border-green-200">
              <p className="text-green-800 text-lg font-semibold mb-2">
                ✓ {result.message}
              </p>
            </div>

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
