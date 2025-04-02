package ex5.main;

import ex5.input.FileRead;
import ex5.validation.CodeParser;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

/**
 * The Sjavac class is the main entry point for the program. It reads a
 * source file, parses its content, and validates the code.
 */
public class Sjavac {

    /**
     * The main method that executes the program.
     *
     * @param args an array of command-line arguments. The first argument should be the name
     *            of the source file to read.
     */
    public static void main (String[] args){

        if (args.length!=1){
            System.err.println(2);
            return;
        }

        String sourceFileName = args[0];
        List<String> lines;
        FileRead fileRead = new FileRead(sourceFileName);
        try{
            lines = fileRead.getFileLines();
        }
        catch (IOException e){
            e.printStackTrace();
            System.out.println(2);
            return;
        }
        CodeParser codeParser = new CodeParser(new ArrayList<>(lines));

        try{
            codeParser.parse();
        }
        catch (Exception e){
            e.printStackTrace();
            System.out.println(1);
            return;
        }
        System.out.println(0);
    }
}
