public class Game {
    private Renderer renderer;
    private Player playerX;
    private Player playerO;
    private Board board;
    private int winStreak;

    /**
     * Checks if there is a winning streak horizontally or vertically for a given mark.
     *
     * @param board     the game board.
     * @param mark      the mark to check (X or O).
     * @param winStreak the number of consecutive marks needed to win.
     * @return true if a winning streak is found, false otherwise.
     */
    private boolean balancedOrVerticalGameOver(Board board, Mark mark, int winStreak) {
        int size = board.getSize();
        for (int i = 0; i < size; i++) {
            for (int k = 0; k < size - winStreak + 1; k++) {
                int rowsCounter = 0, colsCounter = 0;
                for (int j = k; j < winStreak + k; j++) {
                    if (board.getMark(j, i).toString() == mark.toString()) rowsCounter++;
                    if (board.getMark(i, j).toString() == mark.toString()) colsCounter++;
                }
                if (rowsCounter == winStreak || colsCounter == winStreak) return true;
            }
        }
        return false;
    }

    /**
     * Checks if there is a winning streak diagonally for a given mark.
     *
     * @param board     the game board.
     * @param mark      the mark to check (X or O).
     * @param winStreak the number of consecutive marks needed to win.
     * @return true if a diagonal winning streak is found, false otherwise.
     */
    private boolean slantGameOver(Board board, Mark mark, int winStreak) {
        int size = board.getSize();
        // Check top-left to bottom-right diagonals.
        for (int i = 0; i < size - winStreak + 1; i++) {
            for (int k = 0; k < size - winStreak + 1; k++) {
                int counter = 0;
                for (int j = 0; j < winStreak; j++) {
                    if (board.getMark(i + j, k + j).toString() == mark.toString()) counter++;
                }
                if (counter == winStreak) return true;
            }
        }
        // Check top-right to bottom-left diagonals.
        for (int i = 0; i < size - winStreak + 1; i++) {
            for (int k = size - 1; k > winStreak - 2; k--) {
                int counter = 0;
                for (int j = 0; j < winStreak; j++) {
                    if (board.getMark(i + j, k - j).toString() == mark.toString()) counter++;
                }
                if (counter == winStreak) return true;
            }
        }
        return false;
    }

    /**
     * Checks if a player has won the game.
     *
     * @param board     the game board.
     * @param mark      the mark to check (X or O).
     * @param winStreak the number of consecutive marks needed to win.
     * @return true if the player has won, false otherwise.
     */
    private boolean gameWon(Board board, Mark mark, int winStreak) {
        return balancedOrVerticalGameOver(board, mark, winStreak) || slantGameOver(board, mark, winStreak);
    }

    /**
     * Checks if the board is completely filled with marks.
     *
     * @param board the game board.
     * @return true if the board is full, false otherwise.
     */
    private boolean boardIsFull(Board board) {
        int size = board.getSize();
        for (int i = 0; i < size; i++) {
            for (int k = 0; k < size; k++) {
                if (board.getMark(i, k).toString() == Mark.BLANK.toString()) return false;
            }
        }
        return true;
    }

    /**
     * Constructs a game with default board size and win streak.
     *
     * @param playerX   the player using mark X.
     * @param playerO   the player using mark O.
     * @param renderer  the renderer for displaying the game.
     */
    public Game(Player playerX, Player playerO, Renderer renderer) {
        this.playerX = playerX;
        this.playerO = playerO;
        this.board = new Board();
        this.winStreak = board.getSize();
        this.renderer = renderer;
    }

    /**
     * Constructs a game with custom board size and win streak.
     *
     * @param playerX   the player using mark X.
     * @param playerO   the player using mark O.
     * @param size      the size of the board.
     * @param winStreak the number of consecutive marks needed to win.
     * @param renderer  the renderer for displaying the game.
     */
    public Game(Player playerX, Player playerO, int size, int winStreak, Renderer renderer) {
        this.playerX = playerX;
        this.playerO = playerO;
        this.board = new Board(size);
        this.winStreak = winStreak;
        this.renderer = renderer;
    }

    public int getWinStreak() {
        return winStreak;
    }

    public int getBoardSize() {
        return board.getSize();
    }

    /**
     * Runs the game loop until a player wins or the board is full.
     *
     * @return the winning mark (X or O), or BLANK if it's a draw.
     */
    public Mark run() {
        while (true) {
            playerX.playTurn(board, Mark.X);
            renderer.renderBoard(board);
            if (gameWon(board, Mark.X, winStreak)) return Mark.X;
            if (boardIsFull(board)) return Mark.BLANK;

            playerO.playTurn(board, Mark.O);
            renderer.renderBoard(board);
            if (gameWon(board, Mark.O, winStreak)) return Mark.O;
            if (boardIsFull(board)) return Mark.BLANK;
        }
    }
}
