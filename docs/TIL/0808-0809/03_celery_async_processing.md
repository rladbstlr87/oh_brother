# 비동기 처리 (Asynchronous Processing)

## 1. Celery와 Redis를 이용한 비동기 작업 시스템 구축

### 핵심 개념
- 시간이 오래 걸리는 작업을 별도의 '일꾼(Worker)' 프로세스에 위임하여, 메인 프로그램은 즉시 사용자에게 응답할 수 있도록 하는 처리 방식
- Redis: 처리할 작업들을 쌓아두는 '작업 대기열(Task Queue)' 역할을 하는 인-메모리 데이터 저장소. (메시지 브로커)
- Celery Worker: 백그라운드에서 실행되면서 Redis를 감시하다가, 새로운 작업이 들어오면 가져와서 실행하는 주체
- Task: `@shared_task` 데코레이터로 정의된, 비동기적으로 실행될 파이썬 함수

### For example (비동기 처리를 통해 할 수 있는 것)

#### ex.1-1: 사용자 경험(UX) 향상
- 사용자가 무거운 공문 PDF 파일을 업로드했을 때, 동기적으로 처리한다면 텍스트 추출이 끝날 때까지 몇 초 혹은 몇 분간 화면이 멈춰있게 됨
- 비동기 처리를 사용하면, 파일 업로드 요청을 받자마자 "처리 시작했습니다" 라는 응답을 즉시 보내고, 실제 파일 처리는 백그라운드의 Celery 워커에게 맡김. 사용자는 멈춤 없이 다른 작업을 계속할 수 있음
  ```python
  # views.py (사용자 요청을 받는 곳)
  def upload_file(request):
      # ... 파일 저장 로직 ...
      new_document = SourceDocument.objects.create(original_file=request.FILES['file'])
      
      # 작업을 Celery에 보내고 즉시 다음으로 넘어감
      process_document.delay(new_document.id)
      
      return HttpResponse("파일 업로드 성공! 백그라운드에서 처리 중입니다.")
  ```

#### ex.1-2: 안정적인 대규모 작업 처리
- 한 번에 100개의 공문 파일을 처리해야 할 경우, 동기적으로 처리하면 하나의 작업이 실패할 때 전체 프로세스가 멈출 수 있음
- Celery를 사용하면 100개의 처리 작업을 각각 독립적으로 대기열에 넣을 수 있음. 워커들은 이 작업들을 하나씩 가져가 처리하며, 특정 작업이 실패하더라도 다른 작업들에 영향을 주지 않음. Celery는 실패한 작업에 대한 재시도(retry) 로직도 지원하여 안정성을 높임

### What it can do? (더 복잡한 활용)

#### ex.level.2: 주기적인 작업 스케줄링 (Celery Beat)
- Celery Beat라는 스케줄러를 함께 사용하면, 특정 작업을 주기적으로 실행하도록 예약 가능
- 매일 자정마다 특정 웹사이트를 스크래핑하여 새로운 공문을 수집하는 작업
  ```python
  # settings.py
  CELERY_BEAT_SCHEDULE = {
      'collect-band-docs-every-day': {
          'task': 'parsers.tasks.collect_band_documents',
          'schedule': crontab(minute=0, hour=0), # 매일 0시 0분에 실행
      },
  }
  ```

#### ex.level.3: 분산 컴퓨팅
- 처리해야 할 작업량이 매우 많을 경우, 여러 대의 서버에 Celery 워커를 각각 실행시켜 작업 처리 능력을 수평적으로 확장(Scale-out)할 수 있음
- 모든 워커들은 중앙의 Redis 대기열을 함께 바라보며 작업을 나눠서 처리하므로, 단일 서버로는 불가능했던 대용량 데이터 처리를 효율적으로 수행 가능