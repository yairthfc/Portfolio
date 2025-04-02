package ex5.validation;

import ex5.utils.RegexUtils;

import javax.sound.sampled.Line;
import java.io.IOException;
import java.util.*;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
/**
 * The VariableValidator class provides methods to validate various
 * types of variable declarations,
 * placements, method calls, and block structures in Java code.
 */
public class VariableValidator {


    /**
     * Validates a variable declaration line.
     *
     * @param line the line of code to validate
     * @return true if the variable declaration is valid, false otherwise
     * @throws InvalidTypeException if a variable type is invalid
     * @throws InvalidNameException if a variable name is invalid
     */
    public Map<String,String> validatePlacement(String line) throws
            InvalidTypeException, InvalidNameException ,InvalidSyntaxException {
        Map<String,String> result = new HashMap<>();
        line= line.replace(";", "");
        String[] parts = line.split(",");
        Pattern pattern = Pattern.compile("\\s*(\\w+)\\s*(=\\s*(\\S+))?");
        String lastValue = null;

        for (String part : parts) {
            Matcher matcher = pattern.matcher(part.trim());
            if (matcher.matches()) {
                String variable = matcher.group(1);
                    lastValue = matcher.group(3);
                result.put(variable, lastValue);
            }
            else{
                throw new InvalidSyntaxException();
            }
        }

        for (int i = parts.length - 1; i >= 0; i--) {
            Matcher matcher = pattern.matcher(parts[i].trim());
            if (matcher.matches()) {
                String variable = matcher.group(1);
                if (result.get(variable) == null) {
                    result.put(variable, lastValue);
                } else {
                    lastValue = result.get(variable);
                }
            }
        }
        result = checkPlacementScope(result);
        return result;
    }

    /**
     * Checks the scope of variable placements.
     *
     * @param placementReturn the map of variable names to their values
     * @return a map of variable names to their types
     * @throws InvalidNameException if a variable name is invalid
     * @throws InvalidTypeException if a variable type is invalid
     */
    private Map<String,String> checkPlacementScope(Map<String,String> placementReturn)
            throws InvalidNameException,
            InvalidTypeException {
        Map<String,String> result = new HashMap<>();
        for (Map.Entry<String, String> entry : placementReturn.entrySet()) {
            String key = entry.getKey();
            String value = entry.getValue();
            if (RegexUtils.isValidVariableName(key)) {
                if (value == null) {
                    result.put(key, "null");
                }
                else if(RegexUtils.isInteger(value)){
                    result.put(key, "int");
                }
                else if(RegexUtils.isDouble(value)){
                    result.put(key, "double");
                }
                else if(RegexUtils.isChar(value)){
                    result.put(key,"char");
                }
                else if(RegexUtils.isString(value)){
                    result.put(key, "String");
                }
                else if(RegexUtils.isBoolean(value)||RegexUtils.isInteger(value)
                        ||RegexUtils.isDouble(value)){
                    result.put(key, "boolean");
                }
                else if(RegexUtils.isValidVariableName(value)){
                    result.put(key, value);
                }
                else {
                    throw new InvalidTypeException();
                }
            }
            else {
                throw new InvalidNameException();
            }
        }
        return result;
    }

    /**
     * Validates a variable declaration line.
     *
     * @param line the line of code to validate
     * @return a list of lists containing variable names and their types
     * @throws InvalidNameException if a variable name is invalid
     * @throws InvalidTypeException if a variable type is invalid
     * @throws InvalidSyntaxException if the syntax is invalid
     */
    public ArrayList<ArrayList<String>> validateDeclaration(String line)
            throws InvalidNameException,
            InvalidTypeException, InvalidSyntaxException {
        ArrayList<ArrayList<String>> result = new ArrayList<>();
        boolean isFinal = false;
        if (line.startsWith("final")) {
            isFinal = true;
            line = line.replace("final", "").trim();
        }
        // Extract the type
        String type = line.split("\\s+")[0];
        String newLine=line.replaceFirst(type + "\\s+", "").
                replace(";", "");
        Map<String,String> decReturn = null;
        try {
            decReturn = validatePlacement(newLine);
        } catch (InvalidTypeException e) {
            throw e;
        } catch (InvalidNameException e) {
            throw e;
        }

        try {
            result = checkDecScope(decReturn, type);
        } catch (InvalidNameException e) {
            throw e;
        } catch (InvalidSyntaxException e) {
            throw e;
        }
        result.get(0).add(0, type);
        if (isFinal) {
            if (result.get(1).contains("null")){
                throw new InvalidSyntaxException();
            }
            result.get(0).add(0, "F");
        } else {
            result.get(0).add(0, "NF");
        }

        return result;
    }

