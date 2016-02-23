#ifndef _QUEUE_H_
#define _QUEUE_H_

#include <pthread.h>
#include "list.h"
#include "log.h"



/*
 * Error codes used. Negative values are errors,
 * while positive values indicate success.
 */
#define QUEUE_EOUTSIZE   -6   /**< The numbers out of size (failure). */
#define QUEUE_EINVAL     -5   /**< Invalid input arguments (failure). */
#define QUEUE_ENOMEM     -4   /**< No memory available (failure). */
#define QUEUE_EIO        -3   /**< An IO error occured (failure). */
#define QUEUE_ENOTIMPL   -2   /**< Functionality not implemented (failure). */
#define QUEUE_EFAIL      -1   /**< General failure code (failure). */
#define QUEUE_EOK         0   /**< General success code (success). */
#define QUEUE_EFLUSH      1   /**< The command was flushed (success). */
#define QUEUE_EPRIME      2   /**< The command was primed (success). */
#define QUEUE_EFIRSTFIELD 3   /**< Only the first field was processed (success)*/
#define QUEUE_EBITERROR   4   /**< There was a non fatal bit error (success). */
#define QUEUE_ETIMEOUT    5   /**< The operation was timed out (success). */
#define QUEUE_EEOF        6   /**< The operation reached end of file */
#define QUEUE_EAGAIN      7   /**< The command needs to be rerun (success). */


/* structs define */
typedef struct Queue_object{
    list_t              list_head;
    pthread_mutex_t     mutex;

    /*  the max size of the queue.
    *   when max_size > 0, the queue size will be limited by max_size;
    *   when max_size <= 0, the queue size will not be limited.
    */
    int                 max_size;

    int                 element_numbers;

} Queue_object;


typedef struct Queue_element {
    list_t              list_head;
    char *              data;       /* the data ptr  */
} Queue_element;



typedef struct Queue_attrs {
    /* the maximum elements that can be put in queue */     
    int max_size;
} Queue_attrs;




static Queue_attrs Queue_attrs_default = {
    0
};




/* Functions */

static int Queue_init(Queue_object * pQueue, Queue_attrs * attrs)
{

    if (pQueue == NULL) {
        LOG_ERROR("input: pQueue == NULL \n");
        return QUEUE_EINVAL;
    }

    if (attrs == NULL){
        LOG_WARN("input: attrs == NULL , use default attrs\n");
        attrs = &Queue_attrs_default;
    }

    memset(pQueue, 0, sizeof(Queue_object));

    // init the object
    INIT_LIST_HEAD(&pQueue->list_head);

    pthread_mutex_init(&pQueue->mutex, NULL);


    pQueue->max_size = 0; 
    if(attrs->max_size > 0){
        pQueue->max_size = attrs->max_size;
    }

    pQueue->element_numbers = 0; 
        
    return QUEUE_EOK;
}


static int Queue_put(Queue_object * pQueue, char *  ptr)
{

    if(pQueue == NULL || ptr == NULL){
        LOG_WARN("input: pQueue == NULL or ptr == NULL \n");
        return QUEUE_EINVAL;
    }

    int ret = QUEUE_EOK;

    // malloc
    Queue_element * element = (Queue_element *)calloc(1, sizeof(Queue_element));
    if(element == NULL){
        LOG_ERROR("element == NULL,calloc error\n");
        return QUEUE_ENOMEM;
    }

    INIT_LIST_HEAD(&element->list_head);
    element->data = ptr;

    // add to queue list
    pthread_mutex_lock(&pQueue->mutex);
    if(pQueue->max_size > 0 && pQueue->element_numbers >= pQueue->max_size){
        ret = QUEUE_EOUTSIZE;
    }else{
        list_add_tail(&element->list_head, &pQueue->list_head);
        pQueue->element_numbers++;
    }
    pthread_mutex_unlock(&pQueue->mutex);

    return ret;
}

static char * Queue_get(Queue_object * pQueue)
{
    if(pQueue == NULL){
        LOG_WARN("input: pQueue == NULL\n");
        return NULL;
    }

    char    * data = NULL;
    list_t  * elem = NULL;
    list_t  * head = &pQueue->list_head;
    

    pthread_mutex_lock(&pQueue->mutex);
    if(head->next != head && head->prev != head){
        elem = head->next;
        list_del(elem);
        pQueue->element_numbers--;
    }
    pthread_mutex_unlock(&pQueue->mutex);

    if(elem != NULL){
        data = ((Queue_element *)elem)->data;
        free(elem);
    }
    return data;
}

static int Queue_element_numbers(Queue_object * pQueue)
{

    if(pQueue == NULL){
        LOG_WARN("input: pQueue == NULL\n");
        return QUEUE_EINVAL;
    }

    return pQueue->element_numbers;
}


#endif