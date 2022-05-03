ALTER USER 'root'@'%' IDENTIFIED BY 'fhn1C1293cSasd2';
ALTER USER 'mysql'@'%' IDENTIFIED BY 'z8zce3Ct34uabtNo';
CREATE DATABASE atfield DEFAULT CHARSET utf8 COLLATE utf8_general_ci;
GRANT ALL privileges on atfield.* to 'mysql';
flush privileges;
