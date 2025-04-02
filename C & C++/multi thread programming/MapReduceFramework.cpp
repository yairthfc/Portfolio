//
// Created by yairthfc on 7/1/24.
//
#include "MapReduceFramework.h"
#include <map>
#include <cstdio>
#include <atomic>
#include <cstdlib>
#include <iostream>
#include <algorithm>
#include <semaphore.h>
#include <pthread.h>
#define STATE_MASK 13835058055282163712
#define TOTAL_MASK 4611686016279904256
#define DONE_MASK 2147483647
#define STATE 62
#define TOTAL 31
#define DONE 0

struct JobContext;
struct ThreadContext;

uint32_t get_val(uint64_t atomicvar, int val)
{
    if (val == STATE)
    {
        return (atomicvar & STATE_MASK) >> STATE;
    }
    if (val == DONE)
        return (atomicvar & DONE_MASK) ;
    return (atomicvar & TOTAL_MASK) >> TOTAL;
}

void inc_state(std::atomic<uint64_t>* atomicvar)
{
    *atomicvar = ((*atomicvar) & ~STATE_MASK) | (((((*atomicvar) & STATE_MASK) >> STATE) + 1) << STATE);
}

//void inc_done(ThreadContext *tc) { set_val(tc->job->state, DONE, get_val(tc->job->state->load(), DONE) + 1); }


//not for state flag
void set_val(std::atomic<uint64_t>* atomicvar, int valtochange, uint32_t valtoset){
    *atomicvar = ((*atomicvar) & ~(TOTAL_MASK << valtochange)) | ((static_cast<uint64_t>(valtoset) & TOTAL_MASK) << valtochange);
}

//ZEROES DONE!
void set_total(std::atomic<uint64_t>* atomicvar, uint32_t valtoset){
    *atomicvar = ((*atomicvar) & STATE_MASK) | (static_cast<uint64_t>(valtoset) << TOTAL);
    //*atomicvar = ((*atomicvar) & ~TOTAL_MASK) | (((((*atomicvar) & STATE_MASK) >> STATE) + 1) << STATE);
    //*atomicvar = (static_cast<uint64_t>(valtoset)  << TOTAL);
}



class Barrier {
public:
    Barrier(int numThreads);
    ~Barrier();
    void barrier();

private:
    pthread_mutex_t mutex;
    pthread_cond_t cv;
    int count;
    int numThreads;
};

Barrier::Barrier(int numThreads)
        : count(0)
        , numThreads(numThreads)
{
    if (pthread_mutex_init(&mutex, NULL) != 0) {
        fprintf(stderr, "[[Barrier]] error on pthread_mutex_init");
        exit(1);
    }

    if (pthread_cond_init(&cv, NULL) != 0) {
        fprintf(stderr, "[[Barrier]] error on pthread_cond_init");
        pthread_mutex_destroy(&mutex);
        exit(1);
    }
}


Barrier::~Barrier()
{
    if (pthread_mutex_destroy(&mutex) != 0) {
        fprintf(stderr, "[[Barrier]] error on pthread_mutex_destroy");
        exit(1);
    }
    if (pthread_cond_destroy(&cv) != 0){
        fprintf(stderr, "[[Barrier]] error on pthread_cond_destroy");
        exit(1);
    }
}


void Barrier::barrier()
{
    if (pthread_mutex_lock(&mutex) != 0){
        fprintf(stderr, "[[Barrier]] error on pthread_mutex_lock");
        exit(1);
    }
    if (++count < numThreads) {
        if (pthread_cond_wait(&cv, &mutex) != 0){
            fprintf(stderr, "[[Barrier]] error on pthread_cond_wait");
            exit(1);
        }
    } else {
        count = 0;
        if (pthread_cond_broadcast(&cv) != 0) {
            fprintf(stderr, "[[Barrier]] error on pthread_cond_broadcast");
            exit(1);
        }
    }
    if (pthread_mutex_unlock(&mutex) != 0) {
        fprintf(stderr, "[[Barrier]] error on pthread_mutex_unlock");
        exit(1);
    }
}




struct ThreadContext{
    int tid;
    IntermediateVec* inter_vec;
    JobContext* job;
};



