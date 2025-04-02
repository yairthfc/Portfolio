CC = gcc
CFLAGS = -Wall -Wextra
LIBS = -lm

# Main targets
all: snake tweets

# Snakes and Ladders program
snake: snakes_and_ladders.o markov_chain.o linked_list.o
	$(CC) $(CFLAGS) -o snake snakes_and_ladders.o markov_chain.o linked_list.o $(LIBS)

snakes_and_ladders.o: snakes_and_ladders.c markov_chain.h linked_list.h
	$(CC) $(CFLAGS) -c snakes_and_ladders.c

markov_chain.o: markov_chain.c markov_chain.h linked_list.h
	$(CC) $(CFLAGS) -c markov_chain.c

linked_list.o: linked_list.c linked_list.h
	$(CC) $(CFLAGS) -c linked_list.c

# Tweets Generator program
tweets: tweets_generator.o markov_chain.o linked_list.o
	$(CC) $(CFLAGS) -o tweets tweets_generator.o markov_chain.o linked_list.o $(LIBS)

tweets_generator.o: tweets_generator.c markov_chain.h linked_list.h
	$(CC) $(CFLAGS) -c tweets_generator.c

# Cleanup
clean:
	rm -f snake tweets *.o
