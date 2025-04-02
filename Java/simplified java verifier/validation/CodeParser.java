package ex5.validation;

import ex5.utils.RegexUtils;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;
/**
 * The CodeParser class is responsible for parsing and validating the code.
 * It processes each line of code, identifies its type, and performs the necessary validation.
 */
public class CodeParser {
    private boolean inMethod = false;
    private int inBlock = 0;
    private ArrayList<String> lines;
    private VariableValidator variableValidator;
    private ArrayList<MethodValidator> methods;

    /**
     * A map of global variables and their types.
     */
    public static Map<String, VarType> globalVariables = new HashMap<>();

    /**
     * A map of final global variables and their types.
     */
    public static Map<String, VarType> finalGlobalVariables = new HashMap<>();

    /**
     * A list of uninitialized global variables.
     */
    public static ArrayList<String> uninitializedGlobalVariables = new ArrayList<>();

    /**
     * A map of global methods and their parameter types.
     */
    public static Map<String,ArrayList<VarType>> globalMethods = new HashMap<>();//checking method callings

    /**
     * Constructs a CodeParser with the given lines of code.
     *
     * @param lines the lines of code to parse
     */
    public CodeParser(ArrayList<String> lines) {
        this.lines = lines;
        variableValidator = new VariableValidator();
        methods = new ArrayList<>();

    }

    /**
     * Parses and validates the code.
     *
     * @throws InvalidNameException if a variable or method name is invalid
     * @throws InvalidTypeException if a variable type is invalid
     * @throws InvalidSyntaxException if the syntax is invalid
     * @throws InvalidLogicException if there is a logical error
     */
    public void parse() throws InvalidNameException, InvalidTypeException, InvalidSyntaxException,
            InvalidLogicException {
        ArrayList<String> curMethodLines = new ArrayList<>();
        String curMethodName = "";
        Map<String, Map<String, VarType>> curMethodParameters = new HashMap<>();

        for (String line : lines) {
            if(RegexUtils.isComment(line)) {
                continue;
            }
            if(line.stripTrailing().endsWith(";")){
                if(inMethod){
                    curMethodLines.add(line);
                    continue;
                }

                else {
                    String actionType = RegexUtils.getActionType(line);
                    if(actionType == null){
                        throw new InvalidSyntaxException();
                    }
                    switch(actionType){
                        case "declaration":
                            try{
                                ArrayList<ArrayList<String>> decReturn =
                                        variableValidator.validateDeclaration(line);
                                checkDec(decReturn);
                                insertToVarList(decReturn.get(0), decReturn.get(1));
                            }catch (InvalidNameException| InvalidTypeException| InvalidSyntaxException e){
                                throw e;
                            }
                            break;
                        case "placement":
                            try{
                                Map<String,String> placReturn = variableValidator.validatePlacement(line);
                                checkPlacScope(placReturn);
                                removeFromUninitialized(placReturn);
                            } catch ( InvalidTypeException| InvalidNameException
                            e){
                                throw e;
                            }
                    }
                }
            }
            else if(line.stripTrailing().endsWith("{")){
                if(inMethod){
                    curMethodLines.add(line);
                    inBlock += 1;
                }
                else if (RegexUtils.getActionType(line).equals("methodDeclaration")) {
                    curMethodName = RegexUtils.getMethodName(line);
                    if(curMethodName == null){
                        throw new InvalidSyntaxException();
                    }
                    if(globalMethods.containsKey(curMethodName)){
                        throw new InvalidLogicException();
                    }
                    curMethodParameters = RegexUtils.getMethodParameters(line);
                    if(curMethodParameters == null){
                        throw new InvalidSyntaxException();
                    }
                    ArrayList<VarType> curMethodParameterTypes = new ArrayList<>();
                    for (Map<String, VarType> map : curMethodParameters.values()) {
                        for (VarType varType : map.values()) {
                            curMethodParameterTypes.add(varType);
                        }
                    }
                    globalMethods.put(curMethodName, curMethodParameterTypes);
                    inMethod = true;

                }
                else {
                    throw new InvalidSyntaxException();
                }
                continue;
            }
            else if(line.stripTrailing().endsWith("}")){
                if (inBlock > 0){
                    curMethodLines.add(line);
                    inBlock--;
                }
                else if(inMethod){
                    try {
                        MethodValidator method = new MethodValidator(curMethodName,
                                curMethodParameters,
                                curMethodLines, variableValidator);
                        methods.add(method);
                        curMethodParameters.clear();
                        curMethodName = "";
                        inMethod = false;
                        curMethodLines = new ArrayList<>();
                    } catch (Exception e) {
                        throw new RuntimeException(e);
                    }
                }
                else {
                    throw new InvalidSyntaxException();
                }
            }
            // here we need to handle any other case which means to send an exception and do 2
            else{
                throw new InvalidSyntaxException();
            }


        }

        for (MethodValidator method : methods) {
            try{
                method.methodValidate();
            }
            catch( InvalidNameException| InvalidSyntaxException| InvalidTypeException|
                   InvalidLogicException e){
                throw e;
            }
        }
    }

    /**
     * Removes variables from the uninitialized list after they have been initialized.
     *
     * @param placReturn the map of variable names to their values
     */
    private void removeFromUninitialized(Map<String, String> placReturn) {
        for(String var : placReturn.keySet()){
            if(CodeParser.uninitializedGlobalVariables.contains(var)){
                CodeParser.uninitializedGlobalVariables.remove(var);
            }
        }

    }

