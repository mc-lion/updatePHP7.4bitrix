Name:           php-fpm
Version:        7.4.33
Release:        17.el7.cve
Summary:        PHP FastCGI Process Manager with CVE-2026-109618 and CVE-2026-109619
License:        PHP and Zend and BSD
URL:            https://www.php.net/
BuildArch:      x86_64
%define __check_files %{nil}
%global debug_package %{nil}

Requires:       openssl11-libs
Requires:       libzip5
Requires:       libzstd
Requires:       oniguruma
Requires:       libsodium
Requires:       libwebp
Requires:       libpng
Requires:       libjpeg-turbo
Requires:       freetype
Requires:       libxml2
Requires:       libcurl
Requires:       openldap
Requires:       aspell
Requires:       readline
Requires:       bzip2-libs

Provides:       php = %{version}-%{release}
Provides:       php-cli = %{version}-%{release}
Provides:       php-common = %{version}-%{release}
Provides:       php-gd = %{version}-%{release}
Provides:       php-mbstring = %{version}-%{release}
Provides:       php-mysqlnd = %{version}-%{release}
Provides:       php-opcache = %{version}-%{release}
Provides:       php-pdo = %{version}-%{release}
Provides:       php-xml = %{version}-%{release}
Provides:       php-json = %{version}-%{release}
Provides:       php-sodium = %{version}-%{release}
Provides:       php-ldap = %{version}-%{release}
Provides:       php-pspell = %{version}-%{release}
Provides:       php-process = %{version}-%{release}
Provides:       php-zip = %{version}-%{release}
Provides:       php-pecl-zip = %{version}-%{release}

Obsoletes:      php < %{version}-%{release}
Obsoletes:      php-cli < %{version}-%{release}
Obsoletes:      php-common < %{version}-%{release}
Obsoletes:      php-gd < %{version}-%{release}
Obsoletes:      php-mbstring < %{version}-%{release}
Obsoletes:      php-mysqlnd < %{version}-%{release}
Obsoletes:      php-opcache < %{version}-%{release}
Obsoletes:      php-pdo < %{version}-%{release}
Obsoletes:      php-xml < %{version}-%{release}
Obsoletes:      php-json < %{version}-%{release}
Obsoletes:      php-sodium < %{version}-%{release}
Obsoletes:      php-ldap < %{version}-%{release}
Obsoletes:      php-pspell < %{version}-%{release}
Obsoletes:      php-process < %{version}-%{release}
Obsoletes:      php-zip < %{version}-%{release}
Obsoletes:      php-pecl-zip < %{version}-%{release}
Obsoletes:      php-devel < %{version}-%{release}
Obsoletes:      php-dbg < %{version}-%{release}

%description
PHP 7.4.33 FastCGI Process Manager with the security backport
712e60f9edfd03f0960fc4fc3c2c375f42b90aa2 for CVE-2026-109618 and
CVE-2026-109619. Replaces the repository php 7.4 packages. Everything is
installed under /opt/php-7.4.cve: /opt/php-7.4.cve/bin/php,
/opt/php-7.4.cve/sbin/php-fpm, /opt/php-7.4.cve/etc/php.ini,
/opt/php-7.4.cve/etc/php.d and /opt/php-7.4.cve/etc/php-fpm.conf.
/usr/lib/systemd/system/php-fpm.service is a symlink into that tree.

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}
cp -a /php-root/. %{buildroot}/

%pre
getent group apache >/dev/null || groupadd -r apache
getent passwd apache >/dev/null || \
    useradd -r -g apache -d /usr/share/httpd -s /sbin/nologin apache

%files -f /php-files.list
%defattr(-,root,root,-)

%changelog
* Tue Oct 27 2026 php-7.4.cve <php-7.4.cve@localhost> - 7.4.33-17.el7.cve
- Install the repository replacement under /opt/php-7.4.cve
* Tue Oct 27 2026 php-7.4.cve <php-7.4.cve@localhost> - 7.4.33-16.el7.cve
- Replace repository php-fpm with PHP 7.4.33 plus CVE-2026-109618 and CVE-2026-109619
