@echo off
echo Importing tables into 'bibekdb' database...
mysql -u root -p bibekdb < "%~dp0attached_troops.sql"
mysql -u root -p bibekdb < "%~dp0kalidal_bn.sql"
mysql -u root -p bibekdb < "%~dp0leave_record_kalidal_bn.sql"
mysql -u root -p bibekdb < "%~dp0login_details.sql"
mysql -u root -p bibekdb < "%~dp0quote_list_log.sql"
echo All tables imported.
pause