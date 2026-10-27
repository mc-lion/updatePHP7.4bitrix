# php-fpm — замена пакета из репозитория

Пакет `php-fpm-7.4.33-17.el7.cve`. Это не сборка Remi SCL: префикс `/opt/php-7.4.cve`, и файлы PHP лежат внутри него.

```
/opt/php-7.4.cve/bin/php
/opt/php-7.4.cve/sbin/php-fpm
/opt/php-7.4.cve/etc/php.ini
/opt/php-7.4.cve/etc/php.d/*.ini
/opt/php-7.4.cve/etc/php-fpm.conf
/opt/php-7.4.cve/etc/php-fpm.d/www.conf
/opt/php-7.4.cve/var/log/php-fpm/error.log
/opt/php-7.4.cve/var/run/php-fpm.pid
/opt/php-7.4.cve/var/lib/php/session
```

`/usr/lib/systemd/system/php-fpm.service` — ссылка на `/opt/php-7.4.cve/lib/systemd/system/php-fpm.service`. Других файлов вне префикса пакет не ставит.

Пул `www` слушает `127.0.0.1:9000`, пользователь и группа `apache`. Расширения те же, что у модуля Apache, и вшиты в бинарник: opcache, mbstring, calendar, exif, pcntl, shmop, sockets, openssl, zlib, bz2, readline, gettext, mysqli (mysqlnd), sodium, zip, ldap, pspell, curl, gd (jpeg, freetype, webp). Отдельные `.so` из Remi к этому бинарнику не подходят: патч меняет заголовки Zend.

Сборка тянет OpenSSL 1.1.1 (`openssl11`), `libzip.so.5`, oniguruma, libwebp. OPcache подключается строкой `zend_extension=opcache.so`: каталог расширений тоже под `/opt/php-7.4.cve`.

## Сборка

Из этого каталога:

```
docker build -t php-7.4-cve-fpm:centos7.4 .
```

RPM лежит в образе в `/rpms/`. Забрать его:

```
docker create --name php-fpm-rpm php-7.4-cve-fpm:centos7.4
docker cp php-fpm-rpm:/rpms/. .
docker rm php-fpm-rpm
```

Готовый пакет этой сборки: `dist/php-fpm-7.4.33-17.el7.cve.x86_64.rpm`. Каталог `dist` в контекст `docker build` не входит.

## Установка на CentOS 7.4

На сервере нужны репозитории base/updates/extras/epel и remi-safe (оттуда берётся `libzip5`; вместе с ним ставится `libzstd`). Дальше:

```
yum localinstall php-fpm-7.4.33-17.el7.cve.x86_64.rpm
systemctl daemon-reload
systemctl enable --now php-fpm
```

Пакет объявляет `Provides` и `Obsoletes` для `php`, `php-cli`, `php-common`, `php-fpm`, `php-gd`, `php-mbstring`, `php-mysqlnd`, `php-opcache`, `php-pdo`, `php-xml`, `php-json`, `php-sodium`, `php-ldap`, `php-pspell`, `php-process`, `php-zip`, `php-pecl-zip`, `php-devel`, `php-dbg` со версией ниже `7.4.33-17.el7.cve`. `yum localinstall` снимет эти пакеты Remi. Бинарник после этого — `/opt/php-7.4.cve/bin/php`, не `/usr/bin/php`.

Конфиги `php.ini`, `php-fpm.conf`, `www.conf` и `10-opcache.ini` помечены `%config(noreplace)`: при обновлении уже изменённый файл на сервере не перезаписывается.

Юнит systemd: `Type=notify`, `ExecStart=/opt/php-7.4.cve/sbin/php-fpm --nodaemonize --fpm-config /opt/php-7.4.cve/etc/php-fpm.conf`. В `php-fpm.conf` стоит `daemonize = no`.

Проверка:

```
/opt/php-7.4.cve/bin/php -v
/opt/php-7.4.cve/bin/php -r 'echo OPENSSL_VERSION_TEXT, "\n";'
/opt/php-7.4.cve/sbin/php-fpm -t
nm -D /opt/php-7.4.cve/sbin/php-fpm | grep zend_mm_safe_error_ex
readelf -d /opt/php-7.4.cve/bin/php | grep 'libssl.so.1.1'
```

В `ldd` может быть ещё `libssl.so.10`: его тянут libcurl и openldap. Сам PHP собран на `libssl.so.1.1`.

Патч отключает session upload progress в коде. `ini_get('session.upload_progress.enabled')` при этом может вернуть 1.
