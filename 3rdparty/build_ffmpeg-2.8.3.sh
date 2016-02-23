#!/bin/bash
set -e

current_dir=$(cd ../; pwd -P)
build_dir="${current_dir}/_build"
release_dir="${current_dir}/_release"
echo "start to build the tools for transcode system(current_dir: ${current_dir}, build_dir: ${build_dir}, release_dir: ${release_dir})..."

mkdir -p ${build_dir}
mkdir -p ${release_dir}
cp -rf ffmpeg-2.8.3.tar.gz ${build_dir}


export PKG_CONFIG_PATH=${PKG_CONFIG_PATH}:${release_dir}/lib/pkgconfig


# build ffmpeg
pushd ${build_dir} 
if ! [ -e "ffmpeg-2.8.3" ]
then
    echo "########## build ffmepg begin ##########"
    set -x
    tar xf ffmpeg-2.8.3.tar.gz

    pushd ffmpeg-2.8.3 

    # export the dir to enable the build command canbe use.  --disable-pthreads --extra-libs=-lpthread --enable-gpl
    export ffmpeg_exported_release_dir=${release_dir}
    echo ${ffmpeg_exported_release_dir}/include
    echo ${ffmpeg_exported_release_dir}/lib
./configure --prefix=${release_dir} --cc=$CC \
--extra-cflags="-I${ffmpeg_exported_release_dir}/include" --extra-ldflags="-L${ffmpeg_exported_release_dir}/lib -lm " \
--disable-pthreads --extra-libs=-lpthread --enable-gpl \
--enable-static --enable-nonfree \
--enable-version3 

    echo "ffmpeg begin make"
    make
    make install
    popd
    touch ffmpeg-2.8.3
    echo "########## ffmpeg ok ##########"
else
    echo "########## ffmpeg has been installed ##########"
fi
popd


