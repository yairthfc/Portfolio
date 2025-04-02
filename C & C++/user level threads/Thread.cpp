//
// Created by tomer.99 on 6/13/24.
//

#include "Thread.h"

Thread::Thread (thread_entry_point ep, int tid) :
    entryPoint(ep), tid(tid)
{
    this->stack = (char*)malloc(STACK_SIZE);
    this->count++;
}

Thread::~Thread()
{
    free(this->stack);
    this->count--;
}

int Thread::get_q_count(){return this->q_count;}
int Thread::get_ov_q_count(){return overall_q_count;}
int Thread::get_count(){return count;}
int Thread::get_tid(){return this->tid;}
ThreadState Thread::get_state(){return this->state;}
address_t Thread::get_sp(){return this->sp;}
address_t Thread::get_pc(){return this->pc;}
char* Thread::get_stack(){return this->stack;}
sigjmp_buf* Thread::get_buf(){return this->jbuf;}

void Thread::change_count(int i){
    if (i == 1){
        count++;
    }
    else {
        count--;
    }
}

void Thread::inc_q_count() {
    this->q_count++;
    overall_q_count++;
}

void Thread::set_state(ThreadState state) {this->state = state;}

void Thread::set_sp(address_t sp) {this->sp = sp;}

void Thread::set_pc(address_t pc) {this->pc = pc;}





