# 🛡️ Production-Ready VPN Infrastructure (VLESS + Reality + Remnawave)

Отказоустойчивая, масштабируемая VPN-инфраструктура, развернутая на VPS (Ubuntu 24.04, Нидерланды) с автоматическим развертыванием, мониторингом и панелью управления пользователями.

## 🏗️ Архитектура

Система спроектирована с разделением на слои (Control Plane и Data Plane):

* **Data Plane (Трафик)**: 
  * **VLESS + Reality (TCP:443)** — основной канал, маскирующийся под HTTPS (TLS 1.3) к `dl.google.com` для обхода DPI.
  * **VLESS + XHTTP (TCP:8443)** — резервный транспорт для обхода жестких блокировок.
* **Control Plane (Управление)**: 
  * **Remnawave**: Панель управления пользователями, генерация подписок, управление нодами (Node).
  * **Nginx**: Reverse-proxy с Basic Auth и SSL (Let's Encrypt) для безопасного доступа к панели и мониторингу.
* **Observability (Мониторинг)**:
  * **Prometheus + Node Exporter + Blackbox Exporter**: Сбор метрик сервера и проверка доступности портов (ICMP, TCP).
  * **Grafana**: Визуализация метрик (дашборды).
  * **Alertmanager**: Отправка алертов о падении сервисов в Telegram.

## 🚀 Технологический стек

* **OS**: Ubuntu 24.04 LTS
* **VPN Core**: Xray (VLESS, Reality, XHTTP)
* **Panel**: Remnawave (Node.js, PostgreSQL, Redis)
* **Web**: Nginx (Reverse Proxy, Basic Auth, Let's Encrypt)
* **Monitoring**: Prometheus, Grafana, Blackbox, Alertmanager
* **Автоматизация**: Ansible, Bash, Cron
* **Безопасность**: UFW, Fail2ban, раздельное туннелирование

## 📦 Развертывание (Ansible)

Проект полностью автоматизирован. Для развертывания с нуля достаточно одной команды:

bash
cd ansible
ansible-playbook -i inventory.ini playbook.yml


Что делает плейбук:

1. Устанавливает Xray и базовые пакеты (UFW, Fail2ban).
2. Настраивает конфигурацию VLESS+Reality (TCP и XHTTP).
3. Устанавливает Nginx и настраивает reverse-proxy для мониторинга (Basic Auth).
4. Получает SSL-сертификаты через Let's Encrypt (Certbot).
5. Копирует Bash-скрипты для проверки туннеля и бэкапа конфигов.
6. Настраивает Cron для автоматического запуска скриптов.

📊 Мониторинг и Алерты

· Grafana: Доступна по адресу https://<domain>:9443/grafana/ (Basic Auth).
· Дашборды: Node Exporter Full (ID: 1860), Blackbox Exporter (ID: 13659).
· Алерты: При падении порта 443 или 8443, Alertmanager отправляет уведомление в Telegram-бот.

🔐 Безопасность

· UFW: Открыты только необходимые порты (22, 443, 8443, 9443).
· Fail2ban: Защита SSH от брутфорса (3 попытки = бан на 1 час).
· Nginx: Basic Auth и HTTPS для доступа к панели управления и мониторингу.
· SSH: Авторизация по ключам (пароль оставлен как резервный).

📁 Структура проекта

.
├── ansible/
│   ├── inventory.ini
│   ├── playbook.yml
│   ├── check-tunnel.sh
│   ├── backup-configs.sh
│   ├── templates/
│   │   ├── xray-config.json.j2
│   │   └── nginx-monitoring.j2
│   └── vars/
│       ├── secrets.yml (НЕ КОММИТИТСЯ)
│       └── secrets.yml.example
├── .github/workflows/
│   └── validate.yml
└── README.md


📈 Результаты (Benchmarks)

· Скорость: до 290 Мбит/с (VLESS+Reality, Speedtest).
· Пинг: ~60-70 мс (из РФ до Амстердама).
· Uptime: 99.9% (мониторинг Prometheus).

⚠️ Disclaimer

Проект создан в образовательных целях для изучения сетевых технологий, Xray, Docker и Ansible. Используйте в соответствии с законодательством вашей страны.
