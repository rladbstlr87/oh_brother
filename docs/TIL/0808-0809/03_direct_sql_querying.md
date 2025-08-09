# PostgreSQL 직접 조작 및 Raw SQL

## 1. Django dbshell을 이용한 DB 접속

### 핵심 개념
- Django의 `manage.py dbshell` 명령어는 `settings.py`에 설정된 정보를 이용해 데이터베이스의 커맨드 라인 인터페이스로 바로 연결하는 기능
- 별도의 접속 정보를 입력할 필요 없이 간편하게 데이터베이스 셸에 접근 가능

### For example

- 아래 명령어를 터미널에 입력
  ```bash
  python manage.py dbshell
  ```
- 실행 시 PostgreSQL의 psql 프롬프트가 나타나며, SQL 쿼리를 직접 입력할 수 있는 상태가 됨

## 2. Raw SQL을 이용한 데이터 조회

### 핵심 개념
- ORM이 추상화하는 SQL 쿼리문을 직접 작성하여 데이터를 조회하는 방식
- 테이블의 구조와 관계(예: Foreign Key)를 정확히 이해하고 있어야 함
- `SELECT`, `FROM`, `WHERE`, `JOIN` 등의 SQL 키워드를 사용

### For example

- 특정 교회가 주최한 모든 행사 찾기 (ORM: `church.hosted_events.all()`)
  ```sql
  SELECT
    ee.*
  FROM
    events_event AS ee
  JOIN
    churches_church AS cc ON ee.church_id = cc.id
  WHERE
    cc.name = '사랑교회';
  ```
- 위 쿼리는 `churches_church` 테이블과 `events_event` 테이블을 `JOIN`하여, 교회 이름이 '사랑교회'인 모든 행사 정보를 선택

### What it can do?

#### ex.level.2: 복잡한 통계 및 리포팅 쿼리
- 월별 행사 개최 수, 교회별 평균 참석자 수 등 ORM으로 표현하기 복잡하거나 성능이 저하될 수 있는 집계 및 통계 쿼리를 Raw SQL로 작성하여 효율적으로 처리 가능

#### ex.level.3: 데이터베이스 성능 최적화
- ORM이 생성하는 쿼리 대신, 특정 상황에 더 최적화된 쿼리(예: 인덱스 힌트 사용)를 직접 작성하여 데이터베이스의 성능을 극대화

## 3. Raw SQL 결과를 API로 제공하기

### 핵심 개념
- `dbshell`에서 조회한 데이터를 프론트엔드로 전달하려면, 해당 데이터를 JSON 형식으로 제공하는 API 엔드포인트가 필요
- Django View 내에서 Raw SQL을 실행하고, 그 결과를 `JsonResponse`로 반환하여 API를 구현

### For example

#### `events/views.py`
- Raw SQL을 실행하고 결과를 JSON으로 반환하는 뷰 함수를 작성
```python
from django.db import connection
from django.http import JsonResponse

# 커서의 실행 결과를 딕셔너리 리스트로 변환하는 헬퍼 함수
def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

# '사랑교회'의 모든 이벤트를 반환하는 API 뷰
def church_events_api(request):
    # 지난 TIL에서 작성한 Raw SQL 쿼리
    sql = """
        SELECT
          ee.id,
          ee.name,
          ee.date
        FROM
          events_event AS ee
        JOIN
          churches_church AS cc ON ee.church_id = cc.id
        WHERE
          cc.name = '사랑교회';
    """
    
    with connection.cursor() as cursor:
        cursor.execute(sql)
        rows = dictfetchall(cursor)

    # 쿼리 결과를 JSON으로 변환하여 응답
    return JsonResponse(rows, safe=False)
```

#### `events/urls.py`
- 작성된 뷰 함수를 특정 URL 경로와 연결
```python
from django.urls import path
from . import views

urlpatterns = [
    # 기존 url 패턴들
    # ...
    # 새로 추가할 API 경로
    path('api/church-events/', views.church_events_api, name='church_events_api'),
]
```

## 4. dbshell vs GUI Tool (DBeaver)

### 비교 요약

| 구분 | Django dbshell | DBeaver (같은 GUI 툴) |
| :--- | :--- | :--- |
| **용도/목적** | - 개발 중인 Django 프로젝트의 DB를 빠르고 가볍게 확인<br>- 간단한 쿼리 테스트 또는 데이터 존재 유무 체크 | - 데이터베이스 구조(스키마)의 시각적 분석<br>- 복잡한 쿼리 작성 및 데이터 분석, 리포팅<br>- 데이터 가져오기/내보내기 등 고급 기능 사용 |
| **접속 편의성** | - `settings.py` 정보를 자동 사용하므로 매우 편리<br>- 별도 설정 불필요 | - DB 접속 정보(호스트, 포트, 사용자, 암호)를 직접 입력하고 저장해야 함<br>- 한 번 설정 후에는 여러 DB를 쉽게 관리 |
| **사용자 인터페이스** | - CLI (커맨드 라인) 기반<br>- 모든 조작을 명령어로 수행 | - GUI (그래픽) 기반<br>- 테이블, 데이터를 표 형태로 보고 마우스로 조작 가능 |
| **데이터 시각화** | - 텍스트로만 결과를 출력하여 가독성이 떨어짐 | - 테이블 관계(ERD)를 시각적으로 보여줌<br>- 쿼리 결과를 정렬, 필터링하기 용이함 |
| **처리 속도** | - **쿼리 실행 속도**: DB가 처리하므로 GUI 툴과 동일<br>- **실행/접속 속도**: 터미널에서 즉시 실행되므로 매우 빠름 | - **쿼리 실행 속도**: dbshell과 동일<br>- **실행/접속 속도**: 애플리케이션 구동에 시간이 다소 소요됨 |
| **비용** | - Django에 포함된 기능이므로 무료 | - DBeaver Community 버전은 무료<br>- DataGrip 등 일부 전문 툴은 유료 |
| **자원 사용량** | - 매우 가벼워 시스템 자원을 거의 차지하지 않음 | - GUI 앱이므로 dbshell보다 메모리를 더 많이 사용 |

### 결론: 언제 무엇을 사용할까?

- **dbshell은 이럴 때 사용**
    - 개발 중 "이 데이터가 잘 들어갔나?" 하고 빠르게 확인할 때
    - `views.py`에 작성할 간단한 쿼리를 미리 테스트해볼 때
    - 서버 환경 등 GUI를 사용할 수 없는 환경에서 작업할 때

- **DBeaver (GUI 툴)은 이럴 때 사용**
    - 프로젝트의 전체 데이터베이스 구조를 파악하고 싶을 때
    - 여러 테이블을 `JOIN`하는 등 복잡한 SQL 쿼리를 작성하고 분석할 때
    - 쿼리 결과를 엑셀처럼 편하게 보고, 정렬하거나 필터링하고 싶을 때
