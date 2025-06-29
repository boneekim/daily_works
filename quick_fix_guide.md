# 🚨 테이블 구조 즉시 수정 가이드

## 현재 상황
✅ 앱이 정상적으로 문제를 감지했습니다!
❌ daily_works 테이블에 'category' 컬럼이 없어서 데이터 추가 불가

## 🔧 즉시 해결 방법

### 1단계: Supabase SQL Editor 접속
1. **새 탭**에서 https://supabase.com 접속
2. 로그인 후 **daily-works 프로젝트** 선택
3. 왼쪽 메뉴에서 **SQL Editor** 클릭
4. **New query** 클릭

### 2단계: 테이블 재생성 SQL 실행
다음 SQL을 **전체 복사**해서 붙여넣고 **Run** 클릭:

```sql
-- 기존 테이블 삭제
DROP TABLE IF EXISTS daily_works;

-- 올바른 구조로 재생성
CREATE TABLE daily_works (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    category TEXT NOT NULL,
    link TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- RLS 비활성화
ALTER TABLE daily_works DISABLE ROW LEVEL SECURITY;

-- 테스트 데이터 추가
INSERT INTO daily_works (title, category, link) 
VALUES ('테스트 항목', '핫딜', 'https://example.com');

-- 확인
SELECT * FROM daily_works;
```

### 3단계: 성공 확인
- **Success** 메시지 확인
- 마지막 SELECT 결과에서 테스트 데이터 확인

### 4단계: Streamlit 앱 새로고침
- Streamlit 앱 탭으로 돌아가서 **새로고침** (F5)
- 또는 앱에서 아무 버튼이나 클릭

## ✅ 예상 결과

테이블 수정 후 Streamlit 앱에서:
1. **"🎁 데이터베이스가 비어있어서 샘플 데이터를 추가하고 있습니다..."** 메시지
2. **"✅ 42개의 샘플 데이터가 추가되었습니다!"** 성공 메시지
3. **카테고리별 통계 표시** (각 카테고리당 3개씩)
4. **새 항목 추가 정상 작동**

## 🚨 문제 해결 안 되면?

1. **SQL 실행 오류**: 
   - 명령어를 하나씩 따로 실행해보세요
   - 첫 번째 DROP 명령어부터 순서대로

2. **여전히 같은 오류**:
   - 브라우저 새로고침 (Ctrl+F5 또는 Cmd+Shift+R)
   - Streamlit 앱 완전 재시작

3. **다른 오류 발생**:
   - 오류 메시지를 정확히 알려주세요

## 💡 왜 이런 문제가 발생했나?

- Supabase에서 테이블을 처음 생성할 때 기본 구조만 만들어짐
- `title`, `category`, `link` 컬럼이 필요한데 일부만 생성됨
- 위의 SQL로 완전한 구조로 재생성하면 해결됨
