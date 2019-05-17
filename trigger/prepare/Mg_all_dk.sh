#!/bin/bash
img_list=('hello-world' 'httpd' 'mysql')
#img_list=('hello-world')
argv=(''
	'-p 7080:80 '
	'-p 3307:3306 -e MYSQL_ROOT_PASSWORD=123456 ')

case $1 in 
	'rm') docker rm -f `docker ps -aq`
	;;
	'rmi') docker rmi -f `docker images -q`
	;;
	'stp') docker stop `docker ps -aq`
	;;
	'run') 
		for((i=o;i<${#img_list[*]};i++)); do 
			echo docker run ${img_list[i]}
			docker run ${argv[i]} -d ${img_list[i]} #>> run.id
		done
		#cut -c1-10 run.id > run.short_id
		#rm run.id
	;;
	'crt') 
		for((i=o;i<${#img_list[*]};i++)); do 
			echo docker create ${img_list[i]}
			docker create ${argv[i]} ${img_list[i]} #>> create.id
		done
		#cut -c1-10 create.id > crt.short_id
		#rm create.id
	;;
	'start') docker start `docker ps -aq`
	;;
	'pul') echo pulling ${img_list[*]}
		for i in ${img_list[*]}; do 
			docker pull $i
		done
	;;
	*) echo "usage: $0 [commond]"
		echo "commond: "
		echo " pul : pull all images without create containers."
		echo " crt : create all containers without runing.(if not exists, pull fist)"
		echo " run : run all containers(if not exists, pull fist)"
		echo " stp : stop all running containers."
		echo " start : start all stoped containers."
		echo " rm : [!]remove all containers."
		echo " rmi : [!]remove all images"
	;;
esac
