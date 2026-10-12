# CLI и коды завершения

Команды: validate INPUT; diff BEFORE AFTER [--output NEW_FILE]; html INPUT --output NEW_FILE; normalize guard INPUT --scope LABEL --observed-at UTC [--synthetic] --output NEW_FILE; normalize ad INPUT --output NEW_FILE. Нет угадывания файлов и автоматического определения источника. Python-модуль равнозначен установленной opsec-report.

Валидация/нормализация/HTML возвращают оценку: 0 — без fail и полное заявленное покрытие, 1 — любой fail, 2 — неполнота без fail, 3 — неверный вход/выход/runtime. Записанный HTML с fail завершится 1. Diff: 0 — совместимо, 2 — разные контексты, 3 — ошибка. Ноль diff не означает отсутствие изменений/риска. Выход не должен существовать. Диагностика — статические коды без текста исключений/путей источника.

Контекст Guard обязателен: response-0.2 не даёт подходящих области/времени/synthetic для автоматического вывода. --synthetic устанавливает true; без него заявляется non-synthetic, но это не подтверждается независимо. AD берёт класс источника. Вход — строгий UTF-8 без BOM; константы вне JSON и повторные ключи отклоняются.

---

[Documentation index](index.md) · [English](../en/cli-reference.md)
