import java.util.Random;

class WhateverPlayer implements Player{
    private Random rand;

    public WhateverPlayer(){
        rand  = new Random();
    }

    /**
     * Method for playing a turn.
     * @param board The game board where the move will be played.
     * @param mark The mark ('X' or 'O') that the player will place on the board.
     */
    public void playTurn(Board board, Mark mark){
        boolean putMarkSuccess = false;
        while(!putMarkSuccess) {
            int randomRow = rand.nextInt(board.getSize());  // Random row selection
            int randomCol = rand.nextInt(board.getSize());  // Random column selection

            // Attempts to place the mark at the random position
            putMarkSuccess = board.putMark(mark, randomRow, randomCol);
        }
    }
}
