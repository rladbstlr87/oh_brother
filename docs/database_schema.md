# 데이터베이스 모델 설계 (Database Schema)

- 데이터 처리 순서: `SourceDocument` -> (`Church`, `Speaker`, `Contact`...) -> `Event`
- 핵심 원칙: 원본 데이터(`SourceDocument`)와 정제된 데이터(`Event`)를 분리하고, 반복 사용되는 정보(`Church`, `Speaker`, `Contact`)는 독립적인 모델로 관리하여 중복을 최소화

---

## 1. 원본 공문 (SourceDocument)
> 수집된 원본 공문 파일과 처리 상태 관리. 모든 정제된 데이터의 '원재료' 역할.

| 한글명 | 영문명 (Field) | 데이터 타입 (예시) | 설명 |
|---|---|---|---|
| 원본 파일 | `original_file` | FileField | 사용자가 업로드한 원본 파일 (pdf, jpg, png 등) |
| WebP 변환 파일 | `webp_file` | ImageField | 원본을 WebP로 변환하여 저장한 파일 |
| 추출된 텍스트 | `extracted_text` | TextField | OCR로 추출한 텍스트 전문 |
| 처리 상태 | `status` | CharField | `대기`, `처리중`, `완료`, `실패` 등 처리 과정 기록 |
| 생성일 | `created_at` | DateTimeField | 레코드 생성 시각 |

---

## 2. 교회/단체 (Church)
> 교회 또는 단체 정보를 독립적으로 관리하여 중복을 방지.

| 한글명 | 영문명 (Field) | 데이터 타입 (예시) | 설명 |
|---|---|---|---|
| 교회/단체명 | `name` | CharField | |
| 주소 | `address` | CharField | |
| 웹 주소 | `website` | URLField | |

---

## 3. 강사 (Speaker)
> 강사 정보를 관리. 한 강사는 여러 행사에 참여할 수 있음.

| 한글명 | 영문명 (Field) | 데이터 타입 (예시) | 설명 |
|---|---|---|---|
| 강사명 | `name` | CharField | |
| 소속 교회 | `home_church` | ForeignKey | `Church` 모델과 연결 |

---

## 4. 담당자 (Coordinator)
> 행사 문의 담당자 정보를 관리.

| 한글명 | 영문명 (Field) | 데이터 타입 (예시) | 설명 |
|---|---|---|---|
| 담당자명 | `name` | CharField | |
| 연락처 | `phone` | CharField | |

---

## 5. 행사 (Event)
> 모든 정제된 정보를 종합하여 최종 행사 데이터를 구성.

| 한글명 | 영문명 (Field) | 데이터 타입 (예시) | 설명 |
|---|---|---|---|
| 행사명 | `title` | CharField | |
| 주제 | `topic` | CharField | |
| 행사 종류 | `tags` | CharField | `수련회`, `세미나` 등 선택지 |
| 상세 설명 | `description` | TextField | |
| 중심 말씀 | `logos` | CharField | 예: "요한복음 3:16" |
| 포스터 이미지 | `images` | ImageField | 대표 이미지 (WebP 형식) |
| 하루 종일 | `all_day` | BooleanField | 시간 정보 없이 하루 종일 진행되는 행사 여부 |
| 시작 일시 | `start_datetime` | DateTimeField | `all_day=True`이면 시간은 00:00으로 저장 |
| 종료 일시 | `end_datetime` | DateTimeField | `all_day=True`이면 시간은 23:59로 저장 |
| 장소 | `location` | CharField | |
| 주최 교회 | `host_church` | ForeignKey | `Church` 모델과 연결 |
| 강사진 | `speakers` | ManyToManyField | `Speaker` 모델과 연결 |
| 접수 URL | `registration_url` | URLField | |
| 담당자 | `coordinator` | ForeignKey | `Coordinator` 모델과 연결 |
| 원본 공문 | `source_document` | ForeignKey | 이 행사의 출처가 된 `SourceDocument`와 연결 |
| 생성/수정일 | `created_at` / `updated_at` | DateTimeField | |
