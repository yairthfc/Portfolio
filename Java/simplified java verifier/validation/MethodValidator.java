package ex5.validation;

import ex5.utils.RegexUtils;

import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;
/**
 * The MethodValidator class provides methods to validate the structure and content of a
 * method in Java code.
 */
public class MethodValidator {
    private final VariableValidator variableValidator;
    private String methodName;
    private ArrayList<String> methodLines;
    private Map<Integer,Map<String,VarType>> scopedVariables;
    private Map<Integer,Map<String,VarType>> finalScopedVariables;
    private Map<Integer, ArrayList<String>> uninitializedScopedVariables;
    private ArrayList<String> globalUninitializedTemporary;
    private int curScope = 0;

    /**
     * Constructs a MethodValidator with the specified method name, parameters, method lines,
     * and variable validator.
     *
     * @param methodName the name of the method to validate
     * @param params the parameters of the method
     * @param curMethodLines the lines of code in the method
     * @param validator the VariableValidator to use for validation
     */
    public MethodValidator(String methodName, Map<String, Map<String, VarType>> params, ArrayList<String>
            curMethodLines, VariableValidator validator) {
        this.methodName = methodName;
        this.methodLines = curMethodLines;
        scopedVariables = new HashMap<>();
        scopedVariables.put(0,params.get("NF"));
        finalScopedVariables = new HashMap<>();
        finalScopedVariables.put(0,params.get("F"));
        this.variableValidator = validator;
        uninitializedScopedVariables = new HashMap<>();
        uninitializedScopedVariables.put(0,new ArrayList<>());
        globalUninitializedTemporary = new ArrayList<>();
    }

    /**
     * Validates the method by checking the structure and content of the method lines.
     *
     * @throws InvalidNameException if a variable or method name is invalid
     * @throws InvalidSyntaxException if the syntax is invalid
     * @throws InvalidTypeException if a variable type is invalid
     * @throws InvalidLogicException if there is a logical error
     */
    public void methodValidate() throws InvalidNameException, InvalidSyntaxException,
            InvalidTypeException, InvalidLogicException {
        if(!RegexUtils.getActionType(methodLines.getLast()).equals("return")){
            throw new InvalidSyntaxException();
        }
        for (String line : methodLines) {
            String actionType = RegexUtils.getActionType(line);
            if(actionType == null){
                throw new InvalidSyntaxException();
            }
            switch(actionType){
                case "return":
                    if(!RegexUtils.isReturnStatement(line)){
                        throw new InvalidSyntaxException();
                    }
                    break;
                case "declaration":
                    try{
                        ArrayList<ArrayList<String>> decReturn = variableValidator.validateDeclaration(line);
                        checkDecScope(decReturn);
                        insertToVarList(decReturn.get(0), decReturn.get(1));
                    } catch (InvalidTypeException | InvalidNameException | InvalidSyntaxException |
                             InvalidLogicException e){
                        throw e;
                    }
                    break;
                case "placement":
                    try{
                        Map<String,String> placReturn = variableValidator.validatePlacement(line);
                        checkPlacScope(placReturn);
                        removeFromUninitialized(placReturn);
                    }catch (InvalidTypeException | InvalidNameException | InvalidLogicException e){
                        throw e;
                    }
                    break;
                case "method":
                    try {
                        ArrayList<String> callReturn = variableValidator.validateCall(line);
                        checkCallScope(callReturn);
                    } catch (InvalidNameException| InvalidSyntaxException | InvalidLogicException |
                             InvalidTypeException e) {
                        throw e;
                    }
                    break;
                case "blockStart":
                    try {
                        ArrayList<String> blockReturn = variableValidator.validateBlock(line);
                        checkBlockScope(blockReturn);
                    } catch (InvalidNameException | InvalidTypeException | InvalidLogicException  e) {
                        throw e;
                    }
                    curScope++;
                    scopedVariables.put(curScope,new HashMap<>());
                    finalScopedVariables.put(curScope,new HashMap<>());
                    uninitializedScopedVariables.put(curScope,new ArrayList<>());
                    break;
                case "blockEnd":
                    uninitializedScopedVariables.remove(curScope);
                    scopedVariables.remove(curScope);
                    finalScopedVariables.remove(curScope);
                    curScope--;
                    break;
            }
        }
        returnToGlobalUninitialized();
    }

