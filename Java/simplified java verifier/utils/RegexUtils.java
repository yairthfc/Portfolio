package ex5.utils;

import ex5.validation.VarType;
import java.util.HashMap;
import java.util.Map;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * The RegexUtils class provides utility methods for validating and parsing various types of strings
 * in Java code, such as variable names, method names, and different data types.
 */
public class RegexUtils {

    /**
     * Checks if a line is a comment.
     *
     * @param line the line of code to check
     * @return true if the line is a comment, false otherwise
     */
    public static Boolean isComment(String line){
        line = line.trim();
        return line.trim().startsWith("//");
    }

    /**
     * Checks if a line is an integer.
     *
     * @param line the line of code to check
     * @return true if the line is an integer, false otherwise
     */
    public static Boolean isInteger(String line){
        line = line.trim();
        return line.matches("-?\\d+");
    }


    /**
     * Checks if a line is a double.
     *
     * @param line the line of code to check
     * @return true if the line is a double, false otherwise
     */
    public static Boolean isDouble(String line){
        line = line.trim();
        return line.matches("-?\\d+\\.\\d+");
    }

    /**
     * Checks if a line is a boolean.
     *
     * @param line the line of code to check
     * @return true if the line is a boolean, false otherwise
     */
    public static Boolean isBoolean(String line){
        line = line.trim();
        return line.matches("true|false");
    }

    /**
     * Checks if a line is a string.
     *
     * @param line the line of code to check
     * @return true if the line is a string, false otherwise
     */
    public static Boolean isString(String line){
        line = line.trim();
        return line.matches("\".*\"");
    }

    /**
     * Checks if a line is a char.
     *
     * @param line the line of code to check
     * @return true if the line is a char, false otherwise
     */
    public static Boolean isChar(String line){
        line = line.trim();
        return line.matches("'.{1}'");}

    /**
     * Checks if a line is a valid variable name.
     *
     * @param line the line of code to check
     * @return true if the line is a valid variable name, false otherwise
     */
    public static Boolean isValidVariableName(String line){
        line = line.trim();
        return line.matches("^(?!\\d)(?!__)[a-zA-Z0-9_]+$");

    }
    /**
     * Checks if a line is a valid method name.
     *
     * @param line the line of code to check
     * @return true if the line is a valid method name, false otherwise
     */
    public static Boolean isValidMethodName(String line){
        line = line.trim();
            return line.matches("^(?!\\d)(?!_)[a-zA-Z0-9_]+$");

    }



    /**
     * Checks if a line is a valid method start structure.
     *
     * @param line the line of code to check
     * @return true if the line is a valid method start structure, false otherwise
     */
    public static Boolean isValidMethodStartStructure(String line) {

        line = line.trim();


        if (!line.startsWith("void ")) {
            return false;
        }
        if (!line.endsWith("{")){
            return false;
        }
        if (!CheckParam(line)){
            return false;
        }
        String methodName = getMethodName(line);
        return isValidMethodName(methodName);

    }

    /**
     * Checks if the parameters in a method declaration are valid.
     *
     * @param line the line of code to check
     * @return true if the parameters are valid, false otherwise
     */
    private static boolean CheckParam(String line){
        String regex = "\\(([^)]*)\\)";
        Pattern pattern = Pattern.compile(regex);
        Matcher matcher = pattern.matcher(line);
        if (matcher.find()) {
            if (matcher.group(1).isEmpty()){
                return true;
            }
            for (String param : matcher.group(1).split(",")) {
                if (!param.trim().matches
                        ("^(int|String|float|boolean|char)\\s+[a-zA-Z_][a-zA-Z0-9_]*$")) {
                    return false;
                }
            }

           return true;
        }
        return false;
    }

    /**
     * Extracts the method name from a line.
     *
     * @param line the line of code to extract the method name from
     * @return the method name, or null if the line is invalid
     */
    public static String getMethodName(String line) {
        String regex = "^void\\s+([a-zA-Z0-9_]+)\\s*\\(.*\\)\\s*\\{?$";
        Pattern pattern = Pattern.compile(regex);
        Matcher matcher = pattern.matcher(line);
        String methodName;
        if (matcher.find()) {
           return matcher.group(1);}
        return null;

    }

