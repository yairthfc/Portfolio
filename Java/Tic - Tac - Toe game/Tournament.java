public class Tournament {
    private Player player1; // Player 1 in the tournament
    private Player player2; // Player 2 in the tournament
    private int rounds; // Number of rounds to be played
    private Renderer renderer; // Renderer used to display the game

    /**
     * Constructor to initialize the tournament with the given parameters.
     * @param rounds Total rounds to be played in the tournament.
     * @param renderer Renderer used to visualize the game.
     * @param player1 Player 1 participating in the tournament.
     * @param player2 Player 2 participating in the tournament.
     */
    public Tournament(int rounds, Renderer renderer, Player player1, Player player2){
        this.player1 = player1;
        this.player2 = player2;
        this.rounds = rounds;
        this.renderer = renderer;
    }

    /**
     * Runs the tournament and tracks the number of wins for each player and ties.
     * @param size The size of the game board.
     * @param winStreak The number of consecutive marks required to win.
     * @param playerName1 Name of Player 1.
     * @param playerName2 Name of Player 2.
     */
    public void playTournament(int size, int winStreak, String playerName1, String playerName2){
        int player1Wins = 0; // Tracks the number of wins for Player 1
        int player2Wins = 0; // Tracks the number of wins for Player 2
        int ties = 0; // Tracks the number of ties in the tournament

        // Loop through the rounds of the tournament
        for(int i = 0; i < rounds; i++){
            // Alternate the starting player each round
            if(i % 2 == 0){
                Game game = new Game(player1, player2, size, winStreak, renderer); // Player 1 starts
                Mark winner = game.run(); // Run the game and get the winner

                // Update the win/tie count based on the result
                if(winner == Mark.X){
                    player1Wins++; // Player 1 wins
                } else if(winner == Mark.O){
                    player2Wins++; // Player 2 wins
                } else {
                    ties++; // Tie
                }
            }
            else {
                Game game = new Game(player2, player1, size, winStreak, renderer); // Player 2 starts
                Mark winner = game.run(); // Run the game and get the winner

                // Update the win/tie count based on the result
                if(winner == Mark.X){
                    player2Wins++; // Player 2 wins
                } else if(winner == Mark.O){
                    player1Wins++; // Player 1 wins
                } else {
                    ties++; // Tie
                }
            }
        }

        // Display the final results of the tournament
        System.out.println("######### Results #########");
        System.out.println("Player 1, " + playerName1 + " won: " + player1Wins + " rounds");
        System.out.println("Player 2, " + playerName2 + " won: " + player2Wins + " rounds");
        System.out.println("Ties: " + ties);
    }

    /**
     * Main method to start the tournament based on command-line arguments.
     * @param args Command-line arguments to configure the tournament (rounds, board size, player types).
     */
    public static void main(String[] args){
        // Instantiate factories for renderer and players
        RendererFactory rendererFactory = new RendererFactory();
        PlayerFactory playerFactory = new PlayerFactory();

        // Create the renderer and players based on input arguments
        Renderer renderer = rendererFactory.buildRenderer(args[3], Integer.parseInt(args[1]));
        Player player1 = playerFactory.buildPlayer(args[4]);
        Player player2 = playerFactory.buildPlayer(args[5]);

        // Create the tournament instance and start it
        Tournament tournament = new Tournament(Integer.parseInt(args[0]), renderer, player1, player2);
        tournament.playTournament(Integer.parseInt(args[1]), Integer.parseInt(args[2]), args[4], args[5]);
    }
}
