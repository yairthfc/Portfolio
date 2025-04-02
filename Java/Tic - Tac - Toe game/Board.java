/**
 * Represents a square game board where each cell can hold a mark.
 * Supports board initialization, querying marks, and placing marks.
 */
public class Board {

    // Default size of the board.
    private final int DEFAULT_SIZE = 4;

    // 2D array representing the board's grid.
    private final Mark[][] board;

    // Number of rows/columns on the board.
    private int size;

    /**
     * Creates a board with the default size (4x4).
     */
    public Board() {
        board = new Mark[DEFAULT_SIZE][DEFAULT_SIZE];
        size = DEFAULT_SIZE;
        initializeBoard();
    }

    /**
     * Creates a board with a specified size.
     *
     * @param size the size of the board.
     */
    public Board(int size) {
        board = new Mark[size][size];
        this.size = size;
        initializeBoard();
    }

    /**
     * Returns the size of the board.
     *
     * @return the size of the board.
     */
    public int getSize() {
        return size;
    }

    /**
     * Places a mark at the specified position if the cell is empty.
     *
     * @param mark the mark to place.
     * @param row  the row index.
     * @param col  the column index.
     * @return true if the mark was placed, false otherwise.
     */
    public boolean putMark(Mark mark, int row, int col) {
        Mark currentMark = getMark(row, col);
        if (currentMark == null || currentMark == Mark.BLANK) {
            board[row][col] = mark;
            return true;
        }
        return false;
    }

    /**
     * Retrieves the mark at the specified position.
     *
     * @param row the row index.
     * @param col the column index.
     * @return the mark at the position, or null if the cell is uninitialized.
     */
    public Mark getMark(int row, int col) {
        return board[row][col];
    }

    // Initializes all cells in the board to Mark.BLANK.
    private void initializeBoard() {
        for (int i = 0; i < size; i++) {
            for (int j = 0; j < size; j++) {
                board[i][j] = Mark.BLANK;
            }
        }
    }
}
