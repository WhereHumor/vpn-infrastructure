# 🛡️ Production-Ready VPN Infrastructure (VLESS + Reality + Remnawave)

Отказоустойчивая, масштабируемая VPN-инфраструктура с автоматическим развертыванием, мониторингом и Telegram-ботом для выдачи подписок.

## 🏗️ Архитектура системы

* **Data Plane (Трафик):** 
  * **VLESS + Reality (TCP:443)** — основной канал, маскирующийся под TLS (обход DPI).
  * **VLESS + XHTTP (TCP:8443)** — резервный транспорт для обхода жестких блокировок.
  * **Hysteria2 (UDP:443)** — экспериментальный быстрый канал на базе QUIC.
* **Control Plane (Управление):** 
  * **Remnawave:** Панель управления пользователями, генерация подписок, управление нодами (Docker, PostgreSQL, Redis).
  * **Subscription Page:** Отдельный микросервис для отдачи красивых страниц подписок клиентам.
  * **Nginx:** Reverse-proxy с SSL (Let's Encrypt) и Basic Auth для защиты панелей управления.
* **Bot Layer (Автоматизация):** 
  * **Telegram Bot (Python/Aiogram):** Через REST API Remnawave автоматически создает пользователей, задает лимиты (100 ГБ/мес) и выдает ссылки на подключение.
* **Observability (Мониторинг):**
  * **Prometheus + Grafana:** Сбор и визуализация метрик.
  * **cAdvisor:** Мониторинг ресурсов Docker-контейнеров в реальном времени.
  * **Alertmanager:** Уведомления в Telegram (падение сервисов, перегрузка CPU/RAM).

## 🚀 Технологический стек

* **OS:** Ubuntu 24.04 LTS
* **Network:** Xray (VLESS, Reality, XHTTP), Hysteria2, Nginx, UFW, Fail2ban
* **Infrastructure:** Docker, Docker Compose, Remnawave, PostgreSQL, Redis
* **Monitoring:** Prometheus, Grafana, cAdvisor, Blackbox Exporter, Node Exporter
* **Automation:** Ansible (IaC), Bash, Cron, Python (Aiogram), GitHub Actions (CI/CD)

## 📦 Развертывание (Infrastructure as Code)

Вся серверная часть описана в Ansible-плейбуках. Развертывание с нуля занимает несколько минут:

cd ansible
ansible-playbook -i inventory.ini playbook.yml
ansible-playbook -i inventory.ini remnawave-playbook.yml


Что настраивается автоматически:

1. Установка Xray, Docker, Nginx, UFW, Fail2ban.
2. Настройка конфигурации VLESS+Reality, XHTTP, Hysteria2.
3. Развертывание Remnawave (Панель + БД + Страница подписок) в изолированных сетях.
4. Получение SSL-сертификатов Let's Encrypt.
5. Настройка прав доступа и базовой безопасности.

🔄 CI/CD (Continuous Deployment)

Для Telegram-бота настроен пайплайн GitHub Actions. 
При каждом git push в ветку main (если изменения затронули папку telegram-bot/):

1. GitHub Actions подключается к VPS по SSH.
2. Скачивает обновления (git pull).
3. Перезапускает сервис бота (systemctl restart vpn-bot).

📊 Мониторинг и Алерты

· Grafana: Доступна по адресу https://<domain>:9443/grafana/ (Basic Auth).
· Дашборды: Node Exporter Full, cAdvisor, Blackbox.
· Алерты: Настроены уведомления в Telegram на падение портов VPN, падение Панели, перезагрузку бота и высокое потребление RAM контейнерами.

📁 Структура проекта
                                                                                                                         
<img width="498" height="212" alt="image" src="https://github.com/user-attachments/assets/29055b61-f488-49c9-a85b-7cc4c46ce141" />

⚠️ Disclaimer

Проект создан в образовательных целях для изучения сетевых технологий, Docker, Ansible и CI/CD. Используйте в соответствии с законодательством вашей страны.

