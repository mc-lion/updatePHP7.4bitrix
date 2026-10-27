# PHP 7.4.33 + официальный бэкпорт CVE-2026-109618 / CVE-2026-109619
# для CentOS 7.4 (BitrixVM, nginx -> Apache :8888).
# Префикс /opt/php-7.4.cve зашит в бинарники.
FROM docker.io/library/centos:7.4.1708 AS builder

RUN rm -rf /etc/yum.repos.d/* /etc/yum/pluginconf.d/* \
    && sed -i 's/^plugins=.*/plugins=0/' /etc/yum.conf

COPY CentOS-Vault.repo epel.repo remi-libzip5.repo /etc/yum.repos.d/

RUN yum install -y --disablerepo='*' --enablerepo=base,updates,extras,epel,remi-safe,remi \
        gcc gcc-c++ make pkgconfig patch curl ca-certificates which \
        httpd httpd-devel \
        libxml2-devel zlib-devel bzip2-devel libcurl-devel \
        libpng-devel libjpeg-turbo-devel freetype-devel libwebp-devel \
        readline-devel libsodium-devel openldap-devel aspell-devel \
        openssl11-devel libzip5-devel oniguruma-devel \
    && yum clean all

# PHP 7.4 ищет pkg-config-модуль "openssl", EPEL отдаёт его как openssl11.
# openssl-devel (1.0.2) не ставим: его заголовки перебьют 1.1.1.
# У libjpeg-turbo 7.4 нет libjpeg.pc, GD ищет модуль по этому имени.
RUN set -eux; \
    ln -sfn openssl11.pc /usr/lib64/pkgconfig/openssl.pc; \
    pkg-config --modversion openssl | grep -q '^1.1.1'; \
    pkg-config --cflags openssl | grep -q openssl11; \
    test ! -e /usr/include/openssl/ssl.h; \
    if ! pkg-config --exists libjpeg; then \
        printf '%s\n' \
            'prefix=/usr' \
            'exec_prefix=${prefix}' \
            'libdir=${exec_prefix}/lib64' \
            'includedir=${prefix}/include' \
            '' \
            'Name: libjpeg' \
            'Description: libjpeg API from libjpeg-turbo' \
            'Version: 6.2' \
            'Libs: -L${libdir} -ljpeg' \
            'Cflags: -I${includedir}' \
            > /usr/lib64/pkgconfig/libjpeg.pc; \
    fi; \
    pkg-config --exists 'libzip >= 0.11'; \
    pkg-config --exists oniguruma; \
    pkg-config --exists libwebp; \
    pkg-config --exists libsodium; \
    pkg-config --exists freetype2; \
    pkg-config --exists libpng; \
    pkg-config --exists zlib

COPY patches/712e60f9edfd03f0960fc4fc3c2c375f42b90aa2.patch /usr/src/cve-2026-109618-109619.patch

RUN set -eux; \
    echo '5fe57ca6ee96d59b36c6e0ca842843c50884f177bef1e85234cf669b577f5e48  /usr/src/cve-2026-109618-109619.patch' | sha256sum -c -; \
    curl -fL --retry 5 --retry-delay 2 -o /tmp/php-7.4.33.tar.gz https://www.php.net/distributions/php-7.4.33.tar.gz; \
    echo '5a2337996f07c8a097e03d46263b5c98d2c8e355227756351421003bea8f463e  /tmp/php-7.4.33.tar.gz' | sha256sum -c -; \
    tar -xzf /tmp/php-7.4.33.tar.gz -C /usr/src; \
    rm -f /tmp/php-7.4.33.tar.gz

WORKDIR /usr/src/php-7.4.33

RUN patch -p1 --forward --input=/usr/src/cve-2026-109618-109619.patch \
    && grep -q zend_mm_safe_error_ex Zend/zend_alloc.c \
    && ./configure \
        --prefix=/opt/php-7.4.cve \
        --with-libdir=lib64 \
        --with-config-file-path=/etc/php-7.4.cve \
        --with-config-file-scan-dir=/etc/php-7.4.cve/php.d \
        --with-apxs2=/usr/bin/apxs \
        --disable-cgi \
        --disable-phpdbg \
        --without-pear \
        --enable-opcache \
        --enable-mbstring \
        --enable-calendar \
        --enable-exif \
        --enable-pcntl \
        --enable-shmop \
        --enable-sockets \
        --with-openssl \
        --with-zlib \
        --with-bz2 \
        --with-readline \
        --with-gettext \
        --enable-mysqlnd \
        --with-mysqli=mysqlnd \
        --without-sqlite3 \
        --without-pdo-sqlite \
        --with-sodium \
        --with-zip \
        --with-ldap \
        --with-pspell \
        --with-curl \
        --enable-gd \
        --with-webp \
        --with-jpeg \
        --with-freetype

RUN set -eux; \
    jobs="$(nproc)"; \
    if [ "$jobs" -gt 4 ]; then jobs=4; fi; \
    make -j"$jobs"

