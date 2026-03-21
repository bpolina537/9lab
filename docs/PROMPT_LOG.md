Prompt Log
Лабораторная работа №9: Мультиязычное программирование

Студент: Бондаренко Полина
Группа: 221331
Репозиторий: bpolina537/9lab
Дата выполнения: 20.03.2026


Промпт 1
Инструмент: DeepSeek-V3.2

Промпт:
Составь детальный пошаговый план для лабораторной работы №9. Задания:
3. Скомпилировать Go-программу в бинарь и вызвать её из Python (subprocess)
5. Реализовать на Go простой TCP-сервер, к которому подключается Python-клиент
10. Реализовать на Rust структуру и экспортировать её в Python как класс
1. Создать микросервис на Go с тяжёлыми вычислениями, вызывать из Python через HTTP
4. Создать Python-приложение, которое использует Go для оркестрации и Rust для криптографии

Выполнять строго в порядке 3→5→10→1→4.

Из методички используем:
- Go: горутины, каналы, HTTP-сервер, компиляция в бинарь
- Rust: безопасная работа с памятью, FFI, PyO3/Maturin
- Взаимодействие: вызов Go-бинарня как подпроцесса из Python, вызов Rust-функций как библиотеки через PyO3

План должен быть таким, чтобы можно было двигаться шаг за шагом, проверяя каждый этап.

Результат: Получила план с разбивкой на микрошаги и проверками.


Задание 3: Go бинарник + subprocess

Промпт 2
Инструмент: DeepSeek-V3.2

Промпт:
Шаг 1. Инициализируй Go-модуль в папке go-binary: main.go с выводом "Hello from Go" и go.mod. Проверяем.

Результат: Инициализировала go-binary/, main.go, go.mod. Проверка: go run main.go → "Hello from Go"


Промпт 3
Инструмент: DeepSeek-V3.2

Промпт:
Шаг 2. Добавь скрипты сборки build.bat для Windows и build.sh для Linux/Mac. Бинарник go-binary.exe. Проверяем.

Результат: Добавила build.bat, build.sh. Проверка: build.bat → появился go-binary.exe


Промпт 4
Инструмент: DeepSeek-V3.2

Промпт:
Шаг 3. Реализуй Python-скрипт subprocess_client.py, который запускает бинарник через subprocess и выводит результат. Проверяем.

Результат: Реализовала python-client/subprocess_client.py с subprocess.run(). Проверка: python subprocess_client.py → "Output from Go: Hello from Go"


Промпт 5
Инструмент: DeepSeek-V3.2

Промпт:
Шаг 4. Настрой .gitignore: добавь исключения для бинарников *.exe, go-binary, go-binary.exe.

Результат: Настроила .gitignore. Проверка: git status не показывает бинарники

Что пришлось исправлять вручную: ничего
Коммиты: feat: complete task 3 - go binary with subprocess, chore: add gitignore and remove .venv from tracking
Итого промптов на конец задания 3: 5


Задание 5: TCP-сервер на Go + Python-клиент

Промпт 6
Инструмент: DeepSeek-V3.2

Промпт:
Шаг 1. Инициализируй TCP-сервер на Go в папке go-server: базовый сервер принимает одно соединение, читает сообщение, отвечает "OK". Проверяем через nc.

Результат: Инициализировала go-server/main.go, go.mod. Проверка: nc localhost 8080 → "OK"


Промпт 7
Инструмент: DeepSeek-V3.2

Промпт:
Шаг 2. Добавь бесконечный цикл, чтобы сервер обрабатывал несколько соединений последовательно. Проверяем.

Результат: Добавила цикл for. Проверка: несколько подключений подряд → каждое получает "OK"


Промпт 8
Инструмент: DeepSeek-V3.2

Промпт:
Шаг 3. Добавь горутины для параллельной обработки соединений. Проверяем параллельными клиентами.

Результат: Добавила go handleConnection(conn). Проверка: запустила несколько клиентов параллельно → все получили ответ


Промпт 9
Инструмент: DeepSeek-V3.2

Промпт:
Шаг 4. Реализуй Python-клиент tcp_client.py, который подключается через socket, отправляет "ping", выводит ответ. Проверяем.

