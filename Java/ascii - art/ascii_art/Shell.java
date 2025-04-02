package ascii_art;
import ascii_art.KeyboardInput;
import ascii_output.AsciiOutput;
import ascii_output.ConsoleAsciiOutput;
import ascii_output.HtmlAsciiOutput;
import exceptions.InsufficientCharArrayException;
import image.Image;
import image.ImageEditor;
import image_char_matching.SubImgCharMatcher;


import javax.naming.InsufficientResourcesException;
import java.io.IOException;
import java.util.List;
import java.util.TreeMap;

/**
 * main shell class, runs the program
 */
public class Shell {
    private static final String EXIT_COMMAND = "exit";//exit command
    private ImageEditor imageEditor;//instance of image editor
    private SubImgCharMatcher subImgCharMatcher;//instance of sub image character matcher
    private AsciiOutput asciiOutput;  //instance of ascii output

    /**
     * Constructs a new Shell with the specified default character set, resolution, and image.
     *
     * @param defaultCharSet the default character set.
     * @param resolution the resolution.
     * @param image the image.
     */
    public Shell(char[] defaultCharSet, int resolution, Image image) {
        this.imageEditor = new ImageEditor(image,resolution);
        this.subImgCharMatcher = new SubImgCharMatcher(defaultCharSet);
        this.asciiOutput = new ConsoleAsciiOutput();
    }

    /**
     * Runs the shell with the specified image name.
     *
     * @param imageName the image name.
     * @throws IllegalArgumentException if the input command is invalid.
     */
    public void run(String imageName) throws IllegalArgumentException{
        String line = "s";
        while (!line.equals(EXIT_COMMAND)) {
            System.out.print(">>> ");
            line = KeyboardInput.readLine();
            try {
                handleCommand(line); // Handle the user input
            } catch (IllegalArgumentException e) {
                // Catch invalid input exceptions and display an error message
                System.out.println("Did not execute due to incorrect command.");
            }
//            System.out.print(">>> ");
//            line = KeyboardInput.readLine();
        }
    }

    /**
     * Handles the user input command.
     *
     * @param line the input command.
     * @throws IllegalArgumentException if the command is invalid.
     */
    private void handleCommand(String line) throws IllegalArgumentException {
        String[] words = line.split(" ");

        switch (words[0]) {
            case "chars":
                char[] curCharSet = subImgCharMatcher.returnCharset();
                int lenChars = curCharSet.length;
                if(lenChars != 0){
                    for (int i = 0; i < lenChars; i++) {
                        System.out.print(curCharSet[i] + " ");
                    };
                    System.out.println();
                }
                break;
            case "add":
                try {
                    addOrRemove(words);
                }catch (IOException e){
                    System.out.println("Did not add due to incorrect format.");
                }
                    break;
            case "remove":
                try {
                    addOrRemove(words);
                } catch (IOException e) {
                    System.out.println("Did not remove due to incorrect format.");
                }
                break;
            case "res":
                try {
                    resolutionChange(words);
                } catch (IOException e) {
                    System.out.println("Did not change resolution due to incorrect format.");
                } catch (IllegalArgumentException e){
                    System.out.println("Did not change resolution due to exceeding boundaries.");
                }
                break;
            case "round":
                try {
                    roundChange(words);
                } catch (IOException e) {
                    System.out.println("Did not change rounding method due to incorrect format.");
                }
                break;
            case "output":
                try {
                    changeOutput(words);
                } catch (IOException e) {
                    System.out.println("Did not change output method due to incorrect format.");
                }
                // Handle output logic
                break;
            case "asciiArt":
                try {
                    runAsciiAlgorithm();
                } catch (InsufficientCharArrayException e) {
                    System.out.println("Did not execute. Charset is too small.");
                }
                break;
            default:
                // Throw exception for invalid commands
                throw new IllegalArgumentException();
        }
    }

    /**
     * Runs the ASCII art algorithm.
     *
     * @throws InsufficientCharArrayException if the character set is too small.
     */
    private void runAsciiAlgorithm() {
        if(subImgCharMatcher.returnCharset().length < 2){
            throw new InsufficientCharArrayException();
        }
        AsciiArtAlgorithm algorithm = new AsciiArtAlgorithm(this.imageEditor,
                subImgCharMatcher);
        char[][] image = algorithm.run();
        this.asciiOutput.out(image);
    }

