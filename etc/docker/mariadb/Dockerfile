FROM mariadb:latest

ADD ./scripts/init.sql /docker-entrypoint-initdb.d/init.sql
ADD ./scripts/privileges.sql /docker-entrypoint-initdb.d/privileges.sql

CMD ["mysqld"]