RUN set -eux; \
    make install; \
    test -f /usr/lib64/httpd/modules/libphp7.so; \
    mv /usr/lib64/httpd/modules/libphp7.so /usr/lib64/httpd/modules/libphp-7.4.cve.so; \
    rm -f /usr/lib64/httpd/modules/libphp7.la; \
    mkdir -p /opt/php-7.4.cve/lib/httpd; \
    cp -a /usr/lib64/httpd/modules/libphp-7.4.cve.so /opt/php-7.4.cve/lib/httpd/libphp-7.4.cve.so; \
    printf '%s\n' \
        'PHP 7.4.33' \
        'patch 712e60f9edfd03f0960fc4fc3c2c375f42b90aa2' \
        'CVE-2026-109618 GHSA-w8hw-w9fx-j79w' \
        'CVE-2026-109619 GHSA-6wmf-4rv5-p3rp' \
        > /opt/php-7.4.cve/PATCHES.txt; \
    php=/opt/php-7.4.cve/bin/php; \
    "$php" -v | grep -q '^PHP 7.4.33 '; \
    "$php" -i | grep -F 'Configuration File (php.ini) Path => /etc/php-7.4.cve'; \
    "$php" -i | grep -F 'Scan this dir for additional .ini files => /etc/php-7.4.cve/php.d'; \
    "$php" -r 'exit(strpos(OPENSSL_VERSION_TEXT, "OpenSSL 1.1.1") === 0 ? 0 : 1);'; \
    "$php" -m > /tmp/php-modules.txt; \
    for ext in calendar ctype curl date exif gd gettext iconv json ldap libxml mbstring mysqli mysqlnd openssl pcntl pcre pspell readline shmop sockets sodium xml zip zlib bz2; do \
        grep -qx "$ext" /tmp/php-modules.txt; \
    done; \
    "$php" -n -d zend_extension=opcache.so -m | grep -q 'Zend OPcache'; \
    "$php" -r 'foreach (["JPEG Support","FreeType Support","WebP Support"] as $k) { if (empty(gd_info()[$k])) { fwrite(STDERR, $k); exit(1);} } $im=imagecreatetruecolor(8,8); ob_start(); if(!imagejpeg($im)||!imagewebp($im)||!imagepng($im)) exit(1); ob_end_clean();'; \
    nm -D "$php" | grep -q ' zend_mm_safe_error_ex$'; \
    ldd "$php" > /tmp/php-ldd.txt; \
    for needle in libssl.so.1.1 libcrypto.so.1.1 libzip.so.5 libonig.so libwebp.so.4 libsodium.so libcurl.so libjpeg.so libpng libfreetype libldap libpspell libreadline libbz2 libzstd.so libxml2; do \
        grep -q "$needle" /tmp/php-ldd.txt; \
    done; \
    readelf -d "$php" | grep -q 'NEEDED.*libssl\.so\.1\.1'; \
    readelf -d /usr/lib64/httpd/modules/libphp-7.4.cve.so | grep -q 'NEEDED.*libssl\.so\.1\.1'

# Минимальный runtime того же CentOS 7.4, чтобы .so совпал с httpd/apr сервера.
FROM docker.io/library/centos:7.4.1708

RUN rm -rf /etc/yum.repos.d/* /etc/yum/pluginconf.d/* \
    && sed -i 's/^plugins=.*/plugins=0/' /etc/yum.conf

COPY CentOS-Vault.repo epel.repo remi-libzip5.repo /etc/yum.repos.d/

RUN yum install -y --disablerepo='*' --enablerepo=base,updates,extras,epel,remi-safe,remi \
        httpd \
        openssl11-libs \
        libzip5 \
        libzstd \
        oniguruma \
        libwebp \
        libpng \
        libjpeg-turbo \
        freetype \
        libsodium \
        libxml2 \
        libcurl \
        openldap \
        aspell \
        readline \
        bzip2-libs \
    && yum clean all \
    && mkdir -p /run/httpd /etc/php-7.4.cve/php.d /home/bitrix/www \
    && chown apache:apache /run/httpd /home/bitrix/www

COPY --from=builder /opt/php-7.4.cve /opt/php-7.4.cve
COPY --from=builder /usr/lib64/httpd/modules/libphp-7.4.cve.so /usr/lib64/httpd/modules/libphp-7.4.cve.so

RUN set -eux; \
    sed -i \
        -e 's/^Listen 80$/Listen 8888/' \
        -e 's|DocumentRoot "/var/www/html"|DocumentRoot "/home/bitrix/www"|' \
        -e 's|<Directory "/var/www/html">|<Directory "/home/bitrix/www">|' \
        /etc/httpd/conf/httpd.conf; \
    printf '%s\n' 'ServerName localhost' >> /etc/httpd/conf/httpd.conf; \
    printf '%s\n' 'LoadModule php7_module /usr/lib64/httpd/modules/libphp-7.4.cve.so' \
        > /etc/httpd/conf.modules.d/10-php-7.4.cve.conf; \
    printf '%s\n' \
        '<Directory "/home/bitrix/www">' \
        '    Options FollowSymLinks' \
        '    AllowOverride All' \
        '    Require all granted' \
        '</Directory>' \
        '<FilesMatch \.php$>' \
        '    SetHandler application/x-httpd-php' \
        '</FilesMatch>' \
        'DirectoryIndex index.php index.html' \
        > /etc/httpd/conf.d/php-7.4.cve.conf; \
    grep -q '^Listen 8888$' /etc/httpd/conf/httpd.conf; \
    grep -q 'DocumentRoot "/home/bitrix/www"' /etc/httpd/conf/httpd.conf; \
    printf '%s\n' '<?php echo "ok ".PHP_VERSION." ".OPENSSL_VERSION_TEXT, "\n";' > /home/bitrix/www/index.php; \
    httpd -t; \
    httpd -M 2>&1 | grep -q php7_module; \
    httpd -D FOREGROUND & \
    pid=$!; \
    ok=0; \
    for _ in 1 2 3 4 5 6 7 8 9 10; do \
        if curl -fsS http://127.0.0.1:8888/ | grep -q '^ok 7.4.33 OpenSSL 1.1.1'; then ok=1; break; fi; \
        sleep 1; \
    done; \
    kill "$pid" || true; \
    wait "$pid" || true; \
    test "$ok" = 1; \
    rm -f /home/bitrix/www/index.php

EXPOSE 8888

CMD ["/usr/sbin/httpd", "-D", "FOREGROUND"]