Результат: Реализовала python-client/tcp_client.py. Проверка: сервер запущен, клиент → получила "OK"

Проблема: WinError 10053 при втором сообщении — сервер закрывает соединение после первого ответа
Что пришлось исправлять вручную: ничего, для бенчмарков это приемлемо
Коммит: feat: add go tcp server and python tcp client (task 5)
Итого промптов на конец задания 5: 9


Задание 10: Rust структура + PyO3

Промпт 10
Инструмент: DeepSeek-V3.2

Промпт:
Шаг 1. Инициализируй Rust-проект с PyO3 в папке rust-processor через maturin init. Проверяем сборку.

Результат: Инициализировала проект: maturin init в rust-processor/. Проверка: maturin develop → сборка прошла


Промпт 11
Инструмент: DeepSeek-V3.2

Промпт:
Шаг 2. Реализуй структуру DataProcessor с полем factor и методом get_factor. Экспортируй в Python. Проверяем.

Результат: Реализовала #[pyclass], #[new], fn get_factor(). Проверка: dp = DataProcessor(5); print(dp.get_factor()) → 5

Проблема: ошибки под PyO3 0.27 — адаптировала код
Что пришлось исправлять вручную: код под новую версию PyO3


Промпт 12
Инструмент: DeepSeek-V3.2

Промпт:
Шаг 3. Реализуй метод process, который умножает каждое число в списке на factor. Проверяем.

Результат: Реализовала fn process(&self, data: Vec<i32>) -> Vec<i32>. Проверка: dp.process([1,2,3]) → [3,6,9]

Что пришлось исправлять вручную: ничего
Коммиты: feat: add rust DataProcessor with PyO3 (task 10), chore: update gitignore for rust, chore: remove Cargo.lock from repository
Итого промптов на конец задания 10: 12


Задание 1: Go HTTP-микросервис

Промпт 13
Инструмент: DeepSeek-V3.2

Промпт:
Шаг 1. Инициализируй HTTP-микросервис на Go в папке go-http-service. Эндпоинт POST /compute принимает JSON с числами, возвращает сумму квадратов. Проверяем через curl.

Результат: Инициализировала go-http-service/main.go. Проверка: curl -X POST ... -d '{"numbers":[1,2,3]}' → {"result":14}


Промпт 14
Инструмент: DeepSeek-V3.2

Промпт:
Шаг 2. Добавь искусственную задержку 100ms для имитации тяжёлых вычислений.

Результат: Добавила time.Sleep(100 * time.Millisecond). Проверка: запрос выполняется ~100ms


Промпт 15
Инструмент: DeepSeek-V3.2

Промпт:
Шаг 3. Реализуй Python-клиент http_client.py, который отправляет POST-запросы через requests и выводит результат.

Результат: Реализовала python-client/http_client.py. Проверка: запустила сервер, клиент → получила JSON

Что пришлось исправлять вручную: ничего
Коммит: feat: add go http microservice and python http client (task 1)
Итого промптов на конец задания 1: 15


Задание 4: Оркестратор

Промпт 16
Инструмент: DeepSeek-V3.2

Промпт:
Шаг 1. Реализуй orchestrator.py, который отправляет числа в Go HTTP, получает сумму, использует Rust DataProcessor для обработки, выводит результат.

Результат: Реализовала python-client/orchestrator.py. Проверка: запустила Go HTTP-сервер, запустила оркестратор → вывела сумму и финальный результат

Что пришлось исправлять вручную: ничего
Коммит: feat: add orchestrator combining go and rust (task 4)
Итого промптов на конец задания 4: 16


Тесты

Промпт 17
Инструмент: DeepSeek-V3.2

Промпт:
Добавь handler_test.go для Go-сервера: тесты на соединение, конкурентность, бенчмарк.

Результат: Добавила go-server/handler_test.go с 3 тестами и 1 бенчмарком

Проблема: тест с несколькими сообщениями падал (EOF) — упростила до одного сообщения
Что пришлось исправлять вручную: упрощение теста


Промпт 18
Инструмент: DeepSeek-V3.2

