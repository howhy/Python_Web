#!/bin/bash
arrsoft=(gcc
        gcc-c++
        openssl-devel
		gd-devel
		libjpeg-devel
		libpng-devel
		php-gd
		pcre-devel
        )
for soft in ${arrsoft[@]}
do
 if [ ! `rpm -qa $soft` ];then
        yum install -y $soft
 fi
done
[ ! -e /opt/local ] && mkdir /opt/local
useradd -M -s /sbin/nologin nginx
cd /opt/software
wget http://nginx.org/download/nginx-1.10.3.tar.gz
tar xf nginx-1.10.3.tar.gz 
cd nginx-1.10.3
./configure --prefix=/opt/local/nginx-1.10.3 --user=nginx --group=nginx --with-http_stub_status_module --with-http_ssl_module --with-http_realip_module --with-http_gzip_static_module 
ln -s /opt/local/nginx-1.10.3 /opt/local/nginx
make && make install
#chown -R nginx. /opt/local/nginx*
rm -f /opt/local/nginx/conf/nginx.conf
mkdir -p /opt/local/nginx/conf/vhost
cp /opt/software/nginx.conf /opt/local/nginx/conf/
cp /opt/software/default.conf /opt/local/nginx/conf/vhost/
mkdir /opt/website

