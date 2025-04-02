//
// Created by yairthfc on 7/18/24.
//
#include "VirtualMemory.h"
#include "MemoryConstants.h"
#include "PhysicalMemory.h"
#include <cmath>

typedef struct search_data{
    //word_t (&pages_to_ignore)[TABLES_DEPTH];
    unsigned int max_cyclic_distance;
    word_t p;
    word_t p_father;
    word_t p_virtual;
    word_t page_to_look;
    unsigned int counter;
    bool found;
    word_t free_frame;
    word_t maximal_frame_visited = 0;

    search_data(word_t pagetolook)
    {
      //pages_to_ignore = to_ignore;
      max_cyclic_distance = 0;
      p = 0;
      p_father = 0;
      counter = 0;
      found = true;
      free_frame = 0;
      page_to_look = pagetolook;
      p_virtual = 0;
      maximal_frame_visited = 0;

    }

} search_data;



void clear_table(uint64_t f_ind){
  for(uint64_t i = 0; i < PAGE_SIZE; ++i){
    PMwrite (f_ind * PAGE_SIZE + i,0);
  }
  //printRam();
}
void VMinitialize(){
  clear_table (0);
}

//search_data* init_search_data(search_data* sd, word_t* pages_to_ignore, word_t
//page_to_look)
//{
//      sd->pages_to_ignore = pages_to_ignore;
//      sd->max_cyclic_distance = 0;
//      sd->p = 0;
//      sd->p_father = 0;
//      sd->counter = 0;
//      sd->found = false;
//      sd->free_frame = 0;
//      sd->page_to_look = page_to_look;
//      sd->p_virtual = 0;
//      sd->maximal_frame_visited = 0;
//      return sd;
//}


bool is_in(word_t num, word_t (&to_ignore)[TABLES_DEPTH])
{
  for (int i = 0; i < TABLES_DEPTH; ++i) {
    if (to_ignore[i] == num) {
      return true;
    }
  }
  return false;
}

void dfs(search_data& sd, word_t frame, word_t father, int depth, word_t
cur_page,word_t (&to_ignore)[TABLES_DEPTH])
{
  //printRam();
  word_t cur = 0;
  int zeroes = 0;
    if (depth < TABLES_DEPTH)
    {
      //sd.is_visited[frame] = true;
//word_t *cur_p;
      for (int i = 0; i < PAGE_SIZE; i++)
      {
        PMread (frame * PAGE_SIZE + i, &cur);
        if (cur != 0)
        {
          sd.maximal_frame_visited = std::fmax (cur, sd.maximal_frame_visited);
          sd.found = false;
          dfs (sd, cur, frame * PAGE_SIZE + i, depth + 1, ((cur_page <<
          OFFSET_WIDTH) + i) ,
               to_ignore);
        }
        //cur_page+i* pow (2,
          //                                                                           TABLES_DEPTH
          //                                                                           - depth-1)
        else
        {
          zeroes++;
        }
      }
      if (zeroes == PAGE_SIZE && frame != to_ignore[0])
      {
        sd.found = true;
        sd.free_frame = frame;
        if (frame != 0)
        {
          PMwrite (father, 0); //unlink!!
        }
      }
    }
    else // pages layer
    {
      unsigned int distance = std::fmin (NUM_PAGES - std::abs (sd
          .page_to_look-cur_page), std::abs (sd
          .page_to_look-cur_page));
      if (distance > sd.max_cyclic_distance)
      {
        //update all related parameters
        sd.max_cyclic_distance = distance;
        sd.p = frame;
        sd.p_father = father;
        sd.p_virtual = cur_page;
      }
    }
  }


word_t find_a_frame(word_t (&to_ignore)[TABLES_DEPTH], word_t page_to_look){
    //we need to recursively go through the tree and find how many enteris are not 0. if the counter is more then number of frames, we need to do the evict page algorithm
    //int counter = 0;
    //word_t maximal_frame_visited = 0;
    //init struct (ignore = visited)
    search_data sd = search_data(page_to_look);
    //run recursion
    //printRam();
    dfs(sd, 0,0,0,0,to_ignore);
    if (sd.free_frame > 0 && sd.free_frame < NUM_FRAMES) //case 1
    {
      clear_table (sd.free_frame);
      return sd.free_frame;
    }
    //case 2
    else if (sd.maximal_frame_visited + 1 < NUM_FRAMES)
    {
      return sd.maximal_frame_visited + 1;
    }
    //case 3
    else
    {
      PMevict (sd.p, sd.p_virtual);
      clear_table (sd.p);
      PMwrite (sd.p_father,0);
      return sd.p;
    }

}

uint64_t address_configure(uint64_t virtualAddress){
  uint64_t offset = ((uint64_t) (pow (2, OFFSET_WIDTH) - 1)) & virtualAddress;
  uint64_t page_num = virtualAddress >> OFFSET_WIDTH;
  uint64_t cur_level_page_num =
      page_num >> ((TABLES_DEPTH - 1) * OFFSET_WIDTH);
  word_t addr = 0;
  word_t next_addr = 0;
  word_t to_ignore[TABLES_DEPTH];
  for (int i = 0; i < TABLES_DEPTH; i++)
  {
    to_ignore[i] = 0;
  }
  //init to_ignore
  for (int i = 0; i < TABLES_DEPTH; i++)
  {
    cur_level_page_num =
        (page_num >> (TABLES_DEPTH - i - 1) * OFFSET_WIDTH)
                         & ((1LL << OFFSET_WIDTH) -1);
    PMread (addr * PAGE_SIZE + cur_level_page_num, &next_addr);
    if (next_addr == 0)
    {
      word_t f = find_a_frame (to_ignore, page_num);
      //printRam();
      if (i == TABLES_DEPTH - 1)
      {
        PMrestore (f, page_num);
      }
      PMwrite (addr * PAGE_SIZE + cur_level_page_num, f);
      next_addr = f;
    }
    addr = next_addr;
    to_ignore[0] = addr;
  }
  return addr * PAGE_SIZE + offset;
}

int VMread(uint64_t virtualAddress, word_t* value)
{
  if(virtualAddress >= VIRTUAL_MEMORY_SIZE){
    return 0;
  }

  PMread (address_configure (virtualAddress), value);
  return 1;
}

int VMwrite(uint64_t virtualAddress, word_t value){
  if(virtualAddress >= VIRTUAL_MEMORY_SIZE){
    return 0;
  }
  
  PMwrite (address_configure (virtualAddress), value);
  return 1;
}