import java.util.Random;

class GeniusPlayer implements Player {
    private int[] lastChosenCell; // Last cell chosen by the player
    private int[] currentDirection; // Direction for sequential moves
    private Random rand;

    public GeniusPlayer() {
        lastChosenCell = null;
        currentDirection = null;
        rand = new Random();
    } // Constructor for GeniusPlayer

    /**
     * Determines the next move based on the last chosen cell and direction.
     *
     * @param board The game board.
     * @param mark  The player's mark (X or O).
     * @return The next move as {row, col}, or null if no move is found.
     */
    private int[] algorithm(Board board, Mark mark) {
        if (lastChosenCell == null) return null; // No prior move to calculate from
        int row = lastChosenCell[0];
        int col = lastChosenCell[1];
        int boardSize = board.getSize();
        // All possible movement directions: vertical, horizontal, and diagonals
        int[][] offsets = {
                {-1, 0}, {1, 0},  // Vertical
                {0, -1}, {0, 1},  // Horizontal
                {-1, -1}, {1, 1}, // Main diagonal
                {-1, 1}, {1, -1}  // Anti-diagonal
        };
        // Try continuing in the current direction
        if (currentDirection != null) {
            int[] nextMove = moveInLine(board, row, col, boardSize, currentDirection);
            if (nextMove != null) {
                lastChosenCell = nextMove;
                return nextMove;
            }
            // If blocked, try the opposite direction
            int[] oppositeDirection = {-currentDirection[0], -currentDirection[1]};
            nextMove = moveInLine(board, row, col, boardSize, oppositeDirection);
            if (nextMove != null) {
                currentDirection = oppositeDirection;
                lastChosenCell = nextMove;
                return nextMove;}
        }
        // Try new directions if current and opposite directions are blocked
        for (int i = 0; i < offsets.length; i += 2) {
            int[] forward = offsets[i];
            int[] backward = offsets[i + 1];
            int[] forwardMove = moveInLine(board, row, col, boardSize, forward);
            if (forwardMove != null) {
                currentDirection = forward;
                lastChosenCell = forwardMove;
                return forwardMove;
            }
            int[] backwardMove = moveInLine(board, row, col, boardSize, backward);
            if (backwardMove != null) {
                currentDirection = backward;
                lastChosenCell = backwardMove;
                return backwardMove;}
        }
        return null; // No valid moves found
    }

    /**
     * Moves along the given direction until a valid cell is found or the boundary is reached.
     *
     * @param board      The game board.
     * @param row        Current row position.
     * @param col        Current column position.
     * @param boardSize  Size of the board.
     * @param direction  Movement direction as {rowOffset, colOffset}.
     * @return The next valid cell as {row, col}, or null if no valid cell is found.
     */
    private int[] moveInLine(Board board, int row, int col, int boardSize, int[] direction) {
        while (true) {
            row += direction[0];
            col += direction[1];

            if (!isWithinBounds(row, col, boardSize) || board.getMark(row, col) != Mark.BLANK) {
                return null; // Stop if out of bounds or cell is occupied
            }

            return new int[]{row, col}; // Return the first valid cell
        }
    }

    /**
     * Checks if a cell is within the bounds of the board.
     *
     * @param row       Row index.
     * @param col       Column index.
     * @param boardSize Size of the board.
     * @return True if the cell is within bounds, false otherwise.
     */
    private boolean isWithinBounds(int row, int col, int boardSize) {
        return row >= 0 && row < boardSize && col >= 0 && col < boardSize;
    }

    /**
     * Plays a turn for the GeniusPlayer.
     *
     * @param board The game board.
     * @param mark  The player's mark (X or O).
     */
    public void playTurn(Board board, Mark mark) {
        int size = board.getSize();
        boolean putMarkSuccess = false;

        while (!putMarkSuccess) {
            if (size % 2 != 0) { // Attempt center move on odd-sized board
                int middle = size / 2;
                if (board.putMark(mark, middle, middle)) {
                    lastChosenCell = new int[]{middle, middle};
                    return;
                }
            }

            int[] chosenCell = algorithm(board, mark); // Use algorithm to find a move
            if (chosenCell != null) {
                board.putMark(mark, chosenCell[0], chosenCell[1]);
                return;
            }

            // Fallback: random move
            int randomRow = rand.nextInt(board.getSize());
            int randomCol = rand.nextInt(board.getSize());
            putMarkSuccess = board.putMark(mark, randomRow, randomCol);
            lastChosenCell = new int[]{randomRow, randomCol};
        }
    }
}
