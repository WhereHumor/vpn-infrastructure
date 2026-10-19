# 📖 Runbook: VPN Infrastructure Recovery

## 🚨 1. Что делать, если сервер полностью упал (Disaster Recovery)
1. Арендовать новый VPS (Ubuntu 24.04).
2. Склонировать репозиторий: `git clone git@github.com:WhereHumor/vpn-infrastructure.git`
3. Перейти в папку: `cd vpn-infrastructure/ansible`
4. Настроить `inventory.ini` (вписать новый IP).
5. Запустить Ansible: `ansible-playbook -i inventory.ini playbook.yml`
6. Восстановить базу данных Remnawave из бэкапа (см. пункт 3).

## 🔐 2. Продление сертификатов Let's Encrypt
Сертификаты продлеваются автоматически. Если возникла ошибка:
1. Проверить статус: `certbot certificates`
2. Перевыпустить вручную: `certbot renew --force-renewal`
3. Перезапустить Nginx: `systemctl restart nginx`

## 💾 3. Восстановление базы данных Remnawave
1. Найти последний бэкап: `ls -la /opt/backups/remnawave/`
2. Распаковать: `gunzip remnawave_db_YYYY-MM-DD.sql.gz`
3. Залить в БД: `docker exec -i remnawave-db psql -U remnawave -d remnawave < remnawave_db_YYYY-MM-DD.sql`
4. Перезапустить панель: `docker restart remnawave`

## 🛠️ 4. Диагностика (Если что-то не работает)
* **VPN не подключается**: Проверить порты `ss -tlnp | grep -E '443|8443'`. Проверить логи ноды: `docker logs remnawave-node --tail 50`.
* **Панель не открывается**: Проверить Nginx (`nginx -t`) и логи контейнера: `docker logs remnawave`.
* **Подписка не обновляется**: Проверить логи страницы подписок: `docker logs remnawave-subscription-page --tail 50`.
* **Ошибка БД**: Проверить свободное место `df -h` и логи `docker logs remnawave-db`.
