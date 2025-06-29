-- 기존 데이터 모두 삭제 및 노션 데이터 가져오기
-- Supabase SQL Editor에서 실행하세요

-- 1단계: 기존 데이터 모두 삭제
DELETE FROM daily_works;

-- 2단계: AUTO INCREMENT 리셋 (ID를 1부터 다시 시작)
ALTER SEQUENCE daily_works_id_seq RESTART WITH 1;

-- 3단계: 데이터 삭제 확인
SELECT COUNT(*) as "삭제후_데이터_개수" FROM daily_works;

-- 4단계: 노션 데이터 삽입 (사용자가 제공한 실제 데이터로 교체 예정)
-- 예시 형식:
-- INSERT INTO daily_works (title, category, link) VALUES
-- ('실제 노션 제목1', '핫딜', 'https://실제링크1.com'),
-- ('실제 노션 제목2', '체험단', 'https://실제링크2.com');

-- 임시 확인용 데이터 (실제 노션 데이터로 교체 필요)
INSERT INTO daily_works (title, category, link) VALUES
('임시 데이터 - 노션 데이터로 교체 예정', '핫딜', 'https://example.com');

-- 5단계: 삽입 결과 확인
SELECT * FROM daily_works ORDER BY id;