struct JobContext{
    int num_threads;
    std::vector<ThreadContext*>* threads;
    pthread_t* pthreads_pointers;
    std::atomic<uint64_t>* state;
    std::atomic<uint32_t>* keys_counter;
    pthread_mutex_t* mutex;
    pthread_mutex_t* state_mutex;
    pthread_mutex_t* out_mutex;
    const InputVec& input;
    OutputVec& output;
    std::vector<IntermediateVec*>* shuffle_vec;
    sem_t* sem;
    const MapReduceClient& client;
    Barrier* barrier;
    std::atomic<bool> wait;
    JobState last_stage;
    std::atomic<bool> is_stage_updated;
    JobContext(int multiThreadLevel, const InputVec &input,
               OutputVec &output, const MapReduceClient &client) :
            num_threads(multiThreadLevel), input(input), output(output), client(client), wait(false), is_stage_updated(
            true)  {
        //mutexes?
        this->threads = new std::vector<ThreadContext*>;
        this->pthreads_pointers = new pthread_t[multiThreadLevel];
        state = new std::atomic<uint64_t>;
        *state = 0;
        keys_counter = new std::atomic<uint32_t>;
        *keys_counter = 0;
        set_total(this->state, this->input.size());
        sem = new sem_t;

        shuffle_vec = new std::vector<IntermediateVec*>;
        mutex = new pthread_mutex_t;
        state_mutex = new pthread_mutex_t;
        out_mutex = new pthread_mutex_t;

        barrier = new Barrier(num_threads);
        last_stage = {UNDEFINED_STAGE, 0};

        if (pthread_mutex_init(mutex, NULL) !=0)
        {
            std::cout << "system error: unable to create mutex " << std::endl;
            exit(EXIT_FAILURE);
        }
      if (pthread_mutex_init(state_mutex, NULL) !=0)
      {
        std::cout << "system error: unable to create mutex " << std::endl;
        pthread_mutex_destroy(this->mutex);
        exit(EXIT_FAILURE);
      }
      if (pthread_mutex_init(out_mutex, NULL) !=0)
      {
        std::cout << "system error: unable to create mutex " << std::endl;
        pthread_mutex_destroy(this->mutex);
        exit(EXIT_FAILURE);
      }
      if  (sem_init(sem, 0,0) !=0)
      {
        std::cout << "system error: unable to create semaphore " << std::endl;
        pthread_mutex_destroy(this->mutex);
        pthread_mutex_destroy(this->state_mutex);
        pthread_mutex_destroy(this->out_mutex);
        exit(EXIT_FAILURE);
      }

    }

    ~JobContext() {
        pthread_mutex_destroy(this->mutex);
        pthread_mutex_destroy(this->state_mutex);
        pthread_mutex_destroy(this->out_mutex);
        sem_destroy(this->sem);
        //delete barrier;
    }
    //destructor for mutexes and semaphors.
};

void update_state(ThreadContext* tc, stage_t cur_state, unsigned long total){
    if (pthread_mutex_lock(tc->job->state_mutex) != 0)
    {
      std::cout << "system error: unable to use mutex " << std::endl;
      exit(EXIT_FAILURE);
    }
    if (get_val(tc->job->state->load(), STATE) == cur_state)
    {
        tc->job->is_stage_updated.store(false);
        set_total(tc->job->state, total); //ZERO DONE
        //*(tc->job->state) = *(tc->job->state) & (~(static_cast<uint64_t>(DONE_MASK)));
        inc_state(tc->job->state);
        //int done = get_val(tc->job->state->load(), DONE);
    }
  if (pthread_mutex_unlock(tc->job->state_mutex) != 0)
  {
    std::cout << "system error: unable to unuse mutex " << std::endl;
    exit(EXIT_FAILURE);
  }
}



IntermediatePair* max(JobContext* job, int num_threads){
    //bool first = true;
    IntermediatePair* max_pair(NULL) ;
    int tidmax = -1;
    for (int i = 0; i< num_threads ; i++){
        if (job->threads->at(i)->inter_vec->empty()){
            continue;
        }
        if (tidmax == -1)
        {
            //first = false;
            max_pair = &job->threads->at(i)->inter_vec->back();
            tidmax = i;
            continue;
        }
        if(*max_pair->first < *job->threads->at(i)->inter_vec->back().first){
            max_pair = &job->threads->at(i)->inter_vec->back();
            tidmax = i;
        }
    }
   /* if(max_pair.first == NULL){
        return max_pair;
    }*/
    if (tidmax>-1)
    {
        job->threads->at(tidmax)->inter_vec->pop_back();
        return max_pair;
    }
    return nullptr;
}

