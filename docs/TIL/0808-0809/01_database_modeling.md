# 데이터베이스 모델링 (Database Modeling)

## 1. Django ORM을 이용한 모델 설계

### 핵심 개념
- Django ORM(Object-Relational Mapping)을 사용하여, SQL 쿼리 없이 파이썬 클래스만으로 데이터베이스 테이블과 관계를 정의하는 기법
- 각 클래스는 테이블에, 클래스의 속성(attribute)은 테이블의 컬럼(column)에 해당

- `models.ForeignKey`: 1:N (다대일) 관계 정의. (예: 하나의 교회가 여러 행사를 주최)
- `models.ManyToManyField`: N:M (다대다) 관계 정의. (예: 하나의 강사가 여러 행사에 참여)
- `models.CharField`, `models.TextField`, `models.DateTimeField`: 데이터의 종류와 제약조건을 정의하는 필드 타입

### For example (모델 설계를 통해 할 수 있는 것)

#### ex.1-1: 데이터의 무결성 및 일관성 확보
- `Event` 모델이 `Church` 모델을 `ForeignKey`로 참조하게 함으로써, 존재하지 않는 교회가 행사를 주최하는 상황을 원천적으로 방지
- 교회 이름이 변경될 경우, `Church` 모델의 `name`만 수정하면 해당 교회를 참조하는 모든 `Event` 객체에 변경사항이 자동으로 반영됨

#### ex.1-2: 논리적 데이터 검색 및 필터링
- ORM을 통해 복잡한 SQL 없이도 직관적인 데이터 조회가 가능
- 특정 교회가 주최한 모든 행사 찾기
  ```python
  church = Church.objects.get(name='사랑교회')
  events = church.hosted_events.all() # related_name 사용
  ```
- 특정 강사가 참여하는 모든 행사 찾기
  ```python
  speaker = Speaker.objects.get(name='김사랑')
  events = speaker.event_set.all()
  ```

### What it can do? (더 복잡한 활용)

#### ex.level.2: 체계적인 정보 제공 API 개발
- 잘 구조화된 모델은 REST API의 엔드포인트를 설계하는 기반이 됨
- `/api/churches/{church_id}/events/`: 특정 교회의 모든 행사 목록을 보여주는 API
- `/api/speakers/{speaker_id}/events/`: 특정 강사의 모든 행사 목록을 보여주는 API

#### ex.level.3: 관리자 페이지 자동 생성 및 커스터마이징
- 정의된 모델을 Django Admin 사이트에 등록하기만 하면, 별도의 코딩 없이도 데이터를 생성(Create), 조회(Read), 수정(Update), 삭제(Delete)할 수 있는 관리자 페이지가 자동으로 만들어짐
- 이를 통해 개발 초기 단계에서 데이터 관리 및 테스트 효율성을 극대화할 수 있음