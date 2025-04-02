#include "markov_chain.h"
#include <string.h>
int get_random_number(int max_number);

bool check_if_pnt(char *word)
{
    if(word[strlen(word) - 1] == '.') //if ends with '.'
    {
        return true;
    }
    return false;
}

MarkovNode* get_first_random_node(MarkovChain *markov_chain)
{
    LinkedList *database = markov_chain->database;
    while(true) {
        int size = markov_chain->database->size;
        int iterator = get_random_number(size);
        Node *temp = database ->first;
        for (int i = 0; i < iterator; i++) // get the right node
        {
            temp = temp ->next;
        }
        char *data = temp ->data ->data;
        if (!check_if_pnt(data)){return temp->data;} // check if has a point
    }
}


int freq_sum(MarkovNode *node)
{
    int sum = 0;
    for (int i = 0; i < node ->frq_lst_size; i++) // loop on frequencies list
        // and sum
    {
        sum += node ->frequencies_list[i].frequency;
    }
    return sum;
}


MarkovNode* get_next_random_node(MarkovNode *state_struct_ptr)
{
    MarkovNodeFrequency *cur = state_struct_ptr->frequencies_list;
    if (freq_sum(state_struct_ptr) == 0){return NULL;} //if exists
    int random = get_random_number(freq_sum(state_struct_ptr));
    int iterator = 0;
    while (iterator < random) //run on freq list
    {
        iterator += cur->frequency;
        if (iterator <= random)
        {
            cur++;
        }
    }
    return cur ->markov_node;
}


int get_random_number(int max_number)
{
    return rand() % max_number;
}


void generate_tweet(MarkovChain *markov_chain,
                    MarkovNode *first_node, int max_length)
{
    int i = 0;
    MarkovNode *cur = first_node;
    if (first_node == NULL){cur = get_first_random_node(markov_chain);}
    while (cur != NULL && i < max_length) //until line ends
    {
        char *word = cur ->data;
        printf(" %s", word);
        i++;
        cur = get_next_random_node(cur); //next node
    }
}



void free_database(MarkovChain ** ptr_chain)
{
    LinkedList *database = (*ptr_chain) ->database;
    Node *cur = database ->first;
    for(int i = 0; i < database ->size; i++) //free linked list
    {
        MarkovNode *cur_mn = cur->data;
        free(cur_mn->data);
        cur_mn->data = NULL;
        if (cur_mn->frq_lst_size !=0) {
            free(cur_mn->frequencies_list);
            cur_mn->frequencies_list = NULL;
        }
        free(cur_mn);
        cur ->data = NULL;
        Node *temp = cur ->next;
        free(cur);
        cur = temp;
    }
    free(database); // free itself
}



bool add_node_to_frequencies_list(MarkovNode *first_node,
                                  MarkovNode *second_node)
{
    if (first_node ->frq_lst_size == 0) // if empty
    {
        MarkovNodeFrequency *freq_lst = malloc(sizeof (MarkovNodeFrequency));
        if (freq_lst == NULL){return false;}
        first_node ->frequencies_list = freq_lst;
        freq_lst ->markov_node = second_node;
        freq_lst ->frequency = 1;
        first_node ->frq_lst_size = 1;
        return true;
    }

    int size = first_node ->frq_lst_size;
    MarkovNodeFrequency  *cur = first_node ->frequencies_list;
    for (int i=0; i < size; i++) // if exists
    {
        if ((strcmp(cur[i].markov_node ->data, second_node ->data)) == 0)
        {
            cur[i].frequency++;
            return true;
        }
    }
    // if doesnt exist
    MarkovNodeFrequency *new_frq_lst = realloc(first_node ->frequencies_list,
               (first_node ->frq_lst_size +1)* sizeof (MarkovNodeFrequency));
    if (new_frq_lst == NULL){return false;}
    first_node ->frq_lst_size++;
    first_node ->frequencies_list = new_frq_lst;
    MarkovNodeFrequency new_mn;
    new_mn.markov_node = second_node;
    new_mn.frequency = 1;
    first_node ->frequencies_list[first_node ->frq_lst_size -1] = new_mn;
    return true;
}




Node* get_node_from_database(MarkovChain *markov_chain, char *data_ptr)
{
    LinkedList *database = markov_chain ->database;
    int size = database ->size;
    Node *temp = database -> first;
    if (!size){return NULL;}
    while (temp ->next != NULL) //if same data exists
    {
        char *word = temp ->data ->data;
        int flag4 = strcmp(word, data_ptr);
        if (!flag4){return temp;}
        temp = temp ->next;
    }
    return NULL;
}



MarkovNode *create_new_markov_node(char *data_ptr)
{
    MarkovNode  *new_node = malloc(sizeof (MarkovNode));
    if (new_node != NULL) {
        new_node ->frequencies_list = NULL;
        new_node ->frq_lst_size = 0;
        char *word = malloc(strlen(data_ptr) +1);
        new_node->frq_lst_size = 0;
        if (word != NULL) {
            strcpy(word, data_ptr);
            new_node->data = word;
            return new_node; //return new markov node
        } else { free(new_node);}
    }
    return NULL;
}


Node* add_to_database(MarkovChain *markov_chain, char *data_ptr)
{
    //if empty
    LinkedList *database = markov_chain ->database;
    Node *temp = database -> first;
    if( temp == database ->last)
    {
        MarkovNode *add_node = create_new_markov_node(data_ptr);
        if (add_node != NULL)
        {
            int flag1 = add(database, add_node);
            if (!flag1){markov_chain ->size_of_chain = 1;
                return database ->last;}
            return NULL;
        }
        return NULL;
    }
    //if exists
    while(temp)
    {
        MarkovNode *mnt = temp ->data;
        char *data_temp = mnt ->data;
        int flag2 = strcmp(data_temp, data_ptr);
        if (!flag2)
        {
            return temp;
        }
        temp = temp ->next;
    }
    //if doesnt exist
    MarkovNode *add_node = create_new_markov_node(data_ptr);
    if (add_node != NULL)
    {
        int flag3 = add(database, add_node);
        if (!flag3){markov_chain ->size_of_chain++;
            return database ->last;}
        return NULL;
    }
    return NULL;
}