    /**
     * Returns uninitialized variables to the global uninitialized list.
     */
    private void returnToGlobalUninitialized() {
        for(String var : globalUninitializedTemporary){
            CodeParser.uninitializedGlobalVariables.add(var);
        }
    }

    /**
     * Removes variables from the uninitialized list after they have been initialized.
     *
     * @param placReturn the map of variable names to their values
     */
    private void removeFromUninitialized(Map<String, String> placReturn) {
        for(String var : placReturn.keySet()){
            for (int i = curScope ; i >= 0 ; i--) {
                if(uninitializedScopedVariables.get(i).contains(var)){
                    uninitializedScopedVariables.get(i).remove(var);
                }
            }
            if(CodeParser.uninitializedGlobalVariables.contains(var)){
                CodeParser.uninitializedGlobalVariables.remove(var);
                globalUninitializedTemporary.add(var);
            }
        }

    }

    /**
     * Checks the scope of variables used in a block structure.
     *
     * @param blockReturn the list of variable names used in the block condition
     * @throws InvalidTypeException if a variable type is invalid
     * @throws InvalidLogicException if there is a logical error
     */
    private void checkBlockScope(ArrayList<String> blockReturn) throws InvalidTypeException ,
            InvalidLogicException {
        for (String var : blockReturn) {
            try {
                checkForSpeVar(var, VarType.BOOLEAN, "block");
            } catch ( InvalidTypeException | InvalidLogicException e) {
                throw e;
            }
        }
    }

    /**
     * Checks the scope of variables used in a method call.
     *
     * @param callReturn the list of method names and their parameter types
     * @throws InvalidLogicException if there is a logical error
     * @throws InvalidTypeException if a variable type is invalid
     */
    private void checkCallScope(ArrayList<String> callReturn) throws InvalidLogicException,
            InvalidTypeException {
        ArrayList<VarType> params;
        try {
            params = methodExistenceAndParams(callReturn.get(0));
        } catch (InvalidLogicException e){
            throw e;
        }
        callReturn.remove(0);
        for (int i = 0; i < callReturn.size(); i++) {
            String var = callReturn.get(i);
            if(VarType.fromString(var) != null){
                VarType varType = VarType.fromString(var);
                if(!varType.equals(params.get(i))){
                    throw new InvalidTypeException();
                }
            }
            else{
                try{
                    checkForSpeVar(var, params.get(i), "call");
                }catch (InvalidLogicException | InvalidTypeException e){
                    throw e;
                }
            }
        }
    }

    /**
     * Checks if a method exists and retrieves its parameter types.
     *
     * @param methodName the name of the method to check
     * @return a list of parameter types
     * @throws InvalidLogicException if the method does not exist
     */
    private ArrayList<VarType> methodExistenceAndParams(String methodName) throws
            InvalidLogicException {
        if(!CodeParser.globalMethods.containsKey(methodName)){
            throw new InvalidLogicException();
        }
        return CodeParser.globalMethods.get(methodName);
    }

