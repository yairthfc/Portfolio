package ex5.validation;

/**
 * The InvalidNameException class represents an exception that is thrown when a variable
 * or method name is invalid.
 */
public class InvalidNameException extends Exception{
    /**
     * Constructs a new InvalidNameException with the specified detail message.
     *
     * @param message the detail message
     */
    public InvalidNameException(String message){super(message);}


    /**
     * Constructs a new InvalidNameException with no detail message.
     */
    public InvalidNameException(){super();}
}
