# 📝 노션 데이터를 데이터베이스로 가져오기 가이드

## 🗑️ 1단계: 기존 데이터 삭제

먼저 Supabase에서 기존 데이터를 모두 삭제하겠습니다.

**Supabase SQL Editor**에서 다음 실행:
```sql
-- 기존 데이터 모두 삭제
DELETE FROM daily_works;

-- ID 카운터 리셋
ALTER SEQUENCE daily_works_id_seq RESTART WITH 1;

-- 삭제 확인
SELECT COUNT(*) FROM daily_works;
```

## 📋 2단계: 노션 데이터 확인

노션의 **"개인 > 데일리 실천 체험단"** 페이지에서 다음 정보를 확인해주세요:

1. **제목** (각 항목의 제목)
2. **카테고리** (아래 15개 중 하나)
3. **링크** (실제 URL)

### 지원하는 카테고리:
1. 핫딜
2. 체험단  
3. 재태크
4. 매일읽기
5. 전시,문화
6. 방송
7. 시사회
8. 온라인 강의,공부
9. 세미나
10. 회사 혜택
11. 책관련
12. 웹진(무료)
13. 감성블로그
14. 생활편의

## 📤 3단계: 데이터 제공 방법

다음 중 편한 방법을 선택해주세요:

### 방법 A: 텍스트로 제공
```
제목: 네이버 쇼핑 특가
카테고리: 핫딜
링크: https://shopping.naver.com

제목: 올리브영 체험단
카테고리: 체험단
링크: https://oliveyoung.co.kr
```

### 방법 B: 표 형식으로 제공
| 제목 | 카테고리 | 링크 |
|------|----------|------|
| 네이버 쇼핑 특가 | 핫딜 | https://shopping.naver.com |
| 올리브영 체험단 | 체험단 | https://oliveyoung.co.kr |

### 방법 C: CSV 형식으로 제공
```
제목,카테고리,링크
네이버 쇼핑 특가,핫딜,https://shopping.naver.com
올리브영 체험단,체험단,https://oliveyoung.co.kr
```

## 🔄 4단계: SQL 변환

데이터를 제공해주시면 다음과 같은 SQL로 변환해드립니다:

```sql
INSERT INTO daily_works (title, category, link) VALUES
('네이버 쇼핑 특가', '핫딜', 'https://shopping.naver.com'),
('올리브영 체험단', '체험단', 'https://oliveyoung.co.kr'),
('더 많은 데이터...', '카테고리', 'https://링크.com');
```

## 🚀 5단계: 데이터베이스 적용

생성된 SQL을 Supabase에서 실행하여 노션 데이터를 데이터베이스에 추가합니다.

## 💡 참고사항

- 한 번에 많은 데이터를 처리할 수 있습니다
- 링크 URL 형식을 자동으로 검증합니다
- 카테고리가 15개 목록에 없으면 자동으로 매칭해드립니다
- 중복 데이터는 자동으로 체크합니다