    /**
     * Checks the scope of variables used in a variable placement.
     *
     * @param placReturn the map of variable names to their values
     * @throws InvalidTypeException if a variable type is invalid
     * @throws InvalidLogicException if there is a logical error
     */
    private void checkPlacScope(Map<String, String> placReturn) throws  InvalidTypeException,
            InvalidLogicException {
        boolean isFinal = false;
        for(String var: placReturn.keySet()){
            try {
                isFinal = checkForSpeVar(var, getType(placReturn.get(var)), "plac");
            } catch ( InvalidTypeException| InvalidLogicException e){
                throw e;

            }
            if(isFinal){
                throw new InvalidLogicException();
            }
        }
    }

    /**
     * Retrieves the type of a variable.
     *
     * @param var the variable name
     * @return the variable type
     * @throws InvalidTypeException if the variable type cannot be determined
     */
    private VarType getType(String var) throws InvalidTypeException {
        if(VarType.fromString(var) != null){
            return VarType.fromString(var);
        }
        if(globalVariables.containsKey(var)){
            return globalVariables.get(var);
        }
        if(finalGlobalVariables.containsKey(var)){
            return finalGlobalVariables.get(var);
        }
        throw new InvalidTypeException();
    }

    /**
     * Inserts variables into the global variable list.
     *
     * @param vars the list of variable names
     * @param strings the list of variable types
     */
    private void insertToVarList(ArrayList<String> vars, ArrayList<String> strings) {
        VarType type = VarType.fromString(vars.get(1));
        switch (vars.get(0)){
            case "NF":
                for (int i = 2; i < vars.size(); i++){
                    globalVariables.put(vars.get(i), type);
                }
                break;
            case "F":
                for (int i = 2; i < vars.size(); i++){
                    finalGlobalVariables.put(vars.get(i), type);
                }

        }
        for (int i = 2; i < vars.size(); i++){
            if(strings.get(i-2).equals("null")){
                uninitializedGlobalVariables.add(vars.get(i));
            }
        }
    }

    /**
     * Checks the scope of variables used in a variable declaration.
     *
     * @param decReturn the list of variable names and their types
     * @throws InvalidLogicException if there is a logical error
     * @throws InvalidTypeException if a variable type is invalid
     */
    private void checkDec(ArrayList<ArrayList<String>> decReturn) throws
            InvalidLogicException,
            InvalidTypeException {
        VarType typeToCompare = VarType.fromString(decReturn.get(0).get(1));

        if(!decReturn.get(1).isEmpty()){
            for (String var : decReturn.get(1)) {
                if(var.equals("null") || VarType.fromString(var) != null){
                    continue;
                }
                try {
                    checkItsBeenUninitialized(var);
                    checkForSpeVar(var, typeToCompare, "dec");
                } catch ( InvalidTypeException | InvalidLogicException e) {
                    throw e;
                }
            }
        }

        ArrayList<String> varList = decReturn.get(0);
        for(int i = 2; i < varList.size(); i++){
            if(globalVariables.containsKey(varList.get(i))){
                throw new InvalidLogicException();
            }
            if(finalGlobalVariables.containsKey(varList.get(i))){
                throw new InvalidLogicException();
            }
        }
    }

    /**
     * Checks if a variable has been uninitialized.
     *
     * @param var the variable name to check
     * @throws InvalidLogicException if the variable has been uninitialized
     */
    private void checkItsBeenUninitialized(String var) throws
            InvalidLogicException {
        if(uninitializedGlobalVariables.contains(var)){
            throw new InvalidLogicException();
        }
    }

    /**
     * Checks for a specific variable in the current scope.
     *
     * @param var the variable name to check
     * @param typeToCompare the variable type to compare
     * @param action the action type
     * @return true if the variable is final, false otherwise
     * @throws InvalidTypeException if a variable type is invalid
     * @throws InvalidLogicException if there is a logical error
     */
    private boolean checkForSpeVar(String var, VarType typeToCompare, String action)
            throws InvalidTypeException, InvalidLogicException {
        boolean isFinal = false;
        boolean sucForCurVar = false;
        if(globalVariables.containsKey(var)){
            sucForCurVar = true;
            if(!compareTypesByAction(globalVariables.get(var), typeToCompare, action)){
                throw new InvalidTypeException();
            }
        }
        if(finalGlobalVariables.containsKey(var)){
            isFinal = true;
            sucForCurVar = true;
            if(!compareTypesByAction(finalGlobalVariables.get(var), typeToCompare, action)){
                throw new InvalidTypeException();
            }
        }
        if(!sucForCurVar){
            throw new InvalidLogicException();
        }
        return isFinal;
    }

    /**
     * Compares variable types based on the action type.
     *
     * @param varType the first variable type
     * @param typeToCompare the second variable type
     * @param action the action type
     * @return true if the types are compatible, false otherwise
     */
    private boolean compareTypesByAction(VarType varType, VarType typeToCompare, String action) {
        switch (action) {
            case "dec":
                return compareTypes(typeToCompare,varType);
            case "plac":
                return compareTypes(varType,typeToCompare);
            default:
                return false;
        }
    }

    /**
     * Compares two variable types for compatibility.
     *
     * @param type1 the first variable type
     * @param type2 the second variable type
     * @return true if the types are compatible, false otherwise
     */
    private boolean compareTypes(VarType type1, VarType type2){
        if(type1.equals(VarType.BOOLEAN)){
            return type2.equals(VarType.BOOLEAN) || type2.equals(VarType.DOUBLE) ||
                    type2.equals(VarType.INT);
        }
        else if(type1.equals(VarType.DOUBLE)){
            return type2.equals(VarType.INT) || type2.equals(VarType.DOUBLE);
        }
        return type1.equals(type2);
    }
}
