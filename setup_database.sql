-- Daily Works 데이터베이스 설정 스크립트
-- Supabase SQL Editor에서 실행하세요

-- 1. daily_works 테이블 생성
CREATE TABLE daily_works (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    category TEXT NOT NULL,
    link TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL
);

-- 2. 카테고리 제약 조건 추가 (선택사항)
ALTER TABLE daily_works 
ADD CONSTRAINT valid_category 
CHECK (category IN (
    '핫딜', '체험단', '재태크', '매일읽기', '전시,문화', 
    '방송', '시사회', '온라인 강의,공부', '세미나', '회사 혜택', 
    '책관련', '웹진(무료)', '감성블로그', '생활편의'
));

-- 3. RLS (Row Level Security) 활성화
ALTER TABLE daily_works ENABLE ROW LEVEL SECURITY;

-- 4. 모든 사용자가 읽고 쓸 수 있도록 정책 생성 (개발용)
CREATE POLICY "Allow all operations" ON daily_works FOR ALL USING (true);

-- 5. 인덱스 생성 (성능 향상)
CREATE INDEX idx_daily_works_category ON daily_works(category);
CREATE INDEX idx_daily_works_created_at ON daily_works(created_at DESC);
CREATE INDEX idx_daily_works_title ON daily_works(title);

-- 6. 샘플 데이터 삽입 (테스트용)
INSERT INTO daily_works (title, category, link) VALUES
('네이버 쇼핑 핫딜', '핫딜', 'https://shopping.naver.com'),
('신제품 체험단 모집', '체험단', 'https://example.com/review'),
('무료 온라인 강의', '온라인 강의,공부', 'https://example.com/course'),
('전시회 무료 관람', '전시,문화', 'https://example.com/exhibition'),
('도서 리뷰 이벤트', '책관련', 'https://example.com/book');

-- 7. 테이블 정보 확인
SELECT 
    column_name, 
    data_type, 
    is_nullable, 
    column_default
FROM information_schema.columns 
WHERE table_name = 'daily_works' 
ORDER BY ordinal_position;
