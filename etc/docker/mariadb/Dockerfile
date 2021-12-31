FROM mariadb:latest

ADD scripts/privileges.sql /docker-entrypoint-initdb.d/privileges.sql

CMD ["mysqld"]