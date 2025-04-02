import java.util.Random;

/**
 * A player that uses a strategy to choose its moves intelligently.
 */
class CleverPlayer implements Player {
    // The last cell chosen by the player.
    private int[] lastChosenCell;
    private Random rand;

    /**
     * Creates a CleverPlayer.
     */
    public CleverPlayer() {
        lastChosenCell = null;
        rand = new Random();
    }

    /**
     * Finds a blank cell adjacent to the last chosen cell.
     *
     * @param board the game board.
     * @param mark  the player's mark.
     * @return the row and column of the chosen cell, or null if none found.
     */
    private int[] algorithm(Board board, Mark mark) {
        if (lastChosenCell == null) {
            return null;
        }

        int row = lastChosenCell[0];
        int col = lastChosenCell[1];
        int boardSize = board.getSize();

        // Offsets for checking adjacent cells.
        int[][] offsets = {
                {-1, -1}, {-1, 0}, {-1, 1},
                { 0, -1},          { 0, 1},
                { 1, -1}, { 1, 0}, { 1, 1}
        };

        // Collect valid blank cells.
        int[][] validCells = new int[8][2];
        int validCount = 0;
        for (int[] offset : offsets) {
            int newRow = row + offset[0];
            int newCol = col + offset[1];
            if (newRow >= 0 && newRow < boardSize && newCol >= 0 && newCol < boardSize &&
                    board.getMark(newRow, newCol).toString() == "BLANK") {
                validCells[validCount++] = new int[]{newRow, newCol};
            }
        }

        // Return a random valid cell, or null if none found.
        if (validCount > 0) {
            Random rand = new Random();
            lastChosenCell = validCells[rand.nextInt(validCount)];
            return lastChosenCell;
        }
        return null;
    }

    /**
     * Plays the player's turn by placing a mark on the board.
     *
     * @param board the game board.
     * @param mark  the player's mark.
     */
    public void playTurn(Board board, Mark mark) {
        boolean putMarkSuccess = false;

        while (!putMarkSuccess) {
            // Try the center if the board size is odd.
            int size = board.getSize();
            if (size % 2 != 0) {
                int middle = size / 2;
                if (board.putMark(mark, middle, middle)) {
                    putMarkSuccess = true;
                    return;
                }
            }

            // Try an adjacent move using the algorithm.
            int[] chosenCell = algorithm(board, mark);
            if (chosenCell != null) {
                board.putMark(mark, chosenCell[0], chosenCell[1]);
                putMarkSuccess = true;
                return;
            }

            // Fallback to a random move.
            int randomRow = rand.nextInt(size);
            int randomCol = rand.nextInt(size);
            lastChosenCell = new int[]{randomRow, randomCol};
            putMarkSuccess = board.putMark(mark, randomRow, randomCol);
        }
    }
}
