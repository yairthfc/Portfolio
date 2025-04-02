package ex5.validation;

/**
 * The InvalidSyntaxException class represents an exception that is
 * thrown when the syntax of the code is invalid.
 */
public class InvalidSyntaxException extends Exception {

    /**
     * Constructs a new InvalidSyntaxException with the specified detail message.
     *
     * @param message the detail message
     */
    public InvalidSyntaxException(String message) {
        super(message);
    }

    /**
     * Constructs a new InvalidSyntaxException with no detail message.
     */
    public InvalidSyntaxException(){super();}
}
