#ifndef _MEDIA_CAPTURE_H_
#define _MEDIA_CAPTURE_H_

#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <fcntl.h>

#include <string.h>
#include <sys/socket.h>
#include <netinet/in.h>

#include <libavformat/avformat.h>
#include <libavcodec/avcodec.h>


#define MEDIA_CAPTURE_URL_LENTH         256


/*
 * Error codes used. Negative values are errors,
 * while positive values indicate success.
 */
#define MCAP_EOUTSIZE   -6   /**< The numbers out of size (failure). */
#define MCAP_EINVAL     -5   /**< Invalid input arguments (failure). */
#define MCAP_ENOMEM     -4   /**< No memory available (failure). */
#define MCAP_EIO        -3   /**< An IO error occured (failure). */
#define MCAP_ENOTIMPL   -2   /**< Functionality not implemented (failure). */
#define MCAP_EFAIL      -1   /**< General failure code (failure). */
#define MCAP_EOK         0   /**< General success code (success). */
#define MCAP_EFLUSH      1   /**< The command was flushed (success). */
#define MCAP_EPRIME      2   /**< The command was primed (success). */
#define MCAP_EFIRSTFIELD 3   /**< Only the first field was processed (success)*/
#define MCAP_EBITERROR   4   /**< There was a non fatal bit error (success). */
#define MCAP_ETIMEOUT    5   /**< The operation was timed out (success). */
#define MCAP_EEOF        6   /**< The operation reached end of file */
#define MCAP_EAGAIN      7   /**< The command needs to be rerun (success). */


/*  
*  the codes for media capture state
**/
#define M_STATE_OK      0
#define M_STATE_INIT    1   


typedef  struct {
    char    url[MEDIA_CAPTURE_URL_LENTH];
}Media_capture_params;

typedef struct {
    /* the media url */
    char                url[MEDIA_CAPTURE_URL_LENTH];

    /* the media capture thread id, */
    pthread_t           tid;

    /* the context of media stream */
    AVFormatContext *   media_ctx;

    /* the state of the media capture */
    int                 state;

    /* the media capture reset level */
    int                 reset_level;

    /* the queue use for contain the media packets */
    Queue_object        queue;


    /**   **/


} Media_capture_object;



/*      
*   Init the media_capture object
*/
int Media_capture_init(Media_capture_object * obj, Media_capture_params * params);

/*      
*   Release the media_capture object
*/
int Media_capture_release(Media_capture_object * obj);


/*
*   Get the one media frame.
*   
*/
int Media_capture_step(Media_capture_object * obj, AVPacket *pkt);

/*
*   Start the media capture thread to get media frames automaticly.
*   User can get frame asynchronously by Media_capture_frame().
*/
int Media_capture_start(Media_capture_object * obj);


int Media_capture_frame(Media_capture_object * obj, AVPacket *pkt);


// get the packet from media capture
AVPacket * get_packet_from_media_capture(Media_capture_object * obj);



#endif