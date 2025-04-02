package ex5.input;
import ex5.utils.RegexUtils;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;

/**
 * The FileRead class provides methods to read lines from a file and
 * return them as an ArrayList of strings.
 */
public class FileRead{
    private String fileName;
    private String[] lines;

    /**
     * Constructs a FileRead object with the specified file name.
     *
     * @param fileName the name of the file to read
     */
    public FileRead(String fileName) {
        this.fileName = fileName;
    }

    /**
     * Reads the lines from the file and returns them as an ArrayList of strings.
     *
     * @return an ArrayList of strings containing the lines from the file
     * @throws IOException if an I/O error occurs
     */
    public ArrayList<String> getFileLines() throws IOException {
        String line;
        ArrayList<String> lines = new ArrayList<>();
        try(FileReader fileReader = new FileReader(fileName);
            BufferedReader bufferedReader = new BufferedReader(fileReader);)
        {
            while ((line = bufferedReader.readLine()) != null) {
                if(!RegexUtils.isEmpty(line)){
                    lines.add(line);
                }
            }
        }catch (IOException e) {
            throw e;
        }
        return lines;
    }
}
