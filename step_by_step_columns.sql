-- daily_works 테이블에 컬럼을 하나씩 추가하는 SQL
-- Supabase SQL Editor에서 한 줄씩 실행하세요

-- 1단계: 설명 컬럼 추가
ALTER TABLE daily_works ADD COLUMN description TEXT DEFAULT '';

-- 2단계: 상태 컬럼 추가 (활성/비활성/만료)
ALTER TABLE daily_works ADD COLUMN status TEXT DEFAULT 'active';
ALTER TABLE daily_works ADD CONSTRAINT check_status CHECK (status IN ('active', 'inactive', 'expired'));

-- 3단계: 우선순위 컬럼 추가 (1=높음, 2=보통, 3=낮음)
ALTER TABLE daily_works ADD COLUMN priority INTEGER DEFAULT 2;
ALTER TABLE daily_works ADD CONSTRAINT check_priority CHECK (priority IN (1, 2, 3));

-- 4단계: 즐겨찾기 컬럼 추가
ALTER TABLE daily_works ADD COLUMN is_favorite BOOLEAN DEFAULT false;

-- 5단계: 조회수 컬럼 추가
ALTER TABLE daily_works ADD COLUMN view_count INTEGER DEFAULT 0;

-- 6단계: 수정일시 컬럼 추가
ALTER TABLE daily_works ADD COLUMN updated_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW());

-- 7단계: 만료일 컬럼 추가
ALTER TABLE daily_works ADD COLUMN expiry_date DATE;

-- 8단계: 출처 컬럼 추가
ALTER TABLE daily_works ADD COLUMN source TEXT DEFAULT 'manual';

-- 9단계: 태그 컬럼 추가 (배열 형태)
ALTER TABLE daily_works ADD COLUMN tags TEXT[] DEFAULT '{}';

-- 10단계: 수정일시 자동 업데이트 함수 생성
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = TIMEZONE('utc'::text, NOW());
    RETURN NEW;
END;
$$ language 'plpgsql';

-- 11단계: 트리거 생성
CREATE TRIGGER update_daily_works_updated_at 
    BEFORE UPDATE ON daily_works 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

-- 12단계: 성능을 위한 인덱스 생성
CREATE INDEX idx_daily_works_status ON daily_works(status);
CREATE INDEX idx_daily_works_priority ON daily_works(priority);
CREATE INDEX idx_daily_works_is_favorite ON daily_works(is_favorite);
CREATE INDEX idx_daily_works_expiry_date ON daily_works(expiry_date);
CREATE INDEX idx_daily_works_updated_at ON daily_works(updated_at DESC);

-- 13단계: 기존 데이터 업데이트
UPDATE daily_works SET updated_at = created_at WHERE updated_at IS NULL;

-- 14단계: 테이블 구조 확인
SELECT column_name, data_type, is_nullable, column_default 
FROM information_schema.columns 
WHERE table_name = 'daily_works' 
ORDER BY ordinal_position;
