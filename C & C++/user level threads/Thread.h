//
// Created by tomer.99 on 6/13/24.
//

#ifndef EX2_THREAD_H
#define EX2_THREAD_H

#include <stdio.h>
#include <setjmp.h>
#include <signal.h>
#include <unistd.h>
#include <sys/time.h>
#include <stdbool.h>
#include <stdlib.h>

#define MAX_THREAD_NUM 100 /* maximal number of threads */
#define STACK_SIZE 4096 /* stack size per thread (in bytes) */

typedef enum {READY,RUNNING,BLOCKED} ThreadState;
typedef unsigned long address_t;
typedef void (*thread_entry_point)(void);

class Thread {
private:
    int tid;
    ThreadState state;
    char* stack;
    address_t sp;
    address_t pc;
    sigjmp_buf* jbuf;
    thread_entry_point entryPoint;
    int q_count;
    static int overall_q_count;
    static int count;

public:
    Thread (thread_entry_point ep, int tid);
    ~Thread();
    int get_q_count();
    static int get_ov_q_count();
    static int get_count();
    int get_tid();
    ThreadState get_state();
    address_t get_sp();
    address_t get_pc();
    char* get_stack();
    sigjmp_buf* get_buf();

    void change_count(int i);
    void inc_q_count();
    void set_state(ThreadState state);
    void set_sp(address_t sp);
    void set_pc(address_t pc);

};




#endif //EX2_THREAD_H
