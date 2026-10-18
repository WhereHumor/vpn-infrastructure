#!/bin/bash
BACKUP_DIR="/opt/backups"
DATE=$(date +%Y-%m-%d_%H-%M)
mkdir -p "$BACKUP_DIR"
tar -czf "${BACKUP_DIR}/vpn-backup-${DATE}.tar.gz" \
    /usr/local/etc/xray/config.json \
    /etc/nginx/sites-available/monitoring \
    /etc/nginx/.htpasswd 2>/dev/null
find "$BACKUP_DIR" -name "vpn-backup-*.tar.gz" -mtime +15 -delete
