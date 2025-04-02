#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "markov_chain.h"
#include "linked_list.h"

#define BASE 10
#define WORDS_TO_READ_CONSTANT 5
#define NO_LIMIT -1
#define MAX_CORDS_IN_SENTENCE 1000
#define MAX_CORDS_IN_WORD 100
#define MAX_WORDS_TWEET 20

static void print_a_word(void* data){
    char *word = data;
    printf(" %s", word);
}

static int compare_words(void* data1, void* data2){
    char* word1 = data1;
    char* word2 = data2;
    return strcmp(word1, word2);
}

static void free_word(void *ptr){
    free(ptr);
}

static void* copy_word(void* ptr){
    char* word = malloc(strlen(ptr) + 1);
    if (word != NULL) {
        strcpy(word, ptr);
        return word;
    }
    else {return NULL;}
}

static bool is_last_word(void* ptr){
    char* word = ptr;
    if(word[strlen(word) - 1] == '.') //if ends with '.'
    {
        return true;
    }
    return false;
}


int fill_database(FILE *fp, int words_to_read, MarkovChain*markov_chain)
{
    int words_count = 0;
    char cur_line[MAX_CORDS_IN_SENTENCE];
    if (words_to_read != -1) { //if no words to read limit
        while (fgets(cur_line, sizeof (cur_line),
                     fp)&& words_count <words_to_read) {
            Node *last_node = NULL;
            char *word = strtok(cur_line, " \r\t\n");
            while (word != NULL && words_count < words_to_read) {
                Node *node = add_to_database(markov_chain, word);
                if (!node) { return EXIT_FAILURE; }
                if (last_node && !markov_chain->is_last(last_node ->data
                ->data)) {add_node_to_frequencies_list(
            last_node->data, node->data, markov_chain);
                }
                last_node = node;
                words_count++;
                word = strtok(NULL, " \r\t\n");

            }
        }
    }
    else { //if words to read limit
        while (fgets(cur_line, MAX_CORDS_IN_SENTENCE, fp)) {
            Node *last_node = NULL;
            char *word = strtok(cur_line, " \r\t\n"); //line/space
            while (word != NULL) {
                Node *node = add_to_database(markov_chain, word);
                if (!node) { return EXIT_FAILURE; }
                if (last_node && !markov_chain->is_last(last_node ->data
                ->data)) {add_node_to_frequencies_list
                (last_node->data, node->data, markov_chain);
                }
                last_node = node;
                word = strtok(NULL, " \r\t\n");
            }
        }
    }
    return EXIT_SUCCESS;
}





//int main(int argc, char *argv[]){
//    if (argc < 4 || argc > WORDS_TO_READ_CONSTANT){ fprintf(stdout,
//                            "Usage: Invalid number of arguments.");
//        return EXIT_FAILURE;}
//    unsigned long int seed = strtoul(argv[1], NULL, BASE);
//    srand(seed);
//    FILE *in_file = fopen(argv[3], "r"); //open
//    if(in_file == NULL)
//    {
//        fprintf(stdout, "Error: The file path given is invalid.\n");
//        return EXIT_FAILURE;
//    }
//    int number_of_tweets;
//    sscanf(argv[2], "%d", &number_of_tweets);
//    int number_of_words_to_read;
//    if (argc == WORDS_TO_READ_CONSTANT){sscanf(argv[4], "%d",
//                                               &number_of_words_to_read);}
//    else{number_of_words_to_read = NO_LIMIT;}
//    MarkovChain *markov_chain = calloc(1,sizeof (MarkovChain));
//    LinkedList *database = calloc(1, sizeof (LinkedList));
//    if (!database || !markov_chain){
//        fprintf (stdout, "Error: calloc failed.\n");
//        return EXIT_FAILURE;}
//    markov_chain ->is_last = is_last_word;
//    markov_chain ->comp_func = compare_words;
//    markov_chain ->free_data = free_word;
//    markov_chain ->copy_func = copy_word;
//    markov_chain ->print_func = print_a_word;
//    markov_chain ->database = database;
//    database ->first = NULL;
//    database ->last = NULL;
//    int flagged = fill_database(in_file, //fill database
//                number_of_words_to_read, markov_chain);
//    if (flagged)
//    {
//        free_database(&markov_chain);
//        free(markov_chain); //free if didnt work
//        return EXIT_FAILURE;
//    }
//    fclose(in_file);
//    for (int i = 0; i <= number_of_tweets-1; i++) //make tweets
//    {
//        MarkovNode* first_node = get_first_random_node (markov_chain);
//        printf("Tweet %d:", i+1);
//        generate_tweet (markov_chain, first_node, MAX_WORDS_TWEET);
//        printf("\n");
//    }
//    free_database(&markov_chain); //free
//    free(markov_chain);
//    EXIT_SUCCESS;
//}