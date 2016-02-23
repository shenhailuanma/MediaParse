#!/bin/bash
set -e

current_dir=$(cd ../; pwd -P)
build_dir="${current_dir}/_build"
release_dir="${current_dir}/_release"
echo "start to build the tools for transcode system(current_dir: ${current_dir}, build_dir: ${build_dir}, release_dir: ${release_dir})..."

mkdir -p ${build_dir}
mkdir -p ${release_dir}
mkdir -p ${release_dir}/bin
mkdir -p ${release_dir}/etc

cp -rf redis-3.0.6.tar.gz ${build_dir}

export PKG_CONFIG_PATH=${PKG_CONFIG_PATH}:${release_dir}/lib/pkgconfig

# build redis
pushd ${build_dir} 
if ! [ -e "redis-3.0.6" ]
then
    echo "########## build redis begin ##########"
    set -x
    tar xf redis-3.0.6.tar.gz

    pushd redis-3.0.6 

    echo "redis begin make"
    make
    cp -rf src/redis-server     ${release_dir}/bin
    cp -rf src/redis-cli        ${release_dir}/bin
    cp -rf redis.conf           ${release_dir}/etc
    popd
    touch redis-3.0.6 
    echo "########## redis ok ##########"
else
    echo "########## redis has been installed ##########"
fi
popd