auto comparator = [](const IntermediatePair & p1, const IntermediatePair & p2){
    return *p1.first < *p2.first;
};


void emit2 (K2* key, V2* value, void* context){
    auto tc = static_cast<ThreadContext*>(context);
    IntermediatePair pair(key, value);
    tc->inter_vec->insert(tc->inter_vec->cend(), pair);

}
void emit3 (K3* key, V3* value, void* context){
    auto tc = static_cast<ThreadContext*>(context);
    OutputPair pair(key,value);
  if (pthread_mutex_lock(tc->job->out_mutex) != 0)
  {
    std::cout << "system error: unable to use mutex " << std::endl;
    exit(EXIT_FAILURE);
  }
    tc->job->output.push_back(pair);
  if (pthread_mutex_unlock(tc->job->out_mutex) != 0)
  {
    std::cout << "system error: unable to unuse mutex " << std::endl;
    exit(EXIT_FAILURE);
  }
}

void waitForJob(JobHandle job){
    if (!job)
    {
        //error
        return;
    }
    auto jc = static_cast<JobContext*>(job);
    if (!jc->wait.load())
    {
        jc->wait.store(true);
        for (int i=0;i<jc->num_threads;i++)
        {
            if (pthread_join(jc->pthreads_pointers[i],NULL) !=0)
            {
              std::cout << "system error: unable to join " << std::endl;
              exit(EXIT_FAILURE);
            }
        }
    }
}


void getJobState(JobHandle job, JobState* state){
    if (!job || !state)
    {
        return;
    }
    auto jc = static_cast<JobContext*>(job);
    if (jc->is_stage_updated.load())
    {
        state->percentage = jc->last_stage.percentage;
        state->stage = jc->last_stage.stage;
        jc->is_stage_updated.store (false);
        return;
    }
//    pthread_mutex_t mutex;
//    if (pthread_mutex_init(&mutex, NULL) != 0) {
//        fprintf(stderr, "error on pthread_mutex_init");
//        exit(1);
//    }
  if (pthread_mutex_lock(jc->state_mutex) != 0)
  {
    std::cout << "system error: unable to use mutex " << std::endl;
    exit(EXIT_FAILURE);
  }
    uint32_t total_pairs = get_val(jc->state->load(), TOTAL);
    if (total_pairs != 0){
        uint32_t done = get_val(jc->state->load(), DONE);
        state->percentage = std::min((float(done) / float(total_pairs)) * 100,float(100));
    }
    state->stage = static_cast<stage_t>(get_val(jc->state->load(), STATE));
    jc->last_stage = *state;
    jc->is_stage_updated.store(true);
  if (pthread_mutex_unlock(jc->state_mutex) != 0)
  {
    std::cout << "system error: unable to unuse mutex " << std::endl;
    exit(EXIT_FAILURE);
  }
//    if (pthread_mutex_destroy(&mutex) != 0) {
//        fprintf(stderr, "error on pthread_mutex_destroy");
//        exit(1);
//    }

}


void closeJobHandle(JobHandle job){
    if (!job)
    {
        //error
        return;
    }
    waitForJob(job);
    auto jc = static_cast<JobContext*>(job);
    delete jc;
}



