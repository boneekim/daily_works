-- daily_works 테이블에 컬럼 추가 SQL
-- 기존 테이블에 새로운 기능을 위한 컬럼들을 추가합니다

-- 1. 설명 컬럼 추가 (간단한 메모나 설명)
ALTER TABLE daily_works 
ADD COLUMN description TEXT DEFAULT '';

-- 2. 상태 컬럼 추가 (활성/비활성)
ALTER TABLE daily_works 
ADD COLUMN status TEXT DEFAULT 'active' 
CHECK (status IN ('active', 'inactive', 'expired'));

-- 3. 우선순위 컬럼 추가 (1=높음, 2=보통, 3=낮음)
ALTER TABLE daily_works 
ADD COLUMN priority INTEGER DEFAULT 2 
CHECK (priority IN (1, 2, 3));

-- 4. 즐겨찾기 컬럼 추가
ALTER TABLE daily_works 
ADD COLUMN is_favorite BOOLEAN DEFAULT false;

-- 5. 조회수 컬럼 추가 (링크 클릭 횟수)
ALTER TABLE daily_works 
ADD COLUMN view_count INTEGER DEFAULT 0;

-- 6. 수정일시 컬럼 추가
ALTER TABLE daily_works 
ADD COLUMN updated_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW());

-- 7. 만료일 컬럼 추가 (이벤트 종료일)
ALTER TABLE daily_works 
ADD COLUMN expiry_date DATE;

-- 8. 출처 컬럼 추가 (정보 출처)
ALTER TABLE daily_works 
ADD COLUMN source TEXT DEFAULT 'manual';

-- 9. 태그 컬럼 추가 (추가 분류용)
ALTER TABLE daily_works 
ADD COLUMN tags TEXT[] DEFAULT '{}';

-- 10. 업데이트 트리거 생성 (updated_at 자동 갱신)
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = TIMEZONE('utc'::text, NOW());
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_daily_works_updated_at 
    BEFORE UPDATE ON daily_works 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

-- 11. 새로운 컬럼들에 대한 인덱스 생성
CREATE INDEX idx_daily_works_status ON daily_works(status);
CREATE INDEX idx_daily_works_priority ON daily_works(priority);
CREATE INDEX idx_daily_works_is_favorite ON daily_works(is_favorite);
CREATE INDEX idx_daily_works_expiry_date ON daily_works(expiry_date);
CREATE INDEX idx_daily_works_updated_at ON daily_works(updated_at DESC);

-- 12. 기존 데이터 업데이트 (예시)
UPDATE daily_works 
SET 
    description = '기존 데이터',
    source = 'legacy',
    updated_at = created_at
WHERE description IS NULL OR description = '';

-- 13. 테이블 구조 확인
SELECT 
    column_name, 
    data_type, 
    is_nullable, 
    column_default
FROM information_schema.columns 
WHERE table_name = 'daily_works' 
ORDER BY ordinal_position;

-- 14. 샘플 데이터 추가 (새로운 컬럼 포함)
INSERT INTO daily_works (
    title, 
    category, 
    link, 
    description, 
    priority, 
    is_favorite, 
    expiry_date, 
    source,
    tags
) VALUES
(
    '신상품 무료 체험단 모집', 
    '체험단', 
    'https://example.com/new-product', 
    '신제품 사용 후 리뷰 작성하면 제품 증정',
    1,
    true,
    '2024-07-31',
    'instagram',
    '{"신제품", "무료", "체험"}'
),
(
    '온라인 투자 강의 할인', 
    '재태크', 
    'https://example.com/investment', 
    '주식 투자 기초부터 고급까지 90% 할인',
    2,
    false,
    '2024-08-15',
    'email',
    '{"할인", "투자", "강의"}'
);
