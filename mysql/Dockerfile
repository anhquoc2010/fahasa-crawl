FROM mysql

ENV MYSQL_DATABASE=fahasadb
ENV MYSQL_USER=fahasa
ENV MYSQL_PASSWORD=123456
ENV MYSQL_ROOT_PASSWORD=123456

COPY ./mysql/init_db /docker-entrypoint-initdb.d/

EXPOSE 3306

CMD ["mysqld", "--default-authentication-plugin=mysql_native_password"]
