Каталог `apache` — модуль httpd (`libphp-7.4.cve.so`). Собирается из этой папки: `docker build -t php-7.4-cve:centos7.4 .`

PHP 7.4.33 для CentOS 7.4 (BitrixVM) с исправлениями CVE-2026-109618 и CVE-2026-109619

Сборка заменяет PHP 7.4 из Remi: Remi больше не публикует сборки под EL7.
Образ: php-7.4-cve:centos7.4, база docker.io/library/centos:7.4.1708.

Исходники: официальный архив php-7.4.33.tar.gz и патч
712e60f9edfd03f0960fc4fc3c2c375f42b90aa2 («Avoid state corruption via bailout»,
минимальный бэкпорт команды PHP для ветки 7.4).
Контрольные суммы проверяются при сборке.

CVE-2026-109618 (GHSA-w8hw-w9fx-j79w) — повреждение памяти при OOM во время разбора запроса.
CVE-2026-109619 (GHSA-6wmf-4rv5-p3rp) — use-after-free из-за устаревшего состояния после фатальной ошибки.
Оба закрываются одним патчем. В бинарнике есть символ zend_mm_safe_error_ex.


Что зашито в бинарники и менять нельзя

  префикс              /opt/php-7.4.cve
  php.ini              /etc/php-7.4.cve/php.ini
  дополнительные ini   /etc/php-7.4.cve/php.d/*.ini
  каталог расширений   /opt/php-7.4.cve/lib/php/extensions/no-debug-non-zts-20190902
  CLI                  /opt/php-7.4.cve/bin/php

Модуль Apache ставится отдельно:

  /usr/lib64/httpd/modules/libphp-7.4.cve.so

Внутреннее имя модуля — php7_module. Файл называется libphp-7.4.cve.so, чтобы не затереть штатный libphp7.so.


Состав

Вкомпилированы: opcache, mbstring, calendar, exif, pcntl, shmop, sockets, openssl,
zlib, bz2, readline, gettext, mysqli (mysqlnd), sodium, zip, ldap, pspell, curl,
gd (jpeg, freetype, webp).

Вместе со стандартным набором 7.4 также есть ctype, date, dom, fileinfo, iconv,
json, Phar, posix, session, SimpleXML, tokenizer, xml, xmlreader, xmlwriter и PDO
без драйверов. pdo_mysql, pdo_sqlite, sqlite3, bcmath, intl, soap, ffi, cgi и phpdbg
не собирались.

Opcache — отдельный zend_extension, не статическая часть бинарника:

  /opt/php-7.4.cve/lib/php/extensions/no-debug-non-zts-20190902/opcache.so

pcntl и readline есть в CLI. В Apache pcntl не регистрируется: так устроен модуль.

Библиотеки:

  OpenSSL 1.1.1k     libssl.so.1.1, libcrypto.so.1.1   пакет openssl11-libs (EPEL)
  libzip 1.10.1      libzip.so.5                       пакет libzip5 (Remi safe)
  zstd               libzstd.so.1                      пакет libzstd (EPEL), зависимость libzip5
  oniguruma 6.8.2    libonig.so.5                      пакет oniguruma (EPEL)
  libwebp 0.3.0      libwebp.so.4                      базовый пакет CentOS 7.4
  libsodium 1.0.18   libsodium.so.23                   пакет libsodium (EPEL)

В EPEL 7 нет libzip новее 0.10.1, PHP 7.4 с ним не собирается. libzip5 берётся из
оставшихся репозиториев Remi (только пакеты libzip5 и libzip5-devel, не PHP).

libcurl и OpenLDAP CentOS 7 тянут в процесс libssl.so.10 и NSS. Это другие SONAME.
Сам PHP и модуль Apache в NEEDED ссылаются на libssl.so.1.1. Модуль в httpd при этом загружается.

Патч для 7.4 выключает session upload progress в коде. ini_get('session.upload_progress.enabled')
может по-прежнему возвращать 1, но функция не работает. Это поведение официального бэкпорта.


Сборка

Нужен Docker. Из каталога с Dockerfile:

  docker build -t php-7.4-cve:centos7.4 .

Репозитории CentOS 7.4 берутся с archive.kernel.org (centos-vault). vault.centos.org
отдаёт 403 на sqlite-метаданные yum. EPEL — архив archives.fedoraproject.org.
gpgcheck выключен: это архивы EOL-веток.

Сборка сама скачивает php-7.4.33.tar.gz, сверяет SHA-256, накладывает патч из patches/
и проверяет версию, пути ini, OpenSSL 1.1.1, список модулей, gd (jpeg/freetype/webp),
символ патча и загрузку модуля в Apache на порту 8888. Тестовый index.php после проверки удаляется.


Проверка образа

  docker run --rm php-7.4-cve:centos7.4 /opt/php-7.4.cve/bin/php -v
  docker run --rm php-7.4-cve:centos7.4 /opt/php-7.4.cve/bin/php -m
  docker run --rm -p 127.0.0.1:18888:8888 php-7.4-cve:centos7.4

Ожидается PHP 7.4.33 и OpenSSL 1.1.1k. Каталоги /etc/php-7.4.cve и php.d в образе пустые:
конфиги создаются на сервере.


Установка на сервер BitrixVM

На сервере уже работают nginx и Apache. nginx проксирует на Apache, порт по умолчанию 8888,
корень сайта /home/bitrix/www. Штатный httpd.conf BitrixVM не подменяется конфигом из образа.
Из образа забираются только дерево PHP и модуль.

Пакеты времени выполнения, до копирования файлов:

  yum install openssl11-libs oniguruma libsodium libzstd \
      libwebp libpng libjpeg-turbo freetype libxml2 libcurl \
      openldap aspell readline bzip2-libs

libzip5 в базовых репозиториях и в EPEL нет. На сервере нужен remi-safe с ограничением
includepkgs=libzip5 (файл remi-libzip5.repo в этом каталоге) и пакет libzip5.
libzip5-devel на рабочем сервере не нужен.

Копирование из образа:

  docker create --name php74cve-export php-7.4-cve:centos7.4
  docker cp php74cve-export:/opt/php-7.4.cve /opt/php-7.4.cve
  docker cp php74cve-export:/usr/lib64/httpd/modules/libphp-7.4.cve.so \
      /usr/lib64/httpd/modules/libphp-7.4.cve.so
  docker rm php74cve-export

Модуль в Apache (отдельный файл, например /etc/httpd/conf.modules.d/10-php-7.4.cve.conf):

  LoadModule php7_module /usr/lib64/httpd/modules/libphp-7.4.cve.so

Старый LoadModule на libphp7.so или модуль Remi нужно убрать, иначе Apache загрузит оба.
После замены:

  httpd -t
  httpd -M | grep php7_module
  systemctl restart httpd

Конфиги, фаза 3. Каталоги создаются на каждом сервере, содержимое берётся из локальных ini,
а не из образа:

  mkdir -p /etc/php-7.4.cve/php.d

В php.d для opcache достаточно относительного пути, extension_dir уже зашит:

  zend_extension=opcache.so

Строку extension_dir из конфигов Remi нужно удалить. Абсолютный zend_extension= на каталог
Remi загрузит старый opcache.so.


Проверка на сервере

  /opt/php-7.4.cve/bin/php -v
  /opt/php-7.4.cve/bin/php -i | grep -E 'Configuration File|Scan this dir|OpenSSL Library'
  /opt/php-7.4.cve/bin/php -m
  /opt/php-7.4.cve/bin/php -n -d zend_extension=opcache.so -m | grep -i opcache
  ldd /usr/lib64/httpd/modules/libphp-7.4.cve.so | grep -E 'libssl.so.1.1|libzip.so.5|libonig.so|libwebp.so.4'
  nm -D /opt/php-7.4.cve/bin/php | grep zend_mm_safe_error_ex

Ожидается:

  PHP 7.4.33
  Configuration File (php.ini) Path => /etc/php-7.4.cve
  Scan this dir for additional .ini files => /etc/php-7.4.cve/php.d
  OpenSSL Library Version => OpenSSL 1.1.1k
  NEEDED: libssl.so.1.1, libzip.so.5, libonig.so.5, libwebp.so.4
  символ zend_mm_safe_error_ex

Маркер патча в дереве: /opt/php-7.4.cve/PATCHES.txt.