Промпт:
Добавь test_client.py для Python: тесты для TCP и HTTP клиентов.

Результат: Добавила python-client/tests/test_client.py с 5 тестами

Проблема: TypeError с исключениями в http_client — исправила обработку ошибок
Что пришлось исправлять вручную: исправление обработки ошибок в http_client.py


Промпт 19
Инструмент: DeepSeek-V3.2

Промпт:
Добавь юнит-тесты для Rust в lib.rs: конструктор, process, пустой список, отрицательные числа.

Результат: Добавила 12 юнит-тестов

Что пришлось исправлять вручную: ничего
Коммиты: test: add rust unit tests, test: fix go tests
Итого промптов на конец тестов: 19


Бенчмарки

Промпт 20
Инструмент: DeepSeek-V3.2

Промпт:
Создай бенчмарк для сравнения Python, Rust и Go на размерах 100, 500, 1000, 5000, 10000, 50000.

Результат: Создала benchmarks/benchmark.py с графиками и JSON

Проблемы:
- Rust медленнее Python — пересобрала в release
- Go падает на 1M элементов — увеличила буфер
- Tcl/Tk ошибка — добавила Agg бэкенд

Что пришлось исправлять вручную: release-сборка, увеличение буфера, добавление Agg бэкенда
Коммит: fix: add Tcl/Tk path and use Agg backend for plotting
Итого промптов на конец бенчмарков: 20


CI/CD

Промпт 21
Инструмент: DeepSeek-V3.2

Промпт:
Добавь GitHub Actions: тесты для Go, Rust, Python на всех версиях Python.

Результат: Добавила .github/workflows/test.yml

Проблема: maturin develop требует виртуальное окружение — заменила на maturin build + pip install
Что пришлось исправлять вручную: замена maturin develop на maturin build
Коммиты: ci: add GitHub Actions workflows for tests, publish, and benchmarks, ci: add complete CI/CD pipelines, ci: fix Python tests - use maturin build instead of develop
Итого промптов на конец CI/CD: 21


Удаление служебных файлов

Промпт 22
Инструмент: DeepSeek-V3.2

Промпт:
Удали папку .idea из репозитория.

Результат: Выполнила git rm -r --cached .idea

Что пришлось исправлять вручную: ничего
Коммит: chore: remove .idea from repository
Итого промптов: 22


Публикация документации

Промпт 23
Инструмент: DeepSeek-V3.2

Промпт:
Создай PROMPT_LOG.md с полной историей.

Результат: Создала docs/PROMPT_LOG.md

Коммит: docs: add PROMPT_LOG.md
Итого промптов: 23


Итоговая статистика

Этап	Промпты	Итого промптов
Планирование	1	1
Задание 3	4	5
Задание 5	4	9
Задание 10	3	12
Задание 1	3	15
Задание 4	1	16
Тесты	3	19
Бенчмарки	1	20
CI/CD	1	21
Удаление .idea	1	22
Документация	1	23

Всего промптов: 23
Всего коммитов: 17


Полный список коммитов

Хеш	Сообщение
fca499c	chore: add gitignore and remove .venv from tracking
673c8c9	feat: complete task 3 - go binary with subprocess
f08196e	chore: remove .idea from repository
993f422	feat: add go tcp server and python tcp client (task 5)
d8f3d3a	feat: add rust DataProcessor with PyO3 (task 10)
ee6cec0	chore: update gitignore for rust
4c9aff9	chore: remove Cargo.lock from repository
8b2213c	feat: add go http microservice and python http client (task 1)
d39fe04	feat: add orchestrator combining go and rust (task 4)
e66e55e	test: add rust unit tests (12 tests)
769fb22	test: fix go tests - simplify multiple messages test
147189e	fix: add Tcl/Tk path and use Agg backend for plotting
20a8b31	ci: add GitHub Actions workflows for tests, publish, and benchmarks
3a043dc	ci: add complete CI/CD pipelines
8656158	ci: fix Python tests - use maturin build instead of develop
610a118	chore: remove .idea from repository
b32f1b3 docs: add PROMPT_LOG.md
