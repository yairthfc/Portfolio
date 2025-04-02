//
// Created by yairt on 04/06/2024.
//
#include "uthreads.h"
#include "Thread.h"
#include <iostream>
#include <set>
#include <list>
#include <vector>
#include <unordered_map>
#include <setjmp.h>
#include <signal.h>
#define JB_SP 6
#define JB_PC 7
using namespace std;
typedef unsigned long address_t;

std::unordered_map<int, Thread*> All_Threads;
std::unordered_map<unsigned int, std::vector<int>> sleepMap;
std::list<int> ReadyQueue;
int running_t;
struct itimerval timer;
int _quantum_usecs;

//int num_threads = 0;

std::multiset<int> av_nums;
int av_nums_fill(){
    for (int i = 0; i <= 99; ++i){
        av_nums.insert(i);
    }
}

void start_quantum()
{
    timer.it_value.tv_usec = _quantum_usecs % 999999;
    timer.it_value.tv_sec = _quantum_usecs / 999999;
    timer.it_interval.tv_usec = 0;
    timer.it_interval.tv_sec = 0;

    if (setitimer(ITIMER_VIRTUAL, &timer, NULL)) //starts timer
    {
        printf("system error: setitimer error.");
        finish();
    }

}

void stop_timer()
{
    timer.it_value.tv_sec = 0;
    timer.it_value.tv_usec = 0;
    timer.it_interval.tv_usec = 0;
    timer.it_interval.tv_sec = 0;

    if (setitimer(ITIMER_VIRTUAL, &timer, NULL)) //starts timer
    {
        printf("system error: setitimer error.");
        finish();
    }
}

void finish()
{
    std::unordered_map<int,Thread*>::iterator it;
    for (it = All_Threads.begin(); it != All_Threads.end(); it++)
    {
        delete it->second;
    }

    exit(-1);
}
int update_sleeps(){
    std::unordered_map<unsigned int, std::vector<int>> updated_map;

    // Iterate over the original map
    for (const auto& pair : sleepMap) {
        int new_key = pair.first - 1;  // Decrease the key by 1
        updated_map[new_key] = pair.second;  // Insert into the new map
    }

    // Replace the original map with the updated map
    sleepMap = std::move(updated_map);
    auto it = sleepMap.find(0);
    for (size_t i =0; i< (*it).second.size(); ++i){
        int cur_id = it->second[i];
        uthread_resume(cur_id);
    }
    return 0;

}

address_t translate_address(address_t addr)
{
    address_t ret;
    asm volatile("xor    %%fs:0x30,%0\n"
        "rol    $0x11,%0\n"
                 : "=g" (ret)
                 : "0" (addr));
    return ret;
}

int next_tid()
{
    auto tid = av_nums.begin();
    av_nums.erase(tid);
    return *tid;
}

Thread* get_Thread(int tid){
    return All_Threads.find(tid);
}
auto rq_find(int tid){
    for(auto r_it = ReadyQueue.begin(); r_it != ReadyQueue.end();){
        if ((*r_it == tid){
            return *r_it;
        }
    }

}


void timer_handler(ThreadState state)
{
    //add signals blocker
    //add test if theres only one process
    sigsetjmp(*(get_Thread(running_t)->get_buf()), 1);
    ReadyQueue.push_back(running_t);
    running_t = ReadyQueue.front();
    get_Thread(running_t)->inc_q_count();
    ReadyQueue.pop_front();

    siglongjmp(*(get_Thread(running_t)->get_buf()),1);

    fprintf(stderr,"system error: failed switching threads.");
    finish();
}

int uthread_init(int quantum_usecs){
    _quantum_usecs = quantum_usecs;
	if (quantum_usecs <= 0){fprintf(stderr, "thread library error: quantom number not positive");}
    av_nums_fill();
	Thread* main_thread = new Thread(nullptr, next_tid());
	main_thread->set_state(RUNNING);
    main_thread->change_count(1);

    running_t = main_thread->get_tid();

	struct sigaction sa = {0};

    sa.sa_handler = &timer_handler;
    if (sigaction(SIGVTALRM, &sa, NULL) < 0)
    {
        fprintf(stderr,"system error: sigaction error.");
    }
   start_quantum();

    return -1;

}

int uthread_spawn(thread_entry_point entry_point){
	if(Thread::get_count() == MAX_THREAD_NUM){return -1;}

    int cur_tid = next_tid();
	Thread* cur = new Thread(entry_point, cur_tid);
	if (!cur){
        av_nums.insert((cur_tid));
        fprintf(stderr, "system error: failed allocating");
    } //error


	cur->set_state(READY);
	
	cur->set_sp((address_t )cur->get_stack() + STACK_SIZE - sizeof(address_t));
    cur->set_pc((address_t) entry_point);
	sigsetjmp(*(cur->get_buf()),1);
	((*(cur->get_buf()))->__jmpbuf)[JB_SP] = translate_address(cur->get_sp());
    ((*(cur->get_buf()))->__jmpbuf)[JB_PC] = translate_address(cur->get_pc());
	sigemptyset(&(*(cur->get_buf()))->__saved_mask);

    All_Threads[cur->get_tid()] = cur;
	ReadyQueue.push_back(cur->get_tid());
	return cur->get_tid();
}


int uthread_terminate(int tid){
    auto it = av_nums.find(tid);
    if (it != av_nums.end()) {
        std::cerr << "thread library error: tid doesn't exist in a existing thread" << std::endl;
    }

    if (tid != 0){
        if (tid == running_t){
            av_nums.insert(get_Thread(running_t)->get_tid());
            sigsetjmp(*(get_Thread(running_t)->get_buf()), 1);
            delete get_Thread(running_t);
            running_t = ReadyQueue.front();
            get_Thread(running_t)->inc_q_count();
            ReadyQueue.pop_front();
            siglongjmp(*(get_Thread(running_t)->get_buf()),1);
        }


    }
}


int uthread_block(int tid){
    auto it = av_nums.find(tid);
    if (it != av_nums.end()) {
        std::cerr << "thread library error: tid doesn't exist in a existing thread" << std::endl;
    }
    if (tid == 0){
        std::cerr << "thread library error: tid is main thread" << std::endl;
        return -1;
    }
    if (tid == running_t){

    }
}


int uthread_resume(int tid){
    auto it = av_nums.find(tid);
    if (it != av_nums.end()) {
        std::cerr << "thread library error: tid doesn't exist in a existing thread" << std::endl;
        return -1;
    }

    Thread* cur_thread = get_Thread(tid);
    if(cur_thread->get_state() == RUNNING || cur_thread->get_state() == READY){
        std::cerr << "thread library error: tid is not blocked" << std::endl;
        return -1;
    }

    cur_thread->set_state(READY);
    ReadyQueue.push_back(tid);
    return 0;
}


int uthread_sleep(int num_quantums){
    if (running_t == 0){
        std::cerr << "thread library error: tid is main thread" << std::endl;
        return -1;
    }

    if(sleepMap.find(num_quantums) != sleepMap.end()){
        sleppMap[num_quantums].second.push_back(running_t);
    }
    else{
        std::vector<int> cur_vec;
        cur_vec.push_back(running_t);
        sleepMap[num_quantums] =cur_vec;

    }

    uthread_block(running_t);
    return 0;
}

int uthread_get_tid(){
    return running_t;
}

int uthread_get_total_quantums(){
    return get_Thread(0)->get_ov_q_count();
}

int uthread_get_quantums(int tid){
    return get_Thread(tid)->get_q_count();
}