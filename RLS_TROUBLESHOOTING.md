# 🛡️ RLS (Row Level Security) 문제 해결 가이드

## 🚨 현재 문제
daily_works 테이블에서 RLS가 활성화되어 있어 데이터 접근이 차단되고 있습니다.

## ⚡ 빠른 해결 방법 (추천)

### 1️⃣ Supabase SQL Editor 접속
1. **https://supabase.com** → 프로젝트 선택
2. 왼쪽 메뉴에서 **SQL Editor** 클릭  
3. **New query** 클릭

### 2️⃣ RLS 비활성화 명령어 실행
```sql
ALTER TABLE daily_works DISABLE ROW LEVEL SECURITY;
```

### 3️⃣ 실행 확인
**Run** 버튼 클릭 후 성공 메시지 확인

### 4️⃣ 확인 (선택사항)
```sql
SELECT schemaname, tablename, rowsecurity 
FROM pg_tables 
WHERE tablename = 'daily_works';
```
결과에서 `rowsecurity`가 `f` (false)로 나오면 성공!

## 🔧 대안 방법 (RLS 유지하면서 해결)

RLS를 유지하고 싶다면:

```sql
-- 모든 작업 허용 정책 생성
CREATE POLICY "Enable all operations for all users" ON daily_works
    FOR ALL 
    USING (true)
    WITH CHECK (true);
```

## ✅ 해결 후 예상 결과

RLS 비활성화 후 Streamlit 앱에서:
- ✅ 새 항목 추가 가능
- ✅ 기존 데이터 조회 가능
- ✅ 검색 및 필터링 정상 작동
- ✅ 모든 CRUD 작업 가능

## 🤔 RLS란?

**Row Level Security (RLS)**:
- PostgreSQL의 보안 기능
- 테이블의 행(row) 단위로 접근 제어
- 정책(Policy)이 없으면 데이터 접근 불가
- Supabase는 기본적으로 RLS 활성화

## 💡 언제 RLS를 사용해야 할까?

**RLS 비활성화 (추천):**
- 개인 프로젝트
- 테스트/개발 환경
- 단순한 CRUD 앱

**RLS 활성화 (고급):**
- 다중 사용자 시스템
- 사용자별 데이터 분리 필요
- 엄격한 보안 요구사항

## 🚨 문제 해결 안 되면?

1. **테이블 이름 확인**: `daily_works`가 정확한지 확인
2. **권한 확인**: Supabase 프로젝트 소유자인지 확인
3. **새로고침**: 브라우저 새로고침 후 다시 시도
4. **재접속**: Supabase에서 로그아웃 후 다시 로그인
