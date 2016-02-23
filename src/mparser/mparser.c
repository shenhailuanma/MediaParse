#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <fcntl.h>
#include <sys/time.h>
#include <string.h>


#include <libavformat/avformat.h>
#include <libavcodec/avcodec.h>
#include <libswscale/swscale.h>
#include <libavutil/common.h>

#include "log.h"
#include "queue.h"
#include "mparser.h"
#include "media_capture.h"

#include "hiredis.h"



static int parae_packet(AVPacket *pkt)
{
    
}


int main(int argc, char const *argv[])
{


    Queue_object   queue;
    Queue_object * Queue = &queue;

    int ret = 0;


    // test queue
    ret = Queue_init(Queue, NULL);
    LOG_INFO("Queue_init return:%d \n", ret);

    char * ptr ;
    ptr = (char *)malloc(sizeof(int));
    *ptr = 1;
    Queue_put(Queue, (char *)ptr);
    LOG_INFO("Queue_element_numbers:%d \n", Queue_element_numbers(Queue));

    ptr = (char *)malloc(sizeof(int));
    *ptr = 2;
    Queue_put(Queue, (char *)ptr);
    LOG_INFO("Queue_element_numbers:%d \n", Queue_element_numbers(Queue));

    ptr = (char *)malloc(sizeof(int));
    *ptr = 3;
    Queue_put(Queue, (char *)ptr);
    LOG_INFO("Queue_element_numbers:%d \n", Queue_element_numbers(Queue));

    ptr = Queue_get(Queue);
    LOG_INFO("data:%d \n", *ptr);
    LOG_INFO("Queue_element_numbers:%d \n", Queue_element_numbers(Queue));

    ptr = Queue_get(Queue);
    LOG_INFO("data:%d \n", *ptr);
    LOG_INFO("Queue_element_numbers:%d \n", Queue_element_numbers(Queue));

    ptr = Queue_get(Queue);
    LOG_INFO("data:%d \n", *ptr);
    LOG_INFO("Queue_element_numbers:%d \n", Queue_element_numbers(Queue));




    // test redis
    redisContext *conn = redisConnect("127.0.0.1", 6379);
    redisCommand(conn, "set name zhangxu");


    // test 
    Media_capture_object mc;
    Media_capture_params params;

    LOG_DEBUG("\n");
    strcpy(params.url, "/tmp/Meerkats.mp4");
    LOG_DEBUG("\n");

    ret = Media_capture_init(&mc, &params);
    LOG_INFO("Media_capture_init ret:%d \n", ret);

    //ret = Media_capture_start(&mc);
    //LOG_INFO("Media_capture_start ret:%d , tid:%d\n", ret, mc.tid);


    AVPacket pkt;
    while(1){
        ret = Media_capture_step(&mc, &pkt);
        if (ret == 0){
            LOG_INFO("Media_capture_step ret:%d, frame stream_index:%d, dts:%lld\n", ret, pkt.stream_index, pkt.dts);
            if (pkt.stream_index == 0){
                redisCommand(conn, "lpush frames %lld", pkt.dts);
            }
            av_free_packet(&pkt);
        }else{
            LOG_INFO("Media_capture_step ret:%d\n", ret);
            return 0;
        }
        //sleep(1);
    }

    sleep(5);

    return 0;
}