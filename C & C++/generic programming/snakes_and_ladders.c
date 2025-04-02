#include <string.h> // For strlen(), strcmp(), strcpy()
#include "markov_chain.h"

#define MAX(X, Y) (((X) < (Y)) ? (Y) : (X))
#define ARGS_NUM 3
#define EMPTY -1
#define BOARD_SIZE 100
#define MAX_GENERATION_LENGTH 60
#define BASE 10
#define DICE_MAX 6
#define NUM_OF_TRANSITIONS 20

/**
 * represents the transitions by ladders and snakes in the game
 * each tuple (x,y) represents a ladder from x to if x<y or a snake otherwise
 */
const int transitions[][2] = {{13, 4},
                              {85, 17},
                              {95, 67},
                              {97, 58},
                              {66, 89},
                              {87, 31},
                              {57, 83},
                              {91, 25},
                              {28, 50},
                              {35, 11},
                              {8,  30},
                              {41, 62},
                              {81, 43},
                              {69, 32},
                              {20, 39},
                              {33, 70},
                              {79, 99},
                              {23, 76},
                              {15, 47},
                              {61, 14}};

/**
 * struct represents a Cell in the game board
 */
typedef struct Cell {
    int number; // Cell number 1-100
    int ladder_to;  // ladder_to represents the jump of the ladder in case there is one from this square
    int snake_to;  // snake_to represents the jump of the snake in case there is one from this square
    //both ladder_to and snake_to should be -1 if the Cell doesn't have them
} Cell;

static void print_cell(void* cell)
{
    Cell *cell1 = cell;
    if (cell1->snake_to != EMPTY)
    {
        printf(" [%d]-snake to %d ->", cell1->number, cell1->snake_to);
    }
    if (cell1->snake_to != EMPTY)
    {
        printf(" [%d]-ladder to %d ->", cell1->number, cell1->ladder_to);
    }
    else {
        printf(" [%d] ->", cell1->number);
    }
}

static int comp_cells_func(void* data1, void* data2)
{
    Cell *cell1 = data1;
    Cell *cell2 = data2;
    if (cell1->number == cell2->number){return EXIT_FAILURE;}
    else{return EXIT_SUCCESS;}
}

static void free_cell(void* ptr)
{
    Cell *cell = ptr;
    free(cell);
}

static void* copy_cell(void* ptr)
{
    Cell *cell = ptr;
    Cell *new_cell = calloc(1, sizeof (Cell));
    new_cell ->number = cell->number;
    new_cell->snake_to = cell->snake_to;
    new_cell->ladder_to = cell->ladder_to;
    return cell;
}

static bool is_last_cell(void* ptr)
{
    Cell *cell = ptr;
    if(cell->number == BOARD_SIZE){ return true;}
    return false;
}


/** Error handler **/
static int handle_error(char *error_msg, MarkovChain **database)
{
    printf("%s", error_msg);
    if (database != NULL)
    {
        free_database(database);
    }
    return EXIT_FAILURE;
}


static int create_board(Cell *cells[BOARD_SIZE])
{
    for (int i = 0; i < BOARD_SIZE; i++)
    {
        cells[i] = malloc(sizeof(Cell));
        if (cells[i] == NULL)
        {
            for (int j = 0; j < i; j++) {
                free(cells[j]);
            }
            handle_error(ALLOCATION_ERROR_MASSAGE,NULL);
            return EXIT_FAILURE;
        }
        *(cells[i]) = (Cell) {i + 1, EMPTY, EMPTY};
    }

    for (int i = 0; i < NUM_OF_TRANSITIONS; i++)
    {
        int from = transitions[i][0];
        int to = transitions[i][1];
        if (from < to)
        {
            cells[from - 1]->ladder_to = to;
        }
        else
        {
            cells[from - 1]->snake_to = to;
        }
    }
    return EXIT_SUCCESS;
}

/**
 * fills database
 * @param markov_chain
 * @return EXIT_SUCCESS or EXIT_FAILURE
 */
static int fill_database(MarkovChain *markov_chain)
{
    Cell* cells[BOARD_SIZE];
    if(create_board(cells) == EXIT_FAILURE)
    {
        return EXIT_FAILURE;
    }
    MarkovNode *from_node = NULL, *to_node = NULL;
    size_t index_to;
    for (size_t i = 0; i < BOARD_SIZE; i++)
    {
        add_to_database(markov_chain, cells[i]);
    }

    for (size_t i = 0; i < BOARD_SIZE; i++)
    {
        from_node = get_node_from_database(markov_chain,cells[i])->data;

        if (cells[i]->snake_to != EMPTY || cells[i]->ladder_to != EMPTY)
        {
            index_to = MAX(cells[i]->snake_to,cells[i]->ladder_to) - 1;
            to_node = get_node_from_database(markov_chain, cells[index_to])
                    ->data;
            add_node_to_frequencies_list (from_node, to_node, markov_chain);
        }
        else
        {
            for (int j = 1; j <= DICE_MAX; j++)
            {
                index_to = ((Cell*) (from_node->data))->number + j - 1;
                if (index_to >= BOARD_SIZE)
                {
                    break;
                }
                to_node = get_node_from_database(markov_chain, cells[index_to])
                        ->data;
                add_node_to_frequencies_list (from_node, to_node, markov_chain);
            }
        }
    }
    // free temp arr
    for (size_t i = 0; i < BOARD_SIZE; i++)
    {
        free(cells[i]);
    }
    return EXIT_SUCCESS;
}

/**
 * @param argc num of arguments
 * @param argv 1) Seed
 *             2) Number of sentences to generate
 * @return EXIT_SUCCESS or EXIT_FAILURE
 */
int main(int argc, char *argv[])
{
    if (argc != ARGS_NUM){ fprintf(stdout,
    "Usage: Invalid number of arguments.");
    return EXIT_FAILURE;}
    unsigned long int seed = strtoul(argv[1], NULL,BASE);
    srand(seed);
    int number_of_routs;
    sscanf(argv[2], "%d", &number_of_routs);
    MarkovChain *markov_chain = calloc(1, sizeof (MarkovChain));
    LinkedList *database = calloc(1, sizeof (LinkedList));
    if (!database || !markov_chain){
        fprintf (stdout, "Error: malloc failed.\n");
        return EXIT_FAILURE;}
    markov_chain->database = database;
    markov_chain->database->first = NULL;
    markov_chain->database->last = NULL;
    markov_chain->print_func = print_cell;
    markov_chain->copy_func = copy_cell;
    markov_chain->free_data = free_cell;
    markov_chain->comp_func = comp_cells_func;
    markov_chain->is_last = is_last_cell;
    int flagged = fill_database(markov_chain);
    if (flagged){
        printf("Error: filling database has failed.");
        free_database(&markov_chain);
        free(markov_chain);
        return EXIT_FAILURE;
    }
    for (int i = 0; i< number_of_routs; i++)
    {
        printf("Random Walk %d:", i+1);
        generate_tweet (markov_chain,database->first->data,
                        MAX_GENERATION_LENGTH);
        printf("\n");
    }
    free_database(&markov_chain);
    free(markov_chain);
    EXIT_SUCCESS;
}
