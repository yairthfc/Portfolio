public enum Mark {
    BLANK, X, O; // Enum values representing the possible marks

    /**
     * Converts the enum value to its corresponding string representation.
     *
     * @return String representation of the mark.
     */
    public String toString() {
        // Switch case to return the corresponding string for each enum value
        switch (this) {
            case BLANK:
                return "BLANK";
            case X:
                return "X";
            case O:
                return "O";
            default:
                throw new IllegalStateException("Unexpected value: " + this);
        }
    }
}
