# PHP 7.4.33-fpm + CVE-2026-109618 / CVE-2026-109619
# Пакет php-fpm: весь префикс /opt/php-7.4.cve.
FROM docker.io/library/centos:7.4.1708 AS builder

RUN rm -rf /etc/yum.repos.d/* /etc/yum/pluginconf.d/* \
    && sed -i 's/^plugins=.*/plugins=0/' /etc/yum.conf

COPY CentOS-Vault.repo epel.repo remi-libzip5.repo /etc/yum.repos.d/

RUN yum install -y --disablerepo='*' --enablerepo=base,updates,extras,epel,remi-safe,remi \
        gcc gcc-c++ make pkgconfig patch curl ca-certificates which \
        rpm-build redhat-rpm-config \
        libxml2-devel zlib-devel bzip2-devel libcurl-devel \
        libpng-devel libjpeg-turbo-devel freetype-devel libwebp-devel \
        readline-devel libsodium-devel openldap-devel aspell-devel \
        openssl11-devel libzip5-devel oniguruma-devel \
        systemd-devel libacl-devel \
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
COPY php-fpm.conf www.conf php-fpm.service 10-opcache.ini php-fpm.spec /usr/src/pkg/

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
        --sysconfdir=/opt/php-7.4.cve/etc \
        --localstatedir=/opt/php-7.4.cve/var \
        --with-config-file-path=/opt/php-7.4.cve/etc \
        --with-config-file-scan-dir=/opt/php-7.4.cve/etc/php.d \
        --with-libdir=lib64 \
        --enable-fpm \
        --with-fpm-user=apache \
        --with-fpm-group=apache \
        --with-fpm-systemd \
        --with-fpm-acl \
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
    getent group apache >/dev/null || groupadd -r apache; \
    getent passwd apache >/dev/null || useradd -r -g apache -d /usr/share/httpd -s /sbin/nologin apache; \
    make install; \
    prefix=/opt/php-7.4.cve; \
    php=$prefix/bin/php; \
    ext=$($prefix/bin/php-config --extension-dir); \
    install -d \
        $prefix/etc/php.d \
        $prefix/etc/php-fpm.d \
        $prefix/var/log/php-fpm \
        $prefix/var/lib/php/session \
        $prefix/var/run \
        $prefix/lib/systemd/system \
        $prefix/share/doc; \
    cp -a /usr/src/php-7.4.33/php.ini-production $prefix/etc/php.ini; \
    cp -a /usr/src/php-7.4.33/php.ini-production /usr/src/php-7.4.33/php.ini-development $prefix/lib/; \
    sed -i \
        -e 's|^;session.save_path = "/tmp"|session.save_path = "/opt/php-7.4.cve/var/lib/php/session"|' \
        $prefix/etc/php.ini; \
    printf '\ninclude_path = "."\n' >> $prefix/etc/php.ini; \
    cp -a /usr/src/pkg/php-fpm.conf $prefix/etc/php-fpm.conf; \
    cp -a /usr/src/pkg/www.conf $prefix/etc/php-fpm.d/www.conf; \
    cp -a /usr/src/pkg/10-opcache.ini $prefix/etc/php.d/10-opcache.ini; \
    cp -a /usr/src/pkg/php-fpm.service $prefix/lib/systemd/system/php-fpm.service; \
    mkdir -p /usr/lib/systemd/system; \
    ln -sfn $prefix/lib/systemd/system/php-fpm.service /usr/lib/systemd/system/php-fpm.service; \
    printf '%s\n' \
        'PHP 7.4.33' \
        'prefix /opt/php-7.4.cve' \
        'patch 712e60f9edfd03f0960fc4fc3c2c375f42b90aa2' \
        'CVE-2026-109618 GHSA-w8hw-w9fx-j79w' \
        'CVE-2026-109619 GHSA-6wmf-4rv5-p3rp' \
        > $prefix/share/doc/PATCHES.txt; \
    "$php" -v | grep -q '^PHP 7.4.33 '; \
    "$php" -i | grep -F 'Configuration File (php.ini) Path => /opt/php-7.4.cve/etc'; \
    "$php" -i | grep -F 'Scan this dir for additional .ini files => /opt/php-7.4.cve/etc/php.d'; \
    "$php" -i | grep -F "extension_dir => $ext => $ext"; \
    case "$ext" in /opt/php-7.4.cve/*) ;; *) echo "extension_dir outside prefix: $ext"; exit 1 ;; esac; \
    "$php" -r 'exit(strpos(OPENSSL_VERSION_TEXT, "OpenSSL 1.1.1") === 0 ? 0 : 1);'; \
    "$php" -r 'exit(ini_get("session.save_path")==="/opt/php-7.4.cve/var/lib/php/session" ? 0 : 1);'; \
    "$php" -r 'exit(ini_get("include_path")==="." ? 0 : 1);'; \
    "$php" -m > /tmp/php-modules.txt; \
    for extname in calendar curl exif gd gettext ldap mbstring mysqli mysqlnd openssl pcntl pspell shmop sockets sodium zip zlib bz2; do \
        grep -qx "$extname" /tmp/php-modules.txt; \
    done; \
    "$php" -m | grep -q 'Zend OPcache'; \
    nm -D "$php" | grep -q ' zend_mm_safe_error_ex$'; \
    readelf -d "$php" | grep -q 'NEEDED.*libssl\.so\.1\.1'; \
    $prefix/sbin/php-fpm -t; \
    test ! -e /usr/bin/php; \
    test ! -e /etc/php.ini; \
    find "$prefix" -type f \( -name '*.1' -o -name '*.8' \) -exec gzip -n -f {} \;; \
    rm -rf /php-root; \
    mkdir -p /php-root/opt /php-root/usr/lib/systemd/system; \
    cp -a "$prefix" /php-root/opt/; \
    cp -a /usr/lib/systemd/system/php-fpm.service /php-root/usr/lib/systemd/system/php-fpm.service; \
    : > /php-files.list; \
    cd /php-root; \
    find . \( -type f -o -type l \) | sed 's|^\.||' | while read f; do \
        case "$f" in \
            /opt/php-7.4.cve/etc/php.ini|/opt/php-7.4.cve/etc/php-fpm.conf|/opt/php-7.4.cve/etc/php-fpm.d/www.conf|/opt/php-7.4.cve/etc/php.d/10-opcache.ini) \
                echo "%config(noreplace) $f" ;; \
            *) echo "$f" ;; \
        esac; \
    done >> /php-files.list; \
    find . -type d | sed 's|^\.||' | while read d; do \
        [ -n "$d" ] || continue; \
        case "$d" in \
            /opt|/usr|/usr/lib|/usr/lib/systemd|/usr/lib/systemd/system) \
                continue ;; \
            /opt/php-7.4.cve/var/log/php-fpm|/opt/php-7.4.cve/var/lib/php/session) \
                continue ;; \
        esac; \
        echo "%dir $d"; \
    done >> /php-files.list; \
    printf '%s\n' \
        '%attr(770,apache,root) %dir /opt/php-7.4.cve/var/log/php-fpm' \
        '%attr(770,apache,root) %dir /opt/php-7.4.cve/var/lib/php/session' \
        >> /php-files.list; \
    mkdir -p /root/rpmbuild/SPECS /rpms; \
    rpmbuild -bb /usr/src/pkg/php-fpm.spec; \
    cp -a /root/rpmbuild/RPMS/x86_64/php-fpm-*.rpm /rpms/; \
    rpm -qp --requires /rpms/php-fpm-*.rpm | grep -q 'libssl.so.1.1'; \
    rpm -qpl /rpms/php-fpm-*.rpm | grep -q '^/opt/php-7.4.cve/sbin/php-fpm$'; \
    leftover=$(rpm -qpl /rpms/php-fpm-*.rpm | grep -E '^/(usr|etc|var)/' | grep -v '^/usr/lib/systemd/system/php-fpm.service$' || true); \
    test -z "$leftover"

FROM docker.io/library/centos:7.4.1708

RUN rm -rf /etc/yum.repos.d/* /etc/yum/pluginconf.d/* \
    && sed -i 's/^plugins=.*/plugins=0/' /etc/yum.conf

COPY CentOS-Vault.repo epel.repo remi-libzip5.repo /etc/yum.repos.d/
COPY --from=builder /rpms /rpms

RUN yum localinstall -y --disablerepo='*' --enablerepo=base,updates,extras,epel,remi-safe,remi \
        /rpms/php-fpm-*.rpm \
    && yum clean all \
    && /opt/php-7.4.cve/bin/php -v | grep -q '^PHP 7.4.33 ' \
    && /opt/php-7.4.cve/bin/php -r 'exit(strpos(OPENSSL_VERSION_TEXT, "OpenSSL 1.1.1") === 0 ? 0 : 1);' \
    && /opt/php-7.4.cve/sbin/php-fpm -t \
    && test ! -e /usr/bin/php \
    && test ! -e /etc/php.ini \
    && test "$(readlink -f /usr/lib/systemd/system/php-fpm.service)" = /opt/php-7.4.cve/lib/systemd/system/php-fpm.service

CMD ["/opt/php-7.4.cve/sbin/php-fpm", "--nodaemonize", "--fpm-config", "/opt/php-7.4.cve/etc/php-fpm.conf"]
