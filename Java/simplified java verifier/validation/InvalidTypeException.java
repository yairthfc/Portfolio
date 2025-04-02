package ex5.validation;

/**
 * The InvalidTypeException class represents an exception that is thrown when a
 * variable type is invalid.
 */
public class InvalidTypeException extends Exception{
    /**
     * Constructs a new InvalidTypeException with the specified detail message.
     *
     * @param message the detail message
     */
    public InvalidTypeException(String message) {
        super(message);
    }

    /**
     * Constructs a new InvalidTypeException with no detail message.
     */
    public InvalidTypeException(){super();}
}
