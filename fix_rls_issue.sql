-- daily_works 테이블 RLS 문제 해결 SQL
-- Supabase SQL Editor에서 실행하세요

-- 방법 1: RLS 비활성화 (개발/테스트용 - 추천)
ALTER TABLE daily_works DISABLE ROW LEVEL SECURITY;

-- 방법 2: RLS 유지하면서 모든 접근 허용 정책 생성 (대안)
-- 위 방법이 안 되면 이것을 사용하세요

-- 기존 정책 삭제 (있다면)
DROP POLICY IF EXISTS "Allow all operations" ON daily_works;

-- RLS 활성화 (이미 되어있을 수 있음)
ALTER TABLE daily_works ENABLE ROW LEVEL SECURITY;

-- 모든 작업을 허용하는 정책 생성
CREATE POLICY "Enable all operations for all users" ON daily_works
    FOR ALL 
    USING (true)
    WITH CHECK (true);

-- 확인: 테이블의 RLS 상태 체크
SELECT schemaname, tablename, rowsecurity 
FROM pg_tables 
WHERE tablename = 'daily_works';

-- 확인: 현재 정책 목록 보기
SELECT * FROM pg_policies WHERE tablename = 'daily_works';
