# 교회 행사 정보 통합 플랫폼: Oh-Brother (오늘의 교회)

## 1. 프로젝트 개요

- 프로젝트명: 교회 행사 정보 통합 플랫폼 Oh-Brother (오늘의 교회)
- 목표: 흩어져 있는 교회들의 다양한 행사 정보를 한곳에 모아 사용자에게 제공하는 웹 서비스 및 모바일 앱 개발
- 개발 형태: 1인 개발
- 개발 기간: 25.08.06~25.09.30(2개월)
- 결과물: 핵심 기능 구현 및 프로토타입 완성

## 2. 비즈니스 프로세스 (Business Process)

- 추후 상세 내용을 채워넣을 예정

## 3. WBS (Work Breakdown Structure)

- 추후 상세 내용을 채워넣을 예정

## 4. 시스템 아키텍처 (System Architecture)

- 추후 상세 내용을 채워넣을 예정

## 5. 프로젝트 기획서

### 가. 목표

- 최소 기능 제품(MVP) 개발
    - 2개월 내 핵심 기능(정보 수집, 가공, API 제공)을 갖춘 백엔드 시스템과 기본 웹 인터페이스 개발
- 확장성 확보
    - 추후 기능 확장(모바일 앱, 추천 시스템 등)을 고려한 유연하고 확장 가능한 구조 설계
- 자동화
    - 정보 수집부터 가공까지 과정의 자동화를 통한 운영 비용 최소화

### 나. 주요 기능 정의

- 백엔드
    - 웹 크롤러 개발 (대상 웹사이트 3곳 이상)
    - 문서 파서 개발 (PDF, 이미지 형식 우선 처리)
    - REST API 서버 구축 (행사 목록 조회, 상세 조회 등)
    - 데이터베이스 모델링 (사용자, 교회, 행사 정보)
- 프론트엔드 (웹)
    - 행사 목록 조회 기본 페이지
    - 날짜 및 키워드 기반 검색 기능
- 관리자 페이지
    - 수집된 데이터 조회 및 수정 기능

### 다. 기술 스택 (예상)

- Language: Python
- Framework: Django, Django REST Framework
- Database: MySQL
- Infrastructure: AWS (EC2, S3, RDS) 또는 Termux/Linux 기반 서버
- Libraries: Celery, BeautifulSoup, Selenium, PyPDF2, Tesseract OCR 등
- Frontend: FullCalendar
