## WBS (Work Breakdown Structure)

### 1.0 기획 및 설정 (Planning & Setup)
- 예상 기간: 2025.08.06 ~ 2025.08.11

- 1.1. 요구사항 분석 및 기술 스택 확정
- 1.2. `docs/plan.md` 기반 상세 앱 기획 (모델, API)
- 1.3. `docs/wbs.md` 작성 및 일정 구체화
- 1.4. 개발 환경 설정
  - 1.4.1. Python/uv, Git 설치 및 설정
  - 1.4.2. `.gitignore` 파일 생성 및 규칙 정의
  - 1.4.3. Django 프로젝트 및 기본 앱 구조 생성
- 1.5. 데이터베이스 모델링 (ERD 설계)

### 2.0 핵심 백엔드 개발 (Core Backend Development)
- 예상 기간: 2025.08.12 ~ 2025.08.25

- 2.1. `users` 앱 개발
  - 2.1.1. 커스텀 User 모델 정의 (프로필 정보 추가)
  - 2.1.2. 회원가입/로그인/인증 API 구현 (DRF-SimpleJWT 등 활용)
- 2.2. `events` 앱 개발
  - 2.2.1. `Event`, `Church`, `Speaker` 등 핵심 모델 정의
  - 2.2.2. 행사 정보 CRUD API 구현
  - 2.2.3. 행사 검색 및 필터링 API 구현
- 2.3. API 문서화 (Swagger/OpenAPI 연동)

### 3.0 데이터 수집/분석 시스템 개발 (Data Parsing System)
- 예상 기간: 2025.08.26 ~ 2025.09.08

- 3.1. `parsers` 앱 생성 및 Celery/Redis 연동 설정
- 3.2. 웹 크롤러 개발
  - 3.2.1. `BeautifulSoup`, `Selenium` 기반 크롤링 로직 구현
- 3.3. 문서 파서 개발
  - 3.3.1. PDF 파서 (`PyPDF2`)
  - 3.3.2. DOCX 파서 (`python-docx`)
  - 3.3.3. HWP 파서 (`pyhwp`)
  - 3.3.4. 이미지 OCR 파서 (`Pillow`, `Tesseract`)
- 3.4. 비동기 파싱 Celery Task 정의 및 `events` 앱과 연동

### 4.0 관리자 백오피스 개발 (Admin Back-office)
- 예상 기간: 2025.09.09 ~ 2025.09.15

- 4.1. Django Admin 페이지 커스터마이징
- 4.2. 수집된 데이터 검수 및 수정/삭제 기능 구현
- 4.3. 간단한 통계/현황 대시보드 구현

### 5.0 배포 및 테스트 (Deployment & Testing)
- 예상 기간: 2025.09.16 ~ 2025.09.30

- 5.1. 단위/통합 테스트 코드 작성
- 5.2. Ubuntu 서버 환경 구축
- 5.3. PostgreSQL, Redis 서버 설치 및 설정
- 5.4. Nginx, Gunicorn 연동 및 Django 애플리케이션 배포
- 5.5. 배포 후 시스템 안정화 및 버그 수정
