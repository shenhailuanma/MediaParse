#ifndef _LIST_H_
#define _LIST_H_

typedef struct list_head
{
  struct list_head *next;
  struct list_head *prev;
} list_t;

#define INIT_LIST(entry) struct list_head entry = \
  {.next = &entry, \
  .prev = &entry}
  
/* Initialize a new list head.  */
#define INIT_LIST_HEAD(ptr) \
  (ptr)->next = (ptr)->prev = (ptr)
  
//#define offsetof(type, member) (unsigned long)(&(((type *)0)->member))

#define container_of(ptr, type, member) \
  (type *)((char *)ptr - \
  (unsigned long)(&(((type *)0)->member)))

#define list_entry(ptr, type, member) \
  container_of(ptr, type, member)


/* Add new element at the head of the list.  */
static void list_add(list_t *newp, list_t *head)
{
  head->next->prev = newp;
  newp->next = head->next;
  newp->prev = head;
  head->next = newp;
}


/* Add new element at the tail of the list.  */
static inline void list_add_tail(list_t *newp, list_t *head)
{
  head->prev->next = newp;
  newp->next = head;
  newp->prev = head->prev;
  head->prev = newp;
}


/* Remove element from list.  */
static inline void list_del(list_t *elem)
{
  elem->next->prev = elem->prev;
  elem->prev->next = elem->next;
}


/* Join two lists.  */
static inline void list_splice(list_t *add, list_t *head)
{
  /* Do nothing if the list which gets added is empty.  */
  if (add != add->next)
    {
      add->next->prev = head;
      add->prev->next = head->next;
      head->next->prev = add->prev;
      head->next = add->next;
    }
}

#endif

