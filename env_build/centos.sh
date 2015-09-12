
# compile and build tools
yum -y install autoconf automake make libtool patch pkgconfig zip unzip gcc-c++ cmake


# others
yum -y install openssl-devel alsa-lib-devel bzip2-devel db4-devel mysql-devel libevent-devel



# ffmpeg need
# yasm
tar zxf tools/yasm-1.2.0.tar.gz -C /tmp
pushd /tmp/yasm-1.2.0
./configure --prefix=/usr
make 
make install
popd