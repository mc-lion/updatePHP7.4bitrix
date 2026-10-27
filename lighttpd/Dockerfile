# lighttpd-fastcgi 1.4.54 + PHP 7.4.33 CGI с CVE-2026-109618 / CVE-2026-109619.
# PHP и модуль лежат в /opt/php-7.4.cve.
# lighttpd-fastcgi-fpm ставится рядом с пакетом php-fpm и свой PHP не приносит.
FROM docker.io/library/centos:7.4.1708 AS builder

RUN rm -rf /etc/yum.repos.d/* /etc/yum/pluginconf.d/* \
    && sed -i 's/^plugins=.*/plugins=0/' /etc/yum.conf

COPY CentOS-Vault.repo epel.repo remi-libzip5.repo /etc/yum.repos.d/

RUN yum install -y --disablerepo='*' --enablerepo=base,updates,extras,epel,remi-safe,remi \
        gcc gcc-c++ make pkgconfig patch curl ca-certificates which file \
        rpm-build redhat-rpm-config \
        pcre-devel zlib-devel \
        libxml2-devel bzip2-devel libcurl-devel \
        libpng-devel libjpeg-turbo-devel freetype-devel libwebp-devel \
        readline-devel libsodium-devel openldap-devel aspell-devel \
        openssl11-devel libzip5-devel oniguruma-devel \
    && yum clean all

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
    fi

COPY patches/712e60f9edfd03f0960fc4fc3c2c375f42b90aa2.patch /usr/src/cve-2026-109618-109619.patch
COPY lighttpd.ini php-fastcgi-cve.conf php-fpm-fastcgi.conf 10-opcache.ini lighttpd-fastcgi.spec lighttpd-fastcgi-fpm.spec /usr/src/pkg/

RUN set -eux; \
    echo '5fe57ca6ee96d59b36c6e0ca842843c50884f177bef1e85234cf669b577f5e48  /usr/src/cve-2026-109618-109619.patch' | sha256sum -c -; \
    curl -fL --retry 5 --retry-delay 2 -o /tmp/php-7.4.33.tar.gz https://www.php.net/distributions/php-7.4.33.tar.gz; \
    echo '5a2337996f07c8a097e03d46263b5c98d2c8e355227756351421003bea8f463e  /tmp/php-7.4.33.tar.gz' | sha256sum -c -; \
    tar -xzf /tmp/php-7.4.33.tar.gz -C /usr/src; \
    rm -f /tmp/php-7.4.33.tar.gz; \
    curl -fL --retry 5 --retry-delay 2 -o /tmp/lighttpd-1.4.54.tar.xz https://download.lighttpd.net/lighttpd/releases-1.4.x/lighttpd-1.4.54.tar.xz; \
    echo 'cf14cce2254a96d8fcb6d3181e1a3c29a8f832531c3e86ff6f2524ecda9a8721  /tmp/lighttpd-1.4.54.tar.xz' | sha256sum -c -; \
    tar -xJf /tmp/lighttpd-1.4.54.tar.xz -C /usr/src; \
    rm -f /tmp/lighttpd-1.4.54.tar.xz

WORKDIR /usr/src/php-7.4.33

RUN patch -p1 --forward --input=/usr/src/cve-2026-109618-109619.patch \
    && grep -q zend_mm_safe_error_ex Zend/zend_alloc.c \
    && ./configure \
        --prefix=/opt/php-7.4.cve \
        --sysconfdir=/opt/php-7.4.cve/etc \
        --localstatedir=/opt/php-7.4.cve/var \
        --with-config-file-path=/opt/php-7.4.cve/etc \
        --with-config-file-scan-dir=/opt/php-7.4.cve/etc/php.d \
        --with-libdir=lib64 \
        --enable-cgi \
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
    make -j"$jobs"; \
    cd /usr/src/lighttpd-1.4.54; \
    ./configure \
        --prefix=/usr \
        --libdir=/usr/lib64/lighttpd \
        --with-pcre \
        --with-zlib \
        --without-bzip2 \
        --without-fam \
        --without-gdbm \
        --without-geoip \
        --without-krb5 \
        --without-ldap \
        --without-lua \
        --without-memcached \
        --without-mysql \
        --without-openssl \
        --without-pam \
        --without-attr \
        --without-dbi \
        --without-libunwind \
        --without-libxml \
        --without-maxminddb \
        --without-pgsql \
        --without-sqlite \
        --without-uuid \
        --without-webdav-locks \
        --without-webdav-props \
        --without-wolfssl \
        --without-sasl \
        --without-libev; \
    make -j"$jobs"

