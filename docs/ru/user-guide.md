# Установка и воспроизводимые примеры

Нужен Python 3.12+ с текущими исправлениями. Из распакованного корня создайте отдельное окружение и установите пакет. Версии зафиксированы; установка может скачивать пакеты, обработка отчёта сеть не использует. На Windows — python/py -3 и пути .venv\Scripts.

```bash
python3 -m venv .venv
.venv/bin/python -m pip install .
.venv/bin/opsec-report validate examples/after.json
.venv/bin/opsec-report diff examples/before.json examples/after.json --output comparison.json
.venv/bin/opsec-report html examples/before.json --output report.html
```
Первый пример — явные синтетические pass (0), diff даёт explicitly_passed (0), HTML записывается с кодом находок 1. Выходы должны быть новыми. Для повтора выберите новые имена; не перезаписывайте свидетельства ради успеха.

Нормализация изученного AD-примера даёт 0; находок Guard — 1 с явным контекстом:

```bash
.venv/bin/opsec-report normalize ad examples/ad-source.synthetic.json --output normalized-ad.json
.venv/bin/opsec-report normalize guard examples/guard-source.synthetic.json --scope synthetic-materials --observed-at 2026-10-12T00:00:00Z --synthetic --output normalized-guard.json
```
Примеры не доказывают безопасность реальной инфраструктуры. Источники держите приватными, scope/asset проверяйте перед передачей. HTML не содержит JavaScript/сетевых ресурсов и открывается локально; произвольный текст не очищается автоматически.

---

[Documentation index](index.md)
