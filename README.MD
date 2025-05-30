# Ansible Wrapper для сбора системных метрик и установки PostgreSQL

Эта программа предназначена для сбора метрик с указанных серверов, их оценки, установки PostgreSQL наименнее загруженный сервер и настройки для разрешения внешних подключений к базе данных.

## Обзор

Playbook выполняет следующие шаги:

1. **Сбор системных метрик**: Собирает метрики, такие как I/O wait, использование диска, средняя загрузка процессора, использование оперативной памяти с каждого хоста.
2. **Оценка рейтинга**: Рассчитывает итоговый рейтинг для каждого хоста на основе собранных метрик и определяет хост с наименьшим рейтингом (меньший рейтинг означает меньшую нагрузку).
3. **Установка PostgreSQL**: Устанавливает PostgreSQL на хост с наименьшим рейтингом, используя задачи для систем на базе Debian и RedHat.
4. **Конфигурация PostgreSQL**: Настраивает PostgreSQL для прослушивания всех IP-адресов и разрешает внешние подключения со всех IP, за исключением пользователя `student`, который доступен только с других хостов.

## Требования

- Python и [Ansible установлены](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html#pipx-install) на управляющей машине.
- Для использования враппера необходимо установить пакет `ansible-runner`.
    ```bash
    pip install -r requirements.txt
    ```

## Использование

Для запуска враппера используйте Python3:
```bash
python3 main.py <hosts>
```

Для прямого запуска playbook используйте следующую команду:
```bash
ansible-playbook -i inventory.example.ini playbook/main.yml
```

Убедитесь, что inventory-файл настроен правильно с целевыми хостами. [Пример: inventory.example.ini](inventory.example.ini).

## Роли

Playbook использует следующие роли:

- **metrics_collection**: Собирает системные метрики и рассчитывает финальный счет для каждого хоста.
- **score_evaluation**: Агрегирует рейтинги, определяет хост с наименьшим рейтингом и создает динамическую группу для него.
- **postgresql_install**: Устанавливает PostgreSQL на выбранный хост (Debian и RedHat).
- **postgresql_configure**: Настраивает PostgreSQL для разрешения внешних подключений.

## Переменные

Playbook использует настраиваемые переменные:

- **postgresql_version**: Версия PostgreSQL для установки. Определяется в [`playbook/group_vars/all.yml`](playbook/group_vars/all.yml).
- **score_weights**: Коэффициенты для метрик в расчете рейтинга, определены в [`playbook/roles/metrics_collection/defaults/main.yml`](playbook/roles/metrics_collection/defaults/main.yml). Пример метрик с Коэффициентами, основанными на их влиянии на производительность базы данных, где более высокий вес означает большую важность:
    1. Ожидание ввода-вывода (коэффициент: 6, так как производительность ввода-вывода критически важна для PostgreSQL)
    2. Свободное дисковое пространство с порогом (коэффициент: 3, так как достаточное дисковое пространство существенно)
    3. Средняя загрузка процессора (коэффициент: 1, так как загрузка процессора менее критична для базы данных)
    4. Оперативная память (коэффициент: 1, так как свободная оперативная память менее значима для базы данных)

- **disk_threshold_gb**: Порог дискового пространства в ГБ для расчета рейтинга (чтобы свободное пространство не было основным критерием оценки, если доступно 500 ГБ). Определяется в [`playbook/roles/metrics_collection/defaults/main.yml`](playbook/roles/metrics_collection/defaults/main.yml).

## Вывод

Playbook предоставляет следующий вывод:

- Системные метрики для каждого хоста, включая среднее ожидание ввода-вывода, среднюю загрузку процессора, свободное дисковое пространство, используемую оперативную память и общий рейтинг.
- Результат установки PostgreSQL и имя хоста из инвентаризации, на котором произведена установка.

## Примечания

- Playbook разработан для систем на базе Debian (протестирован на Ubuntu Oracular) и RedHat (протестирован на CentOS 9 и AlmaLinux 9).
- Playbook протестирован для работы с двумя хостами, но должен быть функционален с любым количеством хостов.