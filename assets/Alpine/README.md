# Navidrome autorun for Alpine

## How to run

```bash
apk add git docker docker-compose;
git clone https://github.com/AdriUMA/navidrome;
cd navidrome/assets;
cp navidrome.start /etc/local.d/navidrome.start;
chmod +x /etc/local.d/navidrome.start;
rc-update add local default;
```
