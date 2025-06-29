-- daily_works 테이블 구조 확인 및 수정
-- Supabase SQL Editor에서 단계별로 실행하세요

-- 1단계: 현재 테이블 구조 확인
SELECT column_name, data_type, is_nullable, column_default 
FROM information_schema.columns 
WHERE table_name = 'daily_works' 
ORDER BY ordinal_position;

-- 2단계: 기존 테이블 삭제 후 새로 생성 (추천)
DROP TABLE IF EXISTS daily_works;

-- 3단계: 올바른 구조로 테이블 재생성
CREATE TABLE daily_works (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    category TEXT NOT NULL,
    link TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL
);

-- 4단계: RLS 비활성화 (중요!)
ALTER TABLE daily_works DISABLE ROW LEVEL SECURITY;

-- 5단계: 인덱스 생성 (성능 향상)
CREATE INDEX idx_daily_works_category ON daily_works(category);
CREATE INDEX idx_daily_works_created_at ON daily_works(created_at DESC);

-- 6단계: 테이블 구조 재확인
SELECT column_name, data_type, is_nullable, column_default 
FROM information_schema.columns 
WHERE table_name = 'daily_works' 
ORDER BY ordinal_position;

-- 7단계: 테스트 데이터 1개 추가
INSERT INTO daily_works (title, category, link) 
VALUES ('테스트 항목', '핫딜', 'https://example.com');

-- 8단계: 데이터 확인
SELECT * FROM daily_works;
