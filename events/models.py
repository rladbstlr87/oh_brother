import os
from django.db import models

class SourceDocument(models.Model):
    # 원본 파일 부재 가능
    original_file = models.FileField(upload_to='source_documents/', blank=True, null=True, verbose_name="원본 파일")
    webp_file = models.ImageField(upload_to='webp_documents/', blank=True, null=True, verbose_name="WebP 변환 파일")
    extracted_text = models.TextField(blank=True, verbose_name="추출된 텍스트")
    unique_identifier = models.CharField(max_length=255, unique=True, blank=True, null=True, verbose_name="고유 식별자")
    status = models.CharField(max_length=10, default='대기', verbose_name="처리 상태")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="생성일")

    def __str__(self):
        if self.original_file and self.original_file.name:
            return os.path.basename(self.original_file.name)
        if self.unique_identifier:
            return self.unique_identifier
        return f"Source Document {self.id}"

class Church(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name="교회/단체명")
    address = models.CharField(max_length=255, blank=True, verbose_name="주소")
    website = models.URLField(max_length=200, blank=True, verbose_name="URL")

    def __str__(self):
        return self.name

class Speaker(models.Model):
    name = models.CharField(max_length=100, verbose_name="강사명")
    home_church = models.ForeignKey(
        Church,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="affiliated_speakers",
        verbose_name="소속 교회"
    )

    def __str__(self):
        return f"{self.name} ({self.home_church.name if self.home_church else '소속 없음'})"

class Coordinator(models.Model):
    name = models.CharField(max_length=100, verbose_name="담당자명")
    phone = models.CharField(max_length=20, blank=True, verbose_name="연락처")

    def __str__(self):
        return self.name

class Event(models.Model):
    title = models.CharField(max_length=200, verbose_name="집회명")
    topic = models.CharField(max_length=200, blank=True, verbose_name="주제")
    tags = models.CharField(max_length=50, blank=True, verbose_name="집회 종류")
    description = models.TextField(blank=True, verbose_name="상세 설명")
    logos = models.CharField(max_length=100, blank=True, verbose_name="말씀")
    images = models.ImageField(upload_to='event_posters/', blank=True, verbose_name="첨부 이미지")
    all_day = models.BooleanField(default=False, verbose_name="하루 종일")
    start_datetime = models.DateTimeField(verbose_name="시작 일시")
    end_datetime = models.DateTimeField(verbose_name="종료 일시")
    location = models.CharField(max_length=255, verbose_name="장소")
    host_church = models.ForeignKey(
        Church,
        on_delete=models.CASCADE,
        related_name="hosted_events",
        verbose_name="주최 교회/단체"
    )
    speakers = models.ManyToManyField(Speaker, blank=True, verbose_name="강사진")
    registration_url = models.URLField(max_length=200, blank=True, verbose_name="접수 URL")
    coordinator = models.ForeignKey(
        Coordinator,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="담당자"
    )
    source_document = models.ForeignKey(
        SourceDocument,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="원본 공문"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title