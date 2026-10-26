/*
   +----------------------------------------------------------------------+
   | PHP Version 7                                                        |
   +----------------------------------------------------------------------+
   | Copyright (c) The PHP Group                                          |
   +----------------------------------------------------------------------+
   | This source file is subject to version 3.01 of the PHP license,      |
   | that is bundled with this package in the file LICENSE, and is        |
   | available through the world-wide-web at the following url:           |
   | http://www.php.net/license/3_01.txt                                  |
   | If you did not receive a copy of the PHP license and are unable to   |
   | obtain it through the world-wide-web, please send a note to          |
   | license@php.net so we can mail you a copy immediately.               |
   +----------------------------------------------------------------------+
   | Author: Stig Sæther Bakken <ssb@php.net>                             |
   +----------------------------------------------------------------------+
*/

#define CONFIGURE_COMMAND " './configure'  '--prefix=/opt/php-7.4.cve' '--with-libdir=lib64' '--with-config-file-path=/etc/php-7.4.cve' '--with-config-file-scan-dir=/etc/php-7.4.cve/php.d' '--with-apxs2=/usr/bin/apxs' '--disable-cgi' '--disable-phpdbg' '--without-pear' '--enable-opcache' '--enable-mbstring' '--enable-calendar' '--enable-exif' '--enable-pcntl' '--enable-shmop' '--enable-sockets' '--with-openssl' '--with-zlib' '--with-bz2' '--with-readline' '--with-gettext' '--enable-mysqlnd' '--with-mysqli=mysqlnd' '--without-sqlite3' '--without-pdo-sqlite' '--with-sodium' '--with-zip' '--with-ldap' '--with-pspell' '--with-curl' '--enable-gd' '--with-webp' '--with-jpeg' '--with-freetype'"
#define PHP_ODBC_CFLAGS	""
#define PHP_ODBC_LFLAGS		""
#define PHP_ODBC_LIBS		""
#define PHP_ODBC_TYPE		""
#define PHP_OCI8_DIR			""
#define PHP_OCI8_ORACLE_VERSION		""
#define PHP_PROG_SENDMAIL	"/usr/sbin/sendmail"
#define PEAR_INSTALLDIR         ""
#define PHP_INCLUDE_PATH	".:"
#define PHP_EXTENSION_DIR       "/opt/php-7.4.cve/lib/php/extensions/no-debug-non-zts-20190902"
#define PHP_PREFIX              "/opt/php-7.4.cve"
#define PHP_BINDIR              "/opt/php-7.4.cve/bin"
#define PHP_SBINDIR             "/opt/php-7.4.cve/sbin"
#define PHP_MANDIR              "/opt/php-7.4.cve/php/man"
#define PHP_LIBDIR              "/opt/php-7.4.cve/lib/php"
#define PHP_DATADIR             "/opt/php-7.4.cve/share/php"
#define PHP_SYSCONFDIR          "/opt/php-7.4.cve/etc"
#define PHP_LOCALSTATEDIR       "/opt/php-7.4.cve/var"
#define PHP_CONFIG_FILE_PATH    "/etc/php-7.4.cve"
#define PHP_CONFIG_FILE_SCAN_DIR    "/etc/php-7.4.cve/php.d"
#define PHP_SHLIB_SUFFIX        "so"
#define PHP_SHLIB_EXT_PREFIX    ""
