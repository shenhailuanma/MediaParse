#!/bin/bash

FFMPEG_LIBS_DIR=../../_release/lib
FFMPEG_INCLUDE_DIR=../../_release/include
TARGET=mparser
SRC_FILES="mparser.c media_capture.c"

echo SRC_FILES:
echo ${SRC_FILES}

gcc -o $TARGET $SRC_FILES -I$FFMPEG_INCLUDE_DIR \
../../_release/lib/libavformat.a ../../_release/lib/libavcodec.a \
../../_release/lib/libavutil.a ../../_release/lib/libswscale.a \
../../_release/lib/libswresample.a ../../_release/lib/libavfilter.a \
../../_release/lib/libhiredis.a \
-lpthread -ldl -lrt -lm -lz -lbz2 