RUN set -eux; \
    cd /usr/src/php-7.4.33; \
    make install; \
    prefix=/opt/php-7.4.cve; \
    getent group lighttpd >/dev/null || groupadd -r lighttpd; \
    getent passwd lighttpd >/dev/null || useradd -r -g lighttpd -d /var/www/lighttpd -s /sbin/nologin lighttpd; \
    php=$prefix/bin/php; \
    ext=$($prefix/bin/php-config --extension-dir); \
    case "$ext" in $prefix/*) ;; *) echo "extension_dir outside prefix: $ext"; exit 1 ;; esac; \
    install -d \
        $prefix/etc/php.d \
        $prefix/lib/lighttpd \
        $prefix/etc/lighttpd \
        $prefix/var/lib/php/session \
        $prefix/var/run/lighttpd \
        $prefix/share/doc \
        /usr/lib64/lighttpd \
        /etc/lighttpd/conf.d; \
    so=$(find /usr/src/lighttpd-1.4.54 -type f -name 'mod_fastcgi.so' | while read f; do \
        file "$f" | grep -q 'ELF' && echo "$f"; \
    done | head -1); \
    test -n "$so"; \
    cp -a "$so" $prefix/lib/lighttpd/mod_fastcgi.so; \
    ln -sfn $prefix/lib/lighttpd/mod_fastcgi.so /usr/lib64/lighttpd/mod_fastcgi.so; \
    cp -a /usr/src/php-7.4.33/php.ini-production $prefix/etc/php.ini; \
    cp -a /usr/src/php-7.4.33/php.ini-production /usr/src/php-7.4.33/php.ini-development $prefix/lib/; \
    sed -i \
        -e 's|^;session.save_path = "/tmp"|session.save_path = "/opt/php-7.4.cve/var/lib/php/session"|' \
        $prefix/etc/php.ini; \
    printf '\ninclude_path = "."\n' >> $prefix/etc/php.ini; \
    cp -a /usr/src/pkg/10-opcache.ini $prefix/etc/php.d/10-opcache.ini; \
    cp -a /usr/src/pkg/lighttpd.ini $prefix/etc/php.d/lighttpd.ini; \
    cp -a /usr/src/pkg/php-fastcgi-cve.conf $prefix/etc/lighttpd/php-fastcgi-cve.conf; \
    ln -sfn $prefix/etc/lighttpd/php-fastcgi-cve.conf /etc/lighttpd/conf.d/php-fastcgi-cve.conf; \
    chown lighttpd:lighttpd $prefix/var/run/lighttpd $prefix/var/lib/php/session; \
    printf '%s\n' \
        'lighttpd 1.4.54 mod_fastcgi.so' \
        'PHP 7.4.33 CGI' \
        'prefix /opt/php-7.4.cve' \
        'patch 712e60f9edfd03f0960fc4fc3c2c375f42b90aa2' \
        'CVE-2026-109618 GHSA-w8hw-w9fx-j79w' \
        'CVE-2026-109619 GHSA-6wmf-4rv5-p3rp' \
        > $prefix/share/doc/PATCHES.txt; \
    test -x $prefix/bin/php-cgi; \
    test ! -e /usr/bin/php; \
    test ! -e /usr/sbin/php-fpm; \
    "$php" -v | grep -q '^PHP 7.4.33 '; \
    $prefix/bin/php-cgi -v | grep -q '^PHP 7.4.33 '; \
    "$php" -i | grep -F 'Configuration File (php.ini) Path => /opt/php-7.4.cve/etc'; \
    "$php" -r 'exit(strpos(OPENSSL_VERSION_TEXT, "OpenSSL 1.1.1") === 0 ? 0 : 1);'; \
    "$php" -r 'exit(ini_get("session.save_path")==="/opt/php-7.4.cve/var/lib/php/session" ? 0 : 1);'; \
    "$php" -m > /tmp/php-modules.txt; \
    for extname in calendar curl exif gd gettext ldap mbstring mysqli mysqlnd openssl pcntl pspell shmop sockets sodium zip zlib bz2; do \
        grep -qx "$extname" /tmp/php-modules.txt; \
    done; \
    "$php" -m | grep -q 'Zend OPcache'; \
    nm -D $prefix/bin/php-cgi | grep -q ' zend_mm_safe_error_ex$'; \
    readelf -d $prefix/bin/php-cgi | grep -q 'NEEDED.*libssl\.so\.1\.1'; \
    file $prefix/lib/lighttpd/mod_fastcgi.so | grep -q 'ELF .* shared object'; \
    find "$prefix" -type f \( -name '*.1' -o -name '*.8' \) -exec gzip -n -f {} \;; \
    rm -rf /php-root; \
    mkdir -p /php-root/opt /php-root/usr/lib64/lighttpd /php-root/etc/lighttpd/conf.d; \
    cp -a "$prefix" /php-root/opt/; \
    cp -a /usr/lib64/lighttpd/mod_fastcgi.so /php-root/usr/lib64/lighttpd/mod_fastcgi.so; \
    cp -a /etc/lighttpd/conf.d/php-fastcgi-cve.conf /php-root/etc/lighttpd/conf.d/php-fastcgi-cve.conf; \
    : > /php-files.list; \
    cd /php-root; \
    find . \( -type f -o -type l \) | sed 's|^\.||' | while read f; do \
        case "$f" in \
            /opt/php-7.4.cve/etc/php.ini|/opt/php-7.4.cve/etc/php.d/10-opcache.ini|/opt/php-7.4.cve/etc/php.d/lighttpd.ini|/opt/php-7.4.cve/etc/lighttpd/php-fastcgi-cve.conf) \
                echo "%config(noreplace) $f" ;; \
            *) echo "$f" ;; \
        esac; \
    done >> /php-files.list; \
    find . -type d | sed 's|^\.||' | while read d; do \
        [ -n "$d" ] || continue; \
        case "$d" in \
            /opt|/usr|/usr/lib64|/usr/lib64/lighttpd|/etc|/etc/lighttpd|/etc/lighttpd/conf.d) \
                continue ;; \
            /opt/php-7.4.cve/var/lib/php/session|/opt/php-7.4.cve/var/run/lighttpd) \
                continue ;; \
        esac; \
        echo "%dir $d"; \
    done >> /php-files.list; \
    printf '%s\n' \
        '%attr(770,lighttpd,lighttpd) %dir /opt/php-7.4.cve/var/lib/php/session' \
        '%attr(770,lighttpd,lighttpd) %dir /opt/php-7.4.cve/var/run/lighttpd' \
        >> /php-files.list; \
    rm -rf /php-root-fpm; \
    mkdir -p \
        /php-root-fpm$prefix/lib/lighttpd \
        /php-root-fpm$prefix/etc/lighttpd \
        /php-root-fpm$prefix/etc/php.d \
        /php-root-fpm/usr/lib64/lighttpd \
        /php-root-fpm/etc/lighttpd/conf.d; \
    cp -a $prefix/lib/lighttpd/mod_fastcgi.so /php-root-fpm$prefix/lib/lighttpd/mod_fastcgi.so; \
    cp -a /usr/src/pkg/php-fpm-fastcgi.conf /php-root-fpm$prefix/etc/lighttpd/php-fpm-fastcgi.conf; \
    cp -a /usr/src/pkg/lighttpd.ini /php-root-fpm$prefix/etc/php.d/lighttpd.ini; \
    ln -sfn $prefix/lib/lighttpd/mod_fastcgi.so /php-root-fpm/usr/lib64/lighttpd/mod_fastcgi.so; \
    ln -sfn $prefix/etc/lighttpd/php-fpm-fastcgi.conf /php-root-fpm/etc/lighttpd/conf.d/php-fpm-fastcgi.conf; \
    : > /php-files-fpm.list; \
    cd /php-root-fpm; \
    find . \( -type f -o -type l \) | sed 's|^\.||' | while read f; do \
        case "$f" in \
            /opt/php-7.4.cve/etc/lighttpd/php-fpm-fastcgi.conf|/opt/php-7.4.cve/etc/php.d/lighttpd.ini) \
                echo "%config(noreplace) $f" ;; \
            *) echo "$f" ;; \
        esac; \
    done >> /php-files-fpm.list; \
    printf '%s\n' \
        '%dir /opt/php-7.4.cve/lib/lighttpd' \
        '%dir /opt/php-7.4.cve/etc/lighttpd' \
        >> /php-files-fpm.list; \
    mkdir -p /root/rpmbuild/SPECS /rpms; \
    rpmbuild -bb /usr/src/pkg/lighttpd-fastcgi.spec; \
    rpmbuild -bb /usr/src/pkg/lighttpd-fastcgi-fpm.spec; \
    cp -a /root/rpmbuild/RPMS/x86_64/lighttpd-fastcgi-*.rpm /rpms/; \
    test -f /rpms/lighttpd-fastcgi-1.4.54-3.el7.cve.x86_64.rpm; \
    test -f /rpms/lighttpd-fastcgi-fpm-1.4.54-3.el7.cve.x86_64.rpm; \
    rpm -qp --requires /rpms/lighttpd-fastcgi-1.4.54-3.el7.cve.x86_64.rpm | grep -q 'lighttpd = 1.4.54-1.el7'; \
    rpm -qp --requires /rpms/lighttpd-fastcgi-fpm-1.4.54-3.el7.cve.x86_64.rpm | grep -q 'php-fpm = 7.4.33-17.el7.cve'; \
    leftover=$(rpm -qpl /rpms/lighttpd-fastcgi-1.4.54-3.el7.cve.x86_64.rpm | grep -E '^/(usr|etc|var)/' | grep -v '^/usr/lib64/lighttpd/mod_fastcgi.so$' | grep -v '^/etc/lighttpd/conf.d/php-fastcgi-cve.conf$' || true); \
    test -z "$leftover"; \
    fpmfiles=$(rpm -qpl /rpms/lighttpd-fastcgi-fpm-1.4.54-3.el7.cve.x86_64.rpm); \
    echo "$fpmfiles" | grep -q '^/opt/php-7.4.cve/lib/lighttpd/mod_fastcgi.so$'; \
    echo "$fpmfiles" | grep -q '/opt/php-7.4.cve/bin/' && exit 1 || true

FROM php-7.4-cve-fpm:centos7.4 AS withfpm

COPY --from=builder /rpms/lighttpd-fastcgi-fpm-1.4.54-3.el7.cve.x86_64.rpm /rpms/

RUN set -eux; \
    yum install -y --disablerepo='*' --enablerepo=base,updates,extras,epel curl lighttpd; \
    rpm -q lighttpd | grep -q '^lighttpd-1.4.54-1.el7'; \
    rpm -q php-fpm | grep -q '^php-fpm-7.4.33-17.el7.cve'; \
    yum localinstall -y --disablerepo='*' --enablerepo=base,updates,extras,epel,remi-safe,remi \
        /rpms/lighttpd-fastcgi-fpm-1.4.54-3.el7.cve.x86_64.rpm; \
    rpm -q php-fpm | grep -q '^php-fpm-7.4.33-17.el7.cve'; \
    test ! -e /opt/php-7.4.cve/bin/php-cgi; \
    test "$(readlink -f /usr/lib64/lighttpd/mod_fastcgi.so)" = /opt/php-7.4.cve/lib/lighttpd/mod_fastcgi.so; \
    mkdir -p /var/www/html /var/log/lighttpd; \
    printf '%s\n' '<?php echo "ok ".PHP_VERSION." ".OPENSSL_VERSION_TEXT;' > /var/www/html/index.php; \
    chmod 644 /var/www/html/index.php; \
    printf '%s\n' \
        'server.document-root = "/var/www/html"' \
        'server.port = 8080' \
        'server.bind = "127.0.0.1"' \
        'server.username = "lighttpd"' \
        'server.groupname = "lighttpd"' \
        'server.errorlog = "/tmp/lighttpd-error.log"' \
        'server.modules = ( )' \
        'include "/etc/lighttpd/conf.d/php-fpm-fastcgi.conf"' \
        > /tmp/lighttpd-test.conf; \
    /opt/php-7.4.cve/sbin/php-fpm -t; \
    /opt/php-7.4.cve/sbin/php-fpm --nodaemonize --fpm-config /opt/php-7.4.cve/etc/php-fpm.conf & \
    echo $! > /tmp/fpm.pid; \
    lighttpd -t -f /tmp/lighttpd-test.conf; \
    lighttpd -D -f /tmp/lighttpd-test.conf & \
    echo $! > /tmp/lighttpd.pid; \
    ok=0; \
    for i in 1 2 3 4 5 6 7 8 9 10 11 12; do \
        if curl -fsS http://127.0.0.1:8080/index.php | tee /tmp/php-out | grep -q 'ok 7.4.33 OpenSSL 1.1.1'; then \
            ok=1; break; \
        fi; \
        sleep 1; \
    done; \
    kill "$(cat /tmp/lighttpd.pid)" "$(cat /tmp/fpm.pid)" || true; \
    if [ "$ok" != 1 ]; then cat /tmp/lighttpd-error.log || true; cat /opt/php-7.4.cve/var/log/php-fpm/error.log || true; cat /tmp/php-out || true; exit 1; fi; \
    touch /tested-fpm

FROM docker.io/library/centos:7.4.1708

RUN rm -rf /etc/yum.repos.d/* /etc/yum/pluginconf.d/* \
    && sed -i 's/^plugins=.*/plugins=0/' /etc/yum.conf

