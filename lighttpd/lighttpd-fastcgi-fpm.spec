Name:           lighttpd-fastcgi-fpm
Version:        1.4.54
Release:        3.el7.cve
Summary:        lighttpd FastCGI module for the php-fpm package under /opt/php-7.4.cve
License:        BSD and PHP and Zend
URL:            https://www.lighttpd.net/
BuildArch:      x86_64
%define __check_files %{nil}
%global debug_package %{nil}

Requires:       lighttpd = 1.4.54-1.el7
Requires:       php-fpm = 7.4.33-17.el7.cve

Conflicts:      lighttpd-fastcgi >= 1.4.54-3.el7.cve
Obsoletes:      lighttpd-fastcgi < 1.4.54-3.el7.cve

%description
FastCGI module for an already installed php-fpm 7.4.33-17.el7.cve.
It does not ship a second PHP tree. mod_fastcgi.so and the lighttpd
fragment live under /opt/php-7.4.cve and connect to 127.0.0.1:9000.
/usr/lib64/lighttpd/mod_fastcgi.so and the file in /etc/lighttpd/conf.d
are symlinks into that prefix.

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}
cp -a /php-root-fpm/. %{buildroot}/

%files -f /php-files-fpm.list
%defattr(-,root,root,-)

%changelog
* Tue Oct 27 2026 php-7.4.cve <php-7.4.cve@localhost> - 1.4.54-3.el7.cve
- Add a lighttpd FastCGI package that installs next to php-fpm
