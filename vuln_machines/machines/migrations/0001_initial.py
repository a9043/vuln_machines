# Generated by Django 5.2.3 on 2025-06-30 14:08

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='VulnerableMachine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название машины')),
                ('vuln_id', models.CharField(max_length=10, unique=True, validators=[django.core.validators.RegexValidator('^Vuln-\\d{3}$', 'Формат должен быть Vuln-XXX')], verbose_name='Идентификатор')),
                ('is_used', models.BooleanField(default=False, verbose_name='Используется')),
                ('wiki_link', models.URLField(blank=True, null=True, verbose_name='Ссылка на Wiki')),
                ('tags', models.CharField(max_length=255, verbose_name='Теги (уязвимости)')),
                ('description', models.TextField(verbose_name='Описание машины')),
                ('writeups', models.TextField(blank=True, null=True, verbose_name="WriteUp'ы")),
                ('os', models.CharField(choices=[('Linux', 'Linux'), ('Windows', 'Windows'), ('Android', 'Android'), ('MacOS', 'MacOS')], max_length=20, verbose_name='ОС')),
                ('has_gui', models.BooleanField(default=False, verbose_name='Есть ли графика в ОС')),
                ('cases_count', models.PositiveIntegerField(default=0, verbose_name='Количество кейсов')),
                ('cases_list', models.TextField(blank=True, null=True, verbose_name='Список кейсов')),
                ('detected_in', models.CharField(max_length=255, verbose_name='В каких СЗИ детектируется')),
                ('esxi_version', models.CharField(max_length=50, verbose_name='Версия ESXi')),
                ('os_version', models.CharField(max_length=50, verbose_name='Версия ОС')),
                ('additional_versions', models.TextField(blank=True, null=True, verbose_name='Дополнительные версии ПО')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Уязвимая машина',
                'verbose_name_plural': 'Уязвимые машины',
            },
        ),
    ]
