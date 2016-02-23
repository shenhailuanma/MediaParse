#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <fcntl.h>

#include <string.h>
#include <sys/socket.h>
#include <netinet/in.h>

#include <libavformat/avformat.h>
#include <libavcodec/avcodec.h>

#include <pthread.h>
#include "log.h"
#include "queue.h"
#include "media_capture.h"



int Media_capture_init(Media_capture_object * obj, Media_capture_params * params)
{
    if (obj == NULL || params == NULL){
        LOG_ERROR("obj == NULL || params == NULL\n");
        return MCAP_EINVAL;
    }

    int ret = MCAP_EOK;

    memset(obj, 0, sizeof(Media_capture_object));


    if (strlen(params->url) > 0){
        strcpy(obj->url, params->url);
    }else{
        LOG_ERROR("param url strlen == 0\n");
        return MCAP_EINVAL; 
    }

    // init the queue, not limit the queue size(set params NULL)
    ret = Queue_init(&(obj->queue), NULL);


    // init ffmpeg libs
    av_register_all();

    return ret;
}


static int init_media_context(Media_capture_object * obj)
{
    if (obj == NULL){
        LOG_ERROR("obj == NULL\n");
        return MCAP_EINVAL;
    }

    int ret = MCAP_EOK;

    AVFormatContext *ctx = NULL;

    // check the media url 
    if (strlen(obj->url) == 0){
        LOG_WARN("the media url is invalid.\n");
        return MCAP_EINVAL;
    }

    // open media url
    ret = avformat_open_input(&ctx, obj->url, NULL, NULL);
    if (ret < 0){
        LOG_ERROR("Could not open meida url:%s\n", obj->url);
        return MCAP_EFAIL;
    }

    ret = avformat_find_stream_info(ctx, NULL);
    if (ret < 0){
        LOG_ERROR("Could not find stream information\n");
        return MCAP_EFAIL;
    }

    av_dump_format(ctx, 0, obj->url, 0);

    obj->media_ctx = ctx;

    return ret;
}


int Media_capture_step(Media_capture_object * obj, AVPacket *pkt)
{
    if (obj == NULL || pkt == NULL){
        LOG_ERROR("obj == NULL || pkt == NULL\n");
        return MCAP_EINVAL;
    }

    int ret = MCAP_EOK;

    /* init the media_ctx */
    if(obj->media_ctx == NULL){
        ret = init_media_context(obj);
        if (ret < 0){
            LOG_ERROR("init_media_context error, return:%d\n", ret);
            return MCAP_EFAIL;
        }
    }

    av_init_packet(pkt);
    pkt->destruct = av_destruct_packet;

    ret = av_read_frame(obj->media_ctx, pkt);

    return ret;
}


static void Media_capture_thread(void * obj)
{
    if(obj == NULL){
        LOG_ERROR("obj == NULL\n");
        return;
    }


    Media_capture_object * handle = (Media_capture_object *)obj;

    /* init the media_ctx */
    if(handle->media_ctx == NULL){

    }


    while(1){
        sleep(1);
        LOG_DEBUG("Media_capture_thread sleep\n");
    }
}



int Media_capture_start(Media_capture_object * obj)
{
    if (obj == NULL){
        LOG_ERROR("obj == NULL\n");
        return MCAP_EINVAL;
    }

    int ret = MCAP_EOK;

    pthread_attr_t attr;
    pthread_t tid;

    pthread_attr_init(&attr);
    pthread_attr_setschedpolicy(&attr, SCHED_FIFO);
     
    pthread_create(&tid, &attr, (void *)Media_capture_thread, obj);
    LOG_DEBUG("pthread_create tid=%u\n", tid);
    obj->tid = tid;

    return ret;
}
