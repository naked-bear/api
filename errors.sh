
echo -e "\n\n\n******** nginx ********\n\n\n"
cat /var/log/nginx/error.log

echo -e "\n\n\n******** flask ********\n\n\n"
cat /var/log/uwsgi/nakedbear.log