    /**
     * Changes the output method.
     *
     * @param words the input command words.
     * @throws IOException if the input format is incorrect.
     */
    private void changeOutput(String[] words) throws IOException {
        String toOutput;
        if(words.length <= 1) {
            throw new IOException();
        }
        toOutput = words[1];
        switch (toOutput) {
            case "html":
                this.asciiOutput = new HtmlAsciiOutput("out11.html"
                        , "Courier new");
                break;
            case "console":
                this.asciiOutput = new ConsoleAsciiOutput();
                break;
            default:
                throw new IOException();
        }


    }

    /**
     * Changes the rounding method.
     *
     * @param words the input command words.
     * @throws IOException if the input format is incorrect.
     */
    private void roundChange(String[] words) throws IOException {
        String toRound;
        if(words.length <= 1) {
            throw new IOException();
        }
        toRound = words[1];
        if(toRound.equals("up") || toRound.equals("down") || toRound.equals("abs")) {
            subImgCharMatcher.setRound(toRound);
        }
        else{
            throw new IOException();
        }
    }

    /**
     * Changes the resolution.
     *
     * @param words the input command words.
     * @throws IOException if the input format is incorrect.
     * @throws IllegalArgumentException if the resolution change exceeds boundaries.
     */
    private void resolutionChange(String[] words) throws IOException {
        String toRes;
        boolean wasChanged = false;
        if(words.length <= 1) {
            throw new IOException();
        }
        toRes = words[1];
        if(toRes.equals("up") || toRes.equals("down")) {
            try {
                imageEditor.changeResolution(toRes);
                wasChanged = true;
            } catch (IllegalArgumentException e) {
                throw new IllegalArgumentException();
            }
        }
        if(wasChanged){
            System.out.printf("Resolution set to %d.\n", imageEditor.returnResolution());
        }
        else{
            throw new IOException();
        }
    }

    /**
     * Adds or removes characters from the character set.
     *
     * @param words the input command words.
     * @throws IOException if the input format is incorrect.
     */
    private void addOrRemove(String[] words) throws IOException {
        String command = words[0];
        String toAdd;
        if(words.length <= 1) {
            throw new IOException();
        }
        toAdd = words[1];
        switch (toAdd) {
            case "all":
                for (int i = 32; i < 127 ; i++) {
                    addOrRemoveAccordingToCommand(command, (char)i);
                }
                break;
            case "space":
                char space = " ".charAt(0);
                addOrRemoveAccordingToCommand(command, space);
                break;
            default:
                if(toAdd.length() == 1){
                    char charToAscii = toAdd.charAt(0);
                    if(charIsInRange(charToAscii)){
                        addOrRemoveAccordingToCommand(command, (char)charToAscii);
                        break;
                    }
                }
                if(toAdd.length() == 3){
                    if(toAdd.charAt(1) == '-' && charIsInRange(toAdd.charAt(0))
                            && charIsInRange(toAdd.charAt(2))) {
                        int asciiTwo = (int) toAdd.charAt(2);
                        int asciiOne = (int) toAdd.charAt(0);
                        if(asciiOne <= asciiTwo) {
                            for (int i = asciiOne; i <= asciiTwo; i++) {
                                addOrRemoveAccordingToCommand(command, (char) i);
                            }
                            break;
                        }
                        else {
                            for (int i = asciiTwo; i <= asciiOne; i++) {
                                addOrRemoveAccordingToCommand(command, (char) i);
                            }
                            break;
                        }
                    }
                }
                throw new IOException();


        }
    }

    /**
     * Adds or removes a character according to the command.
     *
     * @param command the command ("add" or "remove").
     * @param i the character to add or remove.
     */
    private void addOrRemoveAccordingToCommand(String command, char i) {
        switch (command){
            case "add":
                subImgCharMatcher.addChar(i);
                break;
            case "remove":
                subImgCharMatcher.removeChar(i);
                break;
            default:
                break;
        }
    }

    /**
     * Checks if a character is in the valid ASCII range.
     *
     * @param charToAscii the character to check.
     * @return true if the character is in the valid range, false otherwise.
     */
    private boolean charIsInRange(char charToAscii)
    {
        return 32 <= (int) charToAscii && (int) charToAscii <= 126;
    }

    /**
     * The main method to run the shell.
     *
     * @param args the command line arguments.
     */
    public static void main(String[] args) {
        char[] defaultCharSet = new char[]{'0', '1', '2' , '3', '4', '5', '6', '7', '8', '9'};
        Image image;
        try{
            image = new Image(args[0]);
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
        Shell shell = new Shell(defaultCharSet,2,image);
        shell.run(args[0]);
    }
}
