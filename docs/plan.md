---
### 1. 앱 이름 (App Name)
- 영문명: `(예: events)`
- 설명: 이 앱의 핵심 역할을 한 문장으로 요약합니다.

### 2. 주요 역할 및 책임 (Role & Responsibilities)
- 이 앱이 책임지는 기능 영역을 상세히 서술합니다.
- (예: 교회 행사 정보의 생성, 조회, 수정, 삭제(CRUD)를 담당하며, 관련 데이터 모델을 소유한다.)

### 3. 주요 모델 및 관계 (Models & Relationships)
- 이 앱이 관리할 핵심 데이터 모델을 정의합니다.
- 모델명: (예: Event)
  - 주요 필드: `title`(행사명), `date`(날짜), `location`(장소), `speaker`(강사), `description`(상세설명), `created_at`(생성일) 등
  - 관계: `Church` 모델과 N:1 관계 (ForeignKey), `Speaker` 모델과 N:M 관계 (ManyToManyField)
- 모델명: (예: Church)
  - 주요 필드: `name`(교회명), `address`(주소), `website_url`(웹사이트 주소) 등
  - 관계: ...

### 4. 핵심 기능 및 API 엔드포인트 (Features & API Endpoints)
- 이 앱이 제공할 주요 기능과 그에 해당하는 REST API 엔드포인트를 명시합니다.
- 기능: 전체 행사 목록 조회
  - API: `GET /api/events/`
  - 설명: 페이지네이션, 날짜/교회별 필터링 기능 제공
- 기능: 특정 행사 상세 정보 조회
  - API: `GET /api/events/{event_id}/`
- 기능: (관리자) 새로운 행사 등록
  - API: `POST /api/events/`

### 5. 의존성 (Dependencies)
- 이 앱이 의존하는 다른 부분을 명시합니다.
- 내부 의존성: (예: `users` 앱의 `User` 모델을 참조하여 행사 등록자를 기록함)
- 외부 라이브러리: (예: `Django REST Framework` for API, `Pillow` for ImageField)

### 6. 주요 고려사항 및 리스크 (Considerations & Risks)
- 개발 시 특별히 신경 써야 할 점이나 예상되는 어려움을 기록합니다.
- (예: 행사 날짜/시간을 다룰 때 Timezone 문제에 대한 명확한 정책 수립이 필요함)
- (예: 대용량 이미지 파일 업로드 시 성능 저하 가능성)

### 7. 추후 확장 계획 (Future Enhancements)
- 현재 버전에서는 구현하지 않지만, 미래에 추가될 수 있는 기능을 기록합니다.
- (예: 행사 참여 신청 기능)
- (예: 지도에 행사 위치 표시 기능)

---
