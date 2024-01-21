#https://www.linuxserver.io/blog/webtop-2-0-the-year-of-the-linux-desktop
sudo docker build -t firefox .
sudo docker run --rm -it -p 3000:3000 firefox bash