JobHandle entry_point(JobHandle job){

    // map phase
    auto tc = static_cast<ThreadContext*>(job);
    //pthread_mutex_t* mutex = (pthread_mutex_t*) malloc(sizeof(pthread_mutex_t));
    //malloc error
    update_state(tc, UNDEFINED_STAGE, get_val(tc->job->state->load(), TOTAL));
    uint32_t total = (*(tc->job->state) & TOTAL_MASK) >> TOTAL;
    unsigned long index = ((*(tc->job->state))++ & DONE_MASK) >> DONE; //might be problematic case threads > pairs
    tc->job->is_stage_updated.store(false);
    while(index < total)
    {
        //pthread_mutex_lock(tc->job->mutex);
        //uint32_t old = get_val(tc->job->state->load(), DONE);
        //pthread_mutex_unlock(tc->job->mutex);
        tc->job->client.map(tc->job->input[index].first, tc->job->input[index].second, tc);
        //inc_done(tc);
        if (index < total) { //protection case total = MAXINT
            index = ((*(tc->job->state))++ & DONE_MASK) >> DONE;
            tc->job->is_stage_updated.store(false);
        }
        else
        {
            index = ((*(tc->job->state)) & DONE_MASK) >> DONE;
        }
        //set_val(tc->job->state,DONE,index+1);
    }
    //end map

    //start sort
    std::sort(tc->inter_vec->begin(),tc->inter_vec->end(), comparator);
    (*(tc->job->keys_counter)) += tc->inter_vec->size();
    tc->job->barrier->barrier();
    //end sort

    //start shuffle
    if (tc->tid == 0)
    {
        //tc->job->shuffle_vec = new std::vector<IntermediateVec*>;
        //set_total(tc->job->state,tc->job->keys_counter->load());// zero done
        update_state(tc, MAP_STAGE, tc->job->keys_counter->load());
        auto vec = tc->job->shuffle_vec;
        IntermediatePair* maxi = max(tc->job, tc->job->num_threads) ;
        while(maxi != nullptr){
            //check if current max is diff from old
            if (vec->empty() || (*vec->back()->back().first < *maxi->first || *maxi->first < *vec->back()->back().first))
            {
                IntermediateVec* temp_vec = new IntermediateVec;
                temp_vec->push_back(*maxi);
                vec->push_back(temp_vec);
            }
            else //same key
            {
                vec->back()->push_back(*maxi);
            }
            ((*(tc->job->state))++ & DONE_MASK) >> DONE;
            tc->job->is_stage_updated.store(false);
            maxi = max(tc->job, tc->job->num_threads);
        }
        sem_post(tc->job->sem);
    }
    else
    {
        sem_wait(tc->job->sem);
        sem_post(tc->job->sem);
    }
    //finish shuffle
    // start reduce


    update_state(tc, SHUFFLE_STAGE, get_val(tc->job->state->load(), TOTAL));

    total = (*(tc->job->state) & TOTAL_MASK) >> TOTAL;
    //index = ((*(tc->job->state))++ & DONE_MASK) >> DONE;

    while(!tc->job->shuffle_vec->empty())
    {
      if (pthread_mutex_lock(tc->job->mutex) != 0)
      {
        std::cout << "system error: unable to use mutex " << std::endl;
        exit(EXIT_FAILURE);
      } //error handle?
        if (tc->job->shuffle_vec->empty())
        {
          if (pthread_mutex_unlock(tc->job->mutex) != 0)
          {
            std::cout << "system error: unable to unuse mutex " << std::endl;
            exit(EXIT_FAILURE);
          } //error handle?
            continue;
        }
        IntermediateVec* cur = tc->job->shuffle_vec->back();
        unsigned long size = cur->size();
        tc->job->shuffle_vec->pop_back();
      if (pthread_mutex_unlock(tc->job->mutex) != 0)
      {
        std::cout << "system error: unable to unuse mutex " << std::endl;
        exit(EXIT_FAILURE);
      } //error handle?
        tc->job->client.reduce(cur,tc);
        ((*(tc->job->state)) += size & DONE_MASK) >> DONE;
        tc->job->is_stage_updated.store(false);
        int done = get_val(tc->job->state->load (), DONE);
    }

    //tc->job->barrier->barrier();
    tc->job->is_stage_updated.store(false);
    return job;
}

JobHandle startMapReduceJob(const MapReduceClient& client,
                            const InputVec& inputVec, OutputVec& outputVec,
                            int multiThreadLevel){
    if (inputVec.empty())
    {
        return nullptr;
    }
    JobContext* job = new JobContext(multiThreadLevel, inputVec, outputVec, client);

    for(int i=0; i< multiThreadLevel; ++i){
        job->threads->push_back(new ThreadContext);
        job->threads->at(i)->tid = i;
        job->threads->at(i)->job = job;
        job->threads->at(i)->inter_vec = new IntermediateVec();
        //pthread_t* threads = new pthread_t[multiThreadLevel];
        int res = pthread_create(&job->pthreads_pointers[i], NULL, entry_point, (void*)(job->threads->at(i))); //maybe still need threads array
        if (res != 0)
        {
            std::cout << "system error: unable to create thread " << std::endl;
            exit(EXIT_FAILURE);
        }

    }
    return (JobHandle)(job);
}