    /**
     * Extracts method parameters as a list of VarType objects.
     *
     * @param line the line of code to extract the method parameters from
     * @return a map of parameter names to their types
     */
    public static Map<String, Map<String, VarType>> getMethodParameters(String line) {
        String regex = "^void\\s+[a-zA-Z0-9_]+\\s*\\((.*)\\)\\s*\\{?$";

        Map<String, Map<String, VarType>> outerMap = new HashMap<>();
        outerMap.put("F", new HashMap<>()); // For final parameters
        outerMap.put("NF", new HashMap<>()); // For non-final parameters

        if (line.matches(regex)) {
            String parameterList = line.replaceAll(regex, "$1").trim();

            if (!parameterList.isEmpty()) {
                String[] paramArray = parameterList.split("\\s*,\\s*");

                for (String param : paramArray) {
                    String[] parts = param.trim().split("\\s+");

                    // Handle "final" keyword if present
                    boolean isFinal = false;
                    int offset = 0;
                    if (parts[0].equals("final")) {
                        isFinal = true;
                        offset = 1; // Shift index to consider the actual type
                    }

                    // Ensure the parameter format is valid
                    if (parts.length == 2 + offset) {
                        String type = parts[offset];
                        String name = parts[offset + 1];

                        if (VarType.isValidType(type) && isValidVariableName(name)) {
                            // Add to appropriate map based on "final" status
                            if (isFinal) {
                                outerMap.get("F").put(name, VarType.valueOf(type.toUpperCase()));
                            } else {
                                outerMap.get("NF").put(name, VarType.valueOf(type.toUpperCase()));
                            }
                        } else {
                            return null; // Invalid type or variable name
                        }
                    } else {
                        return null; // Each parameter must have exactly a type and a name
                    }
                }
            }
        }

        return outerMap;
    }


    /**
     * Checks if a line is an if statement.
     *
     * @param line the line of code to check
     * @return true if the line is an if statement, false otherwise
     */
    public static boolean isIfStatement(String line){
        return line.matches("^if\\s*\\(.*\\)\\s*\\{?$");
    }

    /**
     * Checks if a line is a while statement.
     *
     * @param line the line of code to check
     * @return true if the line is a while statement, false otherwise
     */
    public static boolean isWhileStatement(String line){
        return line.matches("^while\\s*\\(.*\\)\\s*\\{?$");
    }

    /**
     * Checks if a line is a return statement.
     *
     * @param line the line of code to check
     * @return true if the line is a return statement, false otherwise
     */
    public static boolean isReturnStatement(String line){
        line = line.trim();
        return line.matches("^return\\s*.*;?$");
    }

    /**
     * Checks if a line is a method call.
     *
     * @param line the line of code to check
     * @return true if the line is a method call, false otherwise
     */
    public static boolean isMethodCall(String line) {
        return line.trim().matches("^[a-zA-Z_][a-zA-Z0-9_]*\\s*\\(.*\\);?$");
    }


    /**
     * Checks if a line is a variable declaration.
     *
     * @param line the line of code to check
     * @return true if the line is a variable declaration, false otherwise
     */
    public static boolean isEmpty(String line) {
        return line == null || line.trim().isEmpty();
    }




    /**
     * Determines the action type of a line.
     *
     * @param line the line of code to check
     * @return the action type of the line
     */
    public static String getActionType(String line){
        if (isReturnStatement(line)){
            return "return";
        }
        if (isIfStatement(line) || isWhileStatement(line)){
            return "blockStart";
        }
        if (line.trim().endsWith("}")){
            return "blockEnd";
        }
        if (isMethodCall(line)){
            return "method";
        }
        if (isValidMethodStartStructure(line)){
            return "methodDeclaration";
        }
         if(line.endsWith(";")){
            if(line.trim().startsWith("int") ||
                    line.trim().startsWith("double") || line.trim().startsWith("char") ||
                    line.trim().startsWith("String") || line.trim().startsWith("boolean")
                    || line.trim().startsWith("final")){
                return "declaration";
            }
            else{
                return "placement";
            }
         }
         return "Null";

    }

}
