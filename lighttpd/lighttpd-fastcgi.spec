Name:           lighttpd-fastcgi
Version:        1.4.54
Release:        3.el7.cve
Summary:        FastCGI module for lighttpd and patched PHP CGI
License:        BSD and PHP and Zend
URL:            https://www.lighttpd.net/
BuildArch:      x86_64
%define __check_files %{nil}
%global debug_package %{nil}

Requires:       lighttpd = 1.4.54-1.el7
Requires:       spawn-fcgi
Requires:       openssl11-libs
Requires:       libzip5
Requires:       libzstd
Requires:       oniguruma
Requires:       libsodium
Requires:       libwebp

Conflicts:      php-fpm >= 7.4.33-17.el7.cve
Conflicts:      lighttpd-fastcgi-fpm

Provides:       php = 7.4.33-17.el7.cve
Provides:       php-cli = 7.4.33-17.el7.cve
Provides:       php-common = 7.4.33-17.el7.cve
Provides:       php-gd = 7.4.33-17.el7.cve
Provides:       php-mbstring = 7.4.33-17.el7.cve
Provides:       php-mysqlnd = 7.4.33-17.el7.cve
Provides:       php-opcache = 7.4.33-17.el7.cve
Provides:       php-xml = 7.4.33-17.el7.cve

Obsoletes:      php < 7.4.33-17.el7.cve
Obsoletes:      php-cli < 7.4.33-17.el7.cve
Obsoletes:      php-common < 7.4.33-17.el7.cve
Obsoletes:      php-fpm < 7.4.33-17.el7.cve
Obsoletes:      php-gd < 7.4.33-17.el7.cve
Obsoletes:      php-mbstring < 7.4.33-17.el7.cve
Obsoletes:      php-mysqlnd < 7.4.33-17.el7.cve
Obsoletes:      php-opcache < 7.4.33-17.el7.cve
Obsoletes:      php-xml < 7.4.33-17.el7.cve
Obsoletes:      php-pecl-zip < 7.4.33-17.el7.cve
Obsoletes:      php-sodium < 7.4.33-17.el7.cve
Obsoletes:      php-ldap < 7.4.33-17.el7.cve
Obsoletes:      php-process < 7.4.33-17.el7.cve

%description
Replacement for the EPEL lighttpd-fastcgi 1.4.54-1.el7 module.
mod_fastcgi.so is built from lighttpd 1.4.54. The PHP CVE-2026-109618 and
CVE-2026-109619 backport is in /opt/php-7.4.cve/bin/php-cgi.
PHP files live under /opt/php-7.4.cve. This package conflicts with php-fpm
7.4.33-17.el7.cve because both own that prefix. Install lighttpd-fastcgi-fpm
instead when php-fpm is already installed.

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}
cp -a /php-root/. %{buildroot}/

%files -f /php-files.list
%defattr(-,root,root,-)

%changelog
* Tue Oct 27 2026 php-7.4.cve <php-7.4.cve@localhost> - 1.4.54-3.el7.cve
- Install patched PHP CGI and mod_fastcgi.so under /opt/php-7.4.cve
* Tue Oct 27 2026 php-7.4.cve <php-7.4.cve@localhost> - 1.4.54-2.el7.cve
- Rebuild lighttpd-fastcgi 1.4.54 with PHP 7.4.33 CGI patched for CVE-2026-109618 and CVE-2026-109619