COPY CentOS-Vault.repo epel.repo remi-libzip5.repo /etc/yum.repos.d/
COPY --from=builder /rpms /rpms
COPY --from=withfpm /tested-fpm /tested-fpm

RUN set -eux; \
    yum install -y --disablerepo='*' --enablerepo=base,updates,extras,epel \
        lighttpd spawn-fcgi curl; \
    rpm -q lighttpd | grep -q '^lighttpd-1.4.54-1.el7'; \
    yum localinstall -y --disablerepo='*' --enablerepo=base,updates,extras,epel,remi-safe,remi \
        /rpms/lighttpd-fastcgi-1.4.54-3.el7.cve.x86_64.rpm; \
    yum clean all; \
    /opt/php-7.4.cve/bin/php -v | grep -q '^PHP 7.4.33 '; \
    /opt/php-7.4.cve/bin/php-cgi -v | grep -q '^PHP 7.4.33 '; \
    test ! -e /usr/bin/php; \
    test "$(readlink -f /usr/lib64/lighttpd/mod_fastcgi.so)" = /opt/php-7.4.cve/lib/lighttpd/mod_fastcgi.so; \
    test "$(readlink -f /etc/lighttpd/conf.d/php-fastcgi-cve.conf)" = /opt/php-7.4.cve/etc/lighttpd/php-fastcgi-cve.conf; \
    mkdir -p /var/www/html /var/log/lighttpd; \
    printf '%s\n' '<?php echo "ok ".PHP_VERSION." ".OPENSSL_VERSION_TEXT;' > /var/www/html/index.php; \
    chown lighttpd:lighttpd /var/www/html/index.php; \
    printf '%s\n' \
        'server.document-root = "/var/www/html"' \
        'server.port = 8080' \
        'server.bind = "127.0.0.1"' \
        'server.username = "lighttpd"' \
        'server.groupname = "lighttpd"' \
        'server.errorlog = "/tmp/lighttpd-error.log"' \
        'server.modules = ( )' \
        'include "/etc/lighttpd/conf.d/php-fastcgi-cve.conf"' \
        > /tmp/lighttpd-test.conf; \
    lighttpd -t -f /tmp/lighttpd-test.conf; \
    lighttpd -D -f /tmp/lighttpd-test.conf & \
    echo $! > /tmp/lighttpd.pid; \
    ok=0; \
    for i in 1 2 3 4 5 6 7 8 9 10 11 12; do \
        if curl -fsS http://127.0.0.1:8080/index.php | tee /tmp/php-out | grep -q 'ok 7.4.33 OpenSSL 1.1.1'; then \
            ok=1; break; \
        fi; \
        sleep 1; \
    done; \
    kill "$(cat /tmp/lighttpd.pid)" || true; \
    if [ "$ok" != 1 ]; then cat /tmp/lighttpd-error.log || true; cat /tmp/php-out || true; exit 1; fi; \
    rm -f /var/www/html/index.php /tmp/lighttpd-test.conf /tmp/php-out /tmp/lighttpd-error.log /tmp/lighttpd.pid

CMD ["/opt/php-7.4.cve/bin/php", "-v"]
