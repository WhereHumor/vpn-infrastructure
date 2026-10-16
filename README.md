# VPN Infrastructure

Отказоустойчивая VPN-инфраструктура на базе Xray (VLESS + Reality) с мониторингом и автоматическим развёртыванием.

## Архитектура

- **VLESS + Reality (TCP, 443)** — основной канал.
- **VLESS + Reality (XHTTP, 8443)** — резервный транспорт.
- **Prometheus + Grafana** — мониторинг.
- **Blackbox Exporter** — проверка доступности.
- **Alertmanager** — алерты в Telegram.

## Компоненты

| Компонент | Назначение |
|-----------|------------|
| Xray | VPN-сервер (VLESS + Reality) |
| Prometheus | Сбор метрик |
| Grafana | Визуализация |
| Blackbox Exporter | Проверка доступности (ICMP, TCP) |
| Alertmanager | Уведомления в Telegram |
| Node Exporter | Метрики VPS |

## Развёртывание

cd ansible
ansible-playbook -i inventory.ini playbook.yml


Требования

· Ubuntu 22.04/24.04
· Ansible 2.15+
· SSH-доступ к VPS

Безопасность

· UFW (только необходимые порты).
· Fail2ban (защита SSH).
· SSH-ключи + пароль как резерв.
· Секреты в vars/secrets.yml (не коммитятся).

Лицензия

MIT

