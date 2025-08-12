import re

def extract_info_from_text(text: str) -> dict:
    """
    주어진 텍스트에서 이벤트 관련 정보를 추출하여 딕셔너리로 반환합니다.
    """
    extracted_data = {}
    lines = [line.strip() for line in text.split('\n') if line.strip()]

    if not lines:
        return {}

    # 1. 제목 추출 (가장 첫 줄을 제목으로 가정)
    extracted_data['title'] = lines[0]

    # 2. 주최 교회/단체 추출 (가장 마지막 줄을 주최로 가정)
    #    - "교회" 또는 "선교회" 등으로 끝나는지 확인하여 정확도 향상 가능
    potential_host = lines[-1]
    if '교회' in potential_host or '선교회' in potential_host:
        extracted_data['host_church_name'] = potential_host

    # 3. URL 추출 (정규표현식 활용)
    url_pattern = r'https?://[^\s/$.?#].[^\s]*'
    url_match = re.search(url_pattern, text)
    if url_match:
        extracted_data['url'] = url_match.group(0)

    # 4. 상세 설명 (전체 텍스트를 일단 저장)
    extracted_data['description'] = text

    # --- 앞으로 추가될 로직 ---
    # TODO: 날짜/시간 (start_datetime, end_datetime) 추출
    # TODO: 장소 (location) 추출
    # TODO: 강사 (speakers) 추출
    # TODO: 주제 (topic) 추출

    return extracted_data