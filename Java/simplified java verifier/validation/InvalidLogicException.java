package ex5.validation;

/**
 * The InvalidLogicException class represents an exception that is thrown when a
 * logical error occurs in the code.
 */
public class InvalidLogicException extends Exception {

    /**
     * Constructs a new InvalidLogicException with the specified detail message.
     *
     * @param message the detail message
     */
    public InvalidLogicException(String message) {
        super(message);
    }

    /**
     * Constructs a new InvalidLogicException with no detail message.
     */
    public InvalidLogicException(){super();}
}
