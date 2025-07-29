# Navidrome autorun for Alpine

## How to run

 > [!WARNING]
 > Execute from this folder

```bash
apk add git docker docker-compose;
cp navidrome.start /etc/local.d/navidrome.start;
chmod +x /etc/local.d/navidrome.start;
rc-update add docker default;
rc-update add local default;
```
