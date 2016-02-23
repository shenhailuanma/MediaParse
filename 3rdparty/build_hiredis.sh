#!/bin/bash
set -e

current_dir=$(cd ../; pwd -P)
build_dir="${current_dir}/_build"
release_dir="${current_dir}/_release"
echo "start to build the tools for transcode system(current_dir: ${current_dir}, build_dir: ${build_dir}, release_dir: ${release_dir})..."

mkdir -p ${build_dir}
mkdir -p ${release_dir}
mkdir -p ${release_dir}/lib
mkdir -p ${release_dir}/include

cp -rf hiredis-master.zip ${build_dir}

export PKG_CONFIG_PATH=${PKG_CONFIG_PATH}:${release_dir}/lib/pkgconfig

# build redis
pushd ${build_dir} 
if ! [ -e "hiredis" ]
then
    echo "########## build hiredis begin ##########"
    set -x
    unzip hiredis-master.zip

    pushd hiredis-master 

    echo "hiredis begin make"
    make
    cp -rf libhiredis.a    ${release_dir}/lib
    cp -rf *.h       ${release_dir}/include

    popd
    touch hiredis
    echo "########## hiredis ok ##########"
else
    echo "########## hiredis has been installed ##########"
fi
popd