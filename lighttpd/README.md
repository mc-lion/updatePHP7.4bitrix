# lighttpd-fastcgi с исправленным PHP

Два пакета. Оба кладут модуль `mod_fastcgi.so` в `/opt/php-7.4.cve`. Штатный lighttpd ищет модуль в `/usr/lib64/lighttpd`, поэтому там лежит ссылка на файл внутри префикса. То же со фрагментом конфига в `/etc/lighttpd/conf.d`: это ссылка, сам файл в префиксе.

`mod_fastcgi.so` PHP не содержит. Исправления CVE-2026-109618 и CVE-2026-109619 находятся в PHP, который модуль вызывает.

Файл `conf.d/fastcgi.conf` из основного пакета lighttpd — закомментированный пример, в нём bin-path указывает на php5. Эти пакеты его не подменяют. Нужную строку `include` добавляют вручную.

## lighttpd-fastcgi — свой PHP CGI

Пакет `lighttpd-fastcgi-1.4.54-3.el7.cve` заменяет одноимённый пакет EPEL `1.4.54-1.el7` и ставит PHP целиком в `/opt/php-7.4.cve`:

```
/opt/php-7.4.cve/bin/php
/opt/php-7.4.cve/bin/php-cgi
/opt/php-7.4.cve/etc/php.ini
/opt/php-7.4.cve/etc/php.d/lighttpd.ini
/opt/php-7.4.cve/etc/php.d/10-opcache.ini
/opt/php-7.4.cve/etc/lighttpd/php-fastcgi-cve.conf
/opt/php-7.4.cve/lib/lighttpd/mod_fastcgi.so
/opt/php-7.4.cve/var/run/lighttpd/php-fastcgi.socket
```

С пакетом `php-fpm` 7.4.33-17.el7.cve он не ставится: оба занимают `/opt/php-7.4.cve`. В `/etc/lighttpd/lighttpd.conf` нужна строка:

```
include "conf.d/php-fastcgi-cve.conf"
```

Зависимости: `lighttpd = 1.4.54-1.el7`, `spawn-fcgi`, библиотеки PHP (`openssl11-libs`, `libzip5`, `libzstd`, oniguruma, libsodium, libwebp). Пакет снимает пакеты Remi `php`, `php-cli`, `php-common`, `php-fpm` и набор расширений со версией ниже `7.4.33-17.el7.cve`.

## lighttpd-fastcgi-fpm — рядом с php-fpm

Пакет `lighttpd-fastcgi-fpm-1.4.54-3.el7.cve` требует уже установленный `php-fpm-7.4.33-17.el7.cve` и свой PHP не приносит. Он добавляет:

```
/opt/php-7.4.cve/lib/lighttpd/mod_fastcgi.so
/opt/php-7.4.cve/etc/lighttpd/php-fpm-fastcgi.conf
/opt/php-7.4.cve/etc/php.d/lighttpd.ini
```

Конфиг ходит на `127.0.0.1:9000`, туда слушает пул `www` пакета php-fpm. В конфиг lighttpd:

```
include "conf.d/php-fpm-fastcgi.conf"
```

Этот пакет и `lighttpd-fastcgi` вместе не ставят: оба кладут ссылку `/usr/lib64/lighttpd/mod_fastcgi.so`.

## Сборка

Из этого каталога:

```
docker build -t php-7.4-cve-lighttpd:centos7.4 .
```

Сборка проверяет оба варианта. Для варианта с php-fpm нужен уже собранный образ `php-7.4-cve-fpm:centos7.4`. Ответ страницы в обоих случаях: `ok 7.4.33 OpenSSL 1.1.1`.

Забрать RPM:

```
docker create --name lighttpd-fastcgi-rpm php-7.4-cve-lighttpd:centos7.4
docker cp lighttpd-fastcgi-rpm:/rpms/. .
docker rm lighttpd-fastcgi-rpm
```

Готовые пакеты этой сборки лежат в `dist/`. Каталог `dist` в контекст `docker build` не входит.

На сервере с `lighttpd-1.4.54-1.el7`, без пакета php-fpm:

```
yum localinstall lighttpd-fastcgi-1.4.54-3.el7.cve.x86_64.rpm
```

Рядом с `php-fpm-7.4.33-17.el7.cve`:

```
yum localinstall lighttpd-fastcgi-fpm-1.4.54-3.el7.cve.x86_64.rpm
```

Проверка CGI-пакета:

```
/opt/php-7.4.cve/bin/php-cgi -v
nm -D /opt/php-7.4.cve/bin/php-cgi | grep zend_mm_safe_error_ex
readelf -d /opt/php-7.4.cve/bin/php-cgi | grep 'libssl.so.1.1'
```

Патч отключает session upload progress в коде. `ini_get('session.upload_progress.enabled')` при этом может вернуть 1.
