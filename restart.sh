
echo "stopping nakedbear..."
sudo systemctl stop nakedbear

echo "starting nakedbear..."
sudo systemctl start nakedbear
sudo systemctl enable nakedbear

echo "restarting nginx..."
sudo systemctl restart nginx

echo "done!"
