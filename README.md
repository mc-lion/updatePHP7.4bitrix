# PHP 7.4.33 с CVE-2026-109618 и CVE-2026-109619 для CentOS 7.4

Три самостоятельные сборки. У каждой свой Dockerfile, копия патча и файлы репозиториев. Команду `docker build` запускают из каталога сборки.

| Каталог | Что получается |
| --- | --- |
| [apache](apache/README.md) | Модуль httpd `libphp-7.4.cve.so`, префикс `/opt/php-7.4.cve` |
| [php-fpm](php-fpm/README.md) | Пакет `php-fpm`, префикс `/opt/php-7.4.cve` |
| [lighttpd](lighttpd/README.md) | `lighttpd-fastcgi` со своим PHP в `/opt/php-7.4.cve` и `lighttpd-fastcgi-fpm` для установки рядом с `php-fpm` |

`lighttpd-fastcgi` и `php-fpm` оба занимают `/opt/php-7.4.cve`, вместе их не ставят. Рядом с `php-fpm` ставится `lighttpd-fastcgi-fpm`: модуль lighttpd без второго дерева PHP.

Патч во всех трёх сборках один: `712e60f9edfd03f0960fc4fc3c2c375f42b90aa2`. Он закрывает CVE-2026-109618 и CVE-2026-109619 и отключает session upload progress в коде, даже если `session.upload_progress.enabled` в ini остаётся 1.
