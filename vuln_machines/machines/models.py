from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from rest_framework import viewsets

class VulnerableMachine(models.Model):
    OS_CHOICES = [
        ('Linux', 'Linux'),
        ('Windows', 'Windows'),
        ('Android', 'Android'),
        ('MacOS', 'MacOS'),
    ]
    
    VULN_CHOICES = [
        ('RCE', 'Remote Code Execution'),
        ('SQLi', 'SQL Injection'),
        ('XSS', 'Cross-Site Scripting'),
        ('LFI', 'Local File Inclusion'),
        ('XXE', 'XML External Entity'),
    ]
    
    SECURITY_SYSTEMS = [
        ('SIEM', 'SIEM'),
        ('EDR', 'EDR'),
        ('PT_AF_PRO', 'PT AF PRO'),
        ('IDS', 'IDS'),
        ('IPS', 'IPS'),
    ]
    
    name = models.CharField(max_length=100, verbose_name="Название машины")
    
    vuln_id = models.CharField(
        max_length=10,
        unique=True,
        validators=[RegexValidator(r'^Vuln-\d{3}$', 'Формат должен быть Vuln-XXX')],
        verbose_name="Идентификатор"
    )
    
    # Тип и статус машины
    TYPE_CHOICES = [
        ('ready', 'Готовая'),
        ('idea', 'Идея'),
    ]
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='ready', verbose_name="Тип")
    status = models.CharField(max_length=50, default='Используется', verbose_name="Статус")
    
    wiki_link = models.URLField(blank=True, null=True, verbose_name="Ссылка на Wiki")
    
    tags = models.CharField(max_length=255, verbose_name="Теги (уязвимости)")
    description = models.TextField(verbose_name="Описание машины")
    writeups = models.TextField(blank=True, null=True, verbose_name="WriteUp'ы")
    
    os = models.CharField(max_length=20, choices=OS_CHOICES, verbose_name="ОС")
    has_gui = models.BooleanField(default=False, verbose_name="Есть ли графика в ОС")
    
    cases_count = models.PositiveIntegerField(default=0, verbose_name="Количество кейсов")
    cases_list = models.TextField(blank=True, null=True, verbose_name="Список кейсов")
    
    detected_in = models.CharField(max_length=255, verbose_name="В каких СЗИ детектируется")
    security_tools = models.CharField(max_length=255, blank=True, null=True, verbose_name="Средства защиты")
    
    # Версии ПО
    esxi_version = models.CharField(max_length=50, verbose_name="Версия ESXi")
    os_version = models.CharField(max_length=50, verbose_name="Версия ОС")
    additional_versions = models.TextField(blank=True, null=True, verbose_name="Дополнительные версии ПО")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Создатель", null=True, blank=True)
    
    def __str__(self):
        return f"{self.vuln_id} - {self.name}"
    
    class Meta:
        verbose_name = "Уязвимая машина"
        verbose_name_plural = "Уязвимые машины"