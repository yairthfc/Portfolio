public class HumanPlayer implements Player {

    public HumanPlayer() {} // Constructor for HumanPlayer

    /**
     * Prompts the user to input coordinates and places the mark on the board.
     *
     * @param board The game board.
     * @param mark  The player's mark (X or O).
     */
    public void playTurn(Board board, Mark mark) {
        boolean putMarkSuccess = false; // Indicates if the mark was successfully placed
        boolean firstTry = true; // Flag to indicate if it's the first attempt to place a mark

        while (!putMarkSuccess) {
            if (firstTry) {
                System.out.println("Player " + mark.toString() + ", type coordinates:");
                firstTry = false; // Set flag to false after the first prompt
            }

            // Read the coordinate input from the user
            int num = KeyboardInput.readInt();
            int row = num / 10;  // Extract row from input
            int col = num % 10;  // Extract column from input

            // Check if the chosen position is within bounds
            if (row >= board.getSize() || col >= board.getSize()) {
                System.out.println("Invalid mark position. Please choose a valid position:");
                continue; // Ask for a valid position if out of bounds
            }

            // Check if the position is already occupied
            if (board.getMark(row, col).toString() != "BLANK") {
                System.out.println("Mark position is already occupied. Please choose a valid position:");
                continue; // Ask for a valid position if occupied
            }

            // Try to place the mark on the board
            putMarkSuccess = board.putMark(mark, row, col);
        }
    }
}