    /**
     * Checks the scope of variable declarations.
     *
     * @param decReturn the map of variable names to their values
     * @param caseType the type of the variables
     * @return a list of lists containing variable names and their types
     * @throws InvalidNameException if a variable name is invalid
     * @throws InvalidSyntaxException if the syntax is invalid
     */
    private ArrayList<ArrayList<String>> checkDecScope(Map<String,String> decReturn , String caseType)
            throws InvalidNameException, InvalidSyntaxException {
        ArrayList<ArrayList<String>> result = new ArrayList<>();
        ArrayList<String> variables = new ArrayList<>();
        ArrayList<String> values = new ArrayList<>();
            switch (caseType) {
                case "int":
                    for (Map.Entry<String, String> entry : decReturn.entrySet()) {
                        String key = entry.getKey();
                        String value = entry.getValue();
                        variables.add(key);
                        if (RegexUtils.isInteger(value)) {
                            values.add("int");
                        } else if (RegexUtils.isValidVariableName(value)) {
                            values.add(value);
                        } else if (value.isEmpty()) {
                            values.add("null");
                        } else {
                            throw new InvalidNameException();
                        }
                    }
                    break;
                case "double":
                    for (Map.Entry<String, String> entry : decReturn.entrySet()) {
                        String key = entry.getKey();
                        String value = entry.getValue();
                        variables.add(key);
                    if (RegexUtils.isDouble(value)) {
                        values.add("double");
                    } else if (RegexUtils.isValidVariableName(value)) {
                        values.add(value);

                    } else if (value.isEmpty()) {
                        values.add("null");
                    } else {
                        throw new InvalidNameException();
                    }
                    }

                    break;
                case "char":
                    for (Map.Entry<String, String> entry : decReturn.entrySet()) {
                        String key = entry.getKey();
                        String value = entry.getValue();
                        variables.add(key);
                        if (RegexUtils.isChar(value)) {
                            values.add("char");
                        } else if (RegexUtils.isValidVariableName(value)) {
                            values.add(value);

                        } else if (value.isEmpty()) {
                            values.add("null");
                        } else {
                            throw new InvalidNameException();
                        }
                    }
                    break;
                case "String":
                    for (Map.Entry<String, String> entry : decReturn.entrySet()) {
                        String key = entry.getKey();
                        String value = entry.getValue();
                        variables.add(key);
                        if (RegexUtils.isString(value)) {
                            values.add("String");
                        } else if (RegexUtils.isValidVariableName(value)) {
                            values.add(value);

                        } else if (value.isEmpty()) {
                            values.add("null");
                        } else {
                            throw new InvalidNameException();
                        }
                    }

                    break;
                case "boolean":
                    for (Map.Entry<String, String> entry : decReturn.entrySet()) {
                        String key = entry.getKey();
                        String value = entry.getValue();
                        variables.add(key);
                        if (RegexUtils.isBoolean(value) || RegexUtils.isInteger(value)
                                || RegexUtils.isDouble(value)) {
                            values.add("boolean");
                        } else if (RegexUtils.isValidVariableName(value)) {
                            values.add(value);

                        } else if (value.isEmpty()) {
                            values.add("null");
                        } else {
                            throw new InvalidNameException();
                        }
                    }
            break;
            default:
                throw new InvalidSyntaxException();
        }
            result.add(variables);
            result.add(values);
            return result;
        }

    /**
     * Validates a method call line.
     *
     * @param line the line of code to validate
     * @return a list of method names and their parameter types
     * @throws InvalidNameException if a method name is invalid
     * @throws InvalidSyntaxException if the syntax is invalid
     */
    public ArrayList<String> validateCall(String line)
            throws InvalidNameException,  InvalidSyntaxException {
        ArrayList<String> result = new ArrayList<>();
        line = line.replace(";", "");
        String regex = "^\\s*(\\w+)\\s*\\((.*)\\)\\s*$";

        Pattern pattern = Pattern.compile(regex);
        Matcher matcher = pattern.matcher(line);
        if (matcher.matches()){
            String methodName = matcher.group(1);
            if (!RegexUtils.isValidMethodName(methodName)){
                throw new InvalidNameException();
            }
            result.add(methodName);
            String[] params = matcher.group(2).split("\\s*,\\s*");
            for (String param : params) {
                if (RegexUtils.isInteger(param)) {
                    result.add("int");
                } else if (RegexUtils.isDouble(param)) {
                    result.add("double");
                } else if (RegexUtils.isChar(param)) {
                    result.add("char");
                } else if (RegexUtils.isString(param)) {
                    result.add("String");
                } else if (RegexUtils.isBoolean(param)) {
                    result.add("boolean");
                } else if (RegexUtils.isValidVariableName(param)) {
                    result.add(param);
                } else if (param.equals("")) {
                    continue;

                } else {
                    throw new InvalidNameException();
                }
            }
        }
        return result;
    }

    /**
     * Validates a block structure line (e.g., if or while).
     *
     * @param line the line of code to validate
     * @return a list of variable names used in the block condition
     * @throws InvalidNameException if a variable name is invalid
     */
    public ArrayList<String> validateBlock(String line) throws InvalidNameException {
        ArrayList<String> result = new ArrayList<>();
        line = line.replace("{", "").trim();
        Pattern pattern = Pattern.compile("^(while|if)\\s*\\((.*)\\)$");
        Matcher matcher = pattern.matcher(line);
        if (matcher.matches()) {
            String condition = matcher.group(2);

            String cleanedCondition = condition.replaceAll("\\|\\|", "").
                    replaceAll("&&", "");
            //System.out.println("Cleaned Condition: " + cleanedCondition);
            String[] conditions = cleanedCondition.trim().split("\\s+");
            //System.out.println("Conditions Array: " + Arrays.toString(conditions));
            for (String var : conditions) {
                //System.out.println(Arrays.toString(conditions));
                if (RegexUtils.isBoolean(var) || RegexUtils.isInteger(var)
                        || RegexUtils.isDouble(var)) {
                    continue;
                } else if (RegexUtils.isValidVariableName(var)) {
                    result.add(var);
                } else {

                    throw new InvalidNameException();
                }
            }
        }
        return result;

    }

}

