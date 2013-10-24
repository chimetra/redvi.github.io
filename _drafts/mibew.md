mysql> CREATE DATABASE mibew_db;
Query OK, 1 row affected (0.00 sec)

mysql> SHOW DATABASES;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| mibew_db           |
| mysql              |
| wordpress          |
+--------------------+
4 rows in set (0.00 sec)

mysql> CREATE USER 'mibew'@'localhost' IDENTIFIED BY 'mibew';
Query OK, 0 rows affected (0.00 sec)

mysql> GRANT ALL PRIVILEGES ON mibew_db.* TO 'mibew'@'localhost';
Query OK, 0 rows affected (0.00 sec)

mysql> FLUSH PRIVILEGES;
Query OK, 0 rows affected (0.00 sec)

```php
# mibew/libs/config.php
 *  Application path on server
 */
$mibewroot = "/mibew";

/*
 *  Internal encoding
 */
$mibew_encoding = "utf-8";

/*
 *  MySQL Database parameters
 */
$mysqlhost = "localhost";
$mysqldb = "mibew_db";
$mysqllogin = "mibew";
$mysqlpass = "mibew";
$mysqlprefix = "";

$dbencoding = "utf8";
$force_charset_in_connection = true;

/*
 *  Mailbox
 */
$mibew_mailbox = "mibew@yourdomain.com";
$mail_encoding = "utf-8";

/*
 *  Locales
 */
$home_locale = "en"; /* native name will be used in this locale */
$default_locale = "en"; /* if user does not provide known lang */
```

redvi@gentoo ~www/localhost/htdocs/mibew % ls locales
en/  names/  ru/
