#!/bin/bash
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'
echo "=== VPN Health Check: $(date) ==="
systemctl is-active --quiet xray && echo -e "Xray: ${GREEN}OK${NC}" || echo -e "Xray: ${RED}FAIL${NC}"
ss -tlnp | grep -q ":443 " && echo -e "Port 443: ${GREEN}OK${NC}" || echo -e "Port 443: ${RED}FAIL${NC}"
ss -tlnp | grep -q ":8443 " && echo -e "Port 8443: ${GREEN}OK${NC}" || echo -e "Port 8443: ${RED}FAIL${NC}"
