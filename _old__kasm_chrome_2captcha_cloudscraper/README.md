## Image on Docker Hub

### Deprecated  

It crashes more often and I don't know why.
I use the built-in linkcatcher-Function in JD

### andi91/kasm_chrome_2captcha_cloudscraper.  

A customized copy of linuxserver/webtop for my use.  
Build an docker image that have all needed dependencies for my Skripts.  
Now on kasm webtop instead rdesktop.  

### Docker compose

```
  crawler:
    container_name: webtop
    image: andi91/kasm_chrome_2captcha_cloudscraper
    ports:
      - "3000:3000"
      #- "3389:3389"
    environment:
      - PUID=1000
      - PGID=1001
      - TZ=Europe/Vienna
    restart: unless-stopped
    privileged: true
    shm_size: '2gb'
    volumes:
      - "./exchange:/exchange:rw"
      - "./jd/downloads:/jd_downloads:rw"
```