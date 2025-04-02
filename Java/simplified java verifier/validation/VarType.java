package ex5.validation;

/**
 * The VarType enum represents various data types in Java code and
 * provides utility methods for type validation and conversion.
 */
public enum VarType {


    /**
     * Represents the integer data type.
     */
    INT,

    /**
     * Represents the double data type.
     */
    DOUBLE,

    /**
     * Represents the string data type.
     */
    STRING,

    /**
     * Represents the boolean data type.
     */
    BOOLEAN,

    /**
     * Represents the char data type.
     */
    CHAR;

    /**
     * Checks if the given type string is a valid VarType.
     *
     * @param type the type string to check
     * @return true if the type string is a valid VarType, false otherwise
     */
    public static boolean isValidType(String type) {
        try {
            VarType.valueOf(type.toUpperCase());
            return true;
        } catch (IllegalArgumentException e) {
            return false;
        }
    }

    /**
     * Converts a type string to its corresponding VarType.
     *
     * @param type the type string to convert
     * @return the corresponding VarType, or null if the type string is invalid
     */
    public static VarType fromString(String type) {
        switch (type) {
            case "int":
                return VarType.INT;
            case "double":
                return VarType.DOUBLE;
            case "String":
                return VarType.STRING;
            case "boolean":
                return VarType.BOOLEAN;
            case "char":
                return VarType.CHAR;
            default:
                return null;
        }
    }
}