    /**
     * Checks the scope of variables used in a placement statement.
     *
     * @param placReturn the map of variable names to their values
     * @throws InvalidLogicException if there is a logical error
     * @throws InvalidTypeException if a variable type is invalid
     */
    private void checkPlacScope(Map<String, String> placReturn) throws
            InvalidLogicException ,
            InvalidTypeException {
        boolean isFinal = false;
        for(String var: placReturn.keySet()){
            try {
                isFinal = checkForSpeVar(var, getType(placReturn.get(var)), "plac");
            } catch (InvalidTypeException | InvalidLogicException e){
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
     * @throws InvalidLogicException if the variable type cannot be determined
     */
    private VarType getType(String var) throws InvalidLogicException  {
        if(VarType.fromString(var) != null){
            return VarType.fromString(var);
        }

        for(int i = curScope; i >= 0; i--){
            if(scopedVariables.get(i).containsKey(var)){
                return scopedVariables.get(i).get(var);
            }
            if(finalScopedVariables.get(i).containsKey(var)){
                return finalScopedVariables.get(i).get(var);
            }
        }
        if(CodeParser.globalVariables.containsKey(var)){
            return CodeParser.globalVariables.get(var);
        }
        if(CodeParser.finalGlobalVariables.containsKey(var)){
            return CodeParser.finalGlobalVariables.get(var);
        }
        throw new InvalidLogicException();
    }

    /**
     * Inserts variables into the scoped variable list.
     *
     * @param vars the list of variable names
     * @param strings the list of variable types
     */
    private void insertToVarList(ArrayList<String> vars,
                                 ArrayList<String> strings) {
        VarType type = VarType.fromString(vars.get(1));
        switch (vars.get(0)){
            case "NF":
                for (int i = 2; i < vars.size(); i++){
                    scopedVariables.get(curScope).put(vars.get(i), type);
                }
                break;
            case "F":
                for (int i = 2; i < vars.size(); i++){
                    finalScopedVariables.get(curScope).put(vars.get(i), type);
                }

        }
        for (int i = 2; i < vars.size(); i++){
            if(strings.get(i-2).equals(null)){
                uninitializedScopedVariables.get(curScope).add(vars.get(i));
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
    private void checkDecScope(ArrayList<ArrayList<String>> decReturn)
            throws InvalidLogicException,
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
                } catch (InvalidLogicException|InvalidTypeException e) {
                    throw e;
                }
            }
        }

        ArrayList<String> varList = decReturn.get(0);
        Map<String, VarType> scopeVariables = scopedVariables.get(curScope);
        Map<String, VarType> finalScopeVariables = finalScopedVariables.get(curScope);
        for(int i = 2; i < varList.size(); i++){
            if(scopeVariables.containsKey(varList.get(i))){
                throw new InvalidLogicException();
            }
            if(finalScopeVariables.containsKey(varList.get(i))){
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
    private void checkItsBeenUninitialized(String var)
            throws InvalidLogicException {
        for(int i = curScope; i >= 0; i--){
            if(uninitializedScopedVariables.get(i).contains(var)){
                throw new InvalidLogicException();
            }
        }
        if(CodeParser.uninitializedGlobalVariables.contains(var)){
            throw new InvalidLogicException();
        }
    }

    /**
     * Compares variable types based on the action type.
     *
     * @param type1 the first variable type
     * @param type2 the second variable type
     * @param action the action type
     * @return true if the types are compatible, false otherwise
     */
    private boolean compareTypesByAction(VarType type1,
                                         VarType type2, String action){
        switch(action){
            case "dec":
                return compareTypes(type2,type1);
            case "plac":
                return compareTypes(type1,type2);
            case "call":
                return compareTypes(type2,type1);
            case "blockStart":
                return compareTypes(type2,type1);
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
            return type2.equals(VarType.BOOLEAN) || type2.equals(VarType.DOUBLE)
                    || type2.equals(VarType.INT);
        }
        else if(type1.equals(VarType.DOUBLE)){
            return type2.equals(VarType.INT) || type2.equals(VarType.DOUBLE);
        }
        return type1.equals(type2);
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
            throws InvalidTypeException,
            InvalidLogicException {
        boolean continueToEnd = false;
        boolean isFinal = false;
        boolean sucForCurVar = false;
        for(int i = curScope; i >= 0; i--){
            if(scopedVariables.get(i).containsKey(var)){
                sucForCurVar = true;
                if(!compareTypesByAction(scopedVariables.get(i).get(var), typeToCompare, action)){
                    throw new InvalidTypeException();
                }
                else{
                    continueToEnd = true;
                    break;
                }
            }
            if(finalScopedVariables.get(i).containsKey(var)){
                isFinal = true;
                sucForCurVar = true;
                if(!compareTypesByAction(finalScopedVariables.get(i).get(var), typeToCompare, action)){
                    throw new InvalidTypeException();
                }
                else{
                    continueToEnd = true;
                    break;
                }
            }
        }
        if(CodeParser.globalVariables.containsKey(var) && !continueToEnd){
            sucForCurVar = true;
            if(!compareTypesByAction(CodeParser.globalVariables.get(var), typeToCompare, action)){
                throw new InvalidTypeException();
            }
        }
        if(CodeParser.finalGlobalVariables.containsKey(var) && !continueToEnd){
            isFinal = true;
            sucForCurVar = true;
            if(!compareTypesByAction(CodeParser.finalGlobalVariables.get(var),
                    typeToCompare, action)){
                throw new InvalidTypeException();
            }
        }
        if(!sucForCurVar){
            throw new InvalidLogicException();
        }
        return isFinal;
    }


}
