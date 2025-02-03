#!/bin/bash

REMOTE_USER="root"
REMOTE_PORT="22"
username="nagios"
password="1234"

#while IFS= read -r line; do
#  echo "$line"
#
#  sshpass -p "$password" ssh -o StrictHostKeyChecking=no -p "$REMOTE_PORT" "$REMOTE_USER@$line" "

#    echo "hello "
#  "
#
#done < hosts.txt
#
#exit 0


filename="hosts.txt"

# Read the file using cat and loop over the lines
for line in $(cat "$filename"); do
	echo "$line"
	sshpass -p "$password" ssh -o StrictHostKeyChecking=no -p "$REMOTE_PORT" "$REMOTE_USER@$line" "
		dpkg --configure -a
		#rm /var/lib/dpkg/lock-frontend
		apt-get update -y
		#rm /var/lib/dpkg/lock
		#apt-get install libmonitoring-plugin-perl -y
		#apt install libnagios-plugin-perl -y

		## we need to remove it if everythig works fine
		echo \"postfix postfix/mailname string yourdomain.com\" | debconf-set-selections
		echo \"postfix postfix/main_mailer_type select Internet Site\" | debconf-set-selections
		#apt-get install -y postfix


		apt-get install nagios-plugins-contrib -y
		#till this

		useradd -m -p $password $username
		mkdir -p /home/nagios/.ssh
		#mkdir -p /usr/lib/nagios/plugins/
		exit"

	sshpass -p $password scp /root/.ssh/authorized_keys2 $REMOTE_USER@$line:/root/.ssh/
	#sshpass -p $password scp /root/plugins/* $REMOTE_USER@$line:/usr/lib/nagios/plugins/


	ssh "$line" "
		#chmod a+x /usr/lib/nagios/plugins/*
		cd /usr/lib/nagios/plugins/
		./check_memory
		./check_uptime
		cd
		pwd
		cd /home/nagios/.ssh
		cp -rp /root/.ssh/authorized_keys2 .
		chown -R nagios:nagios *
		chmod -R og-rxw /home/nagios/.ssh
		ls -la
		exit"

	su - nagios -c "sshpass -p $password ssh -o StrictHostKeyChecking=no -p $REMOTE_PORT $REMOTE_USER@$line '
		echo \"in\"
		exit
	'"
	sleep 3



done
exit 0