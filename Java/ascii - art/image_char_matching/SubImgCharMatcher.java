package image_char_matching;

import java.util.*;

/**
 * Class to match sub-images to characters based on brightness.
 */
public class SubImgCharMatcher {
    private TreeMap<Double, TreeSet<Character>> charBrightnessMap;//brightness treemap with characters
    private String currentRound = "abs";//current rounding method
    private final int sideInMatrix = 16;//side of the matrix for character brightness
    private double maxBrightness = 0; //max brightness
    private double minBrightness = 255; //min brightness
    private boolean changeHasBeenMade = false; //check if change has been made


    /**
     * Constructs a new SubImgCharMatcher with the specified character set.
     *
     * @param charset the character set.
     */
    public SubImgCharMatcher(char[] charset) {
        this.charBrightnessMap = new TreeMap<>();
        for (char c : charset) {
            addChar(c);
        }
    }

    /**
     * Normalizes the brightness values in the map.
     */
    private void normalizeBrightness() {
        TreeMap<Double, TreeSet<Character>> normalizedMap = new TreeMap<>();
        for (Map.Entry<Double, TreeSet<Character>> entry : charBrightnessMap.entrySet()) {
            double normalizedBrightness = (entry.getKey() - minBrightness) / (maxBrightness - minBrightness);

            normalizedMap.put(normalizedBrightness, entry.getValue());
        }
        charBrightnessMap = normalizedMap;
    }

    /**
     * Returns the brightness of a character.
     *
     * @param c the character.
     * @return the brightness.
     */
    private Double getBrightness(char c) {
        double score = 0f;
        boolean[][] cMatrix = CharConverter.convertToBoolArray(c);
        for (int i = 0; i < sideInMatrix; i++) {
            for (int j = 0; j < sideInMatrix; j++) {
                if (cMatrix[i][j]) {
                    score++;
                }
            }
        }
        if (score > maxBrightness) {
            maxBrightness = score;
        }
        if (score < minBrightness) {
            minBrightness = score;
        }
        return score;
    }

    /**
     * Sets the rounding method.
     *
     * @param round the rounding method.
     */
    public void setRound(String round) {
        this.currentRound = round;
    }

    /**
     * Returns a character based on the brightness and rounding method.
     *
     * @param brightness the brightness value.
     * @return the matched character.
     */
    private char returnCharByRound(Double brightness) {
        switch (currentRound) {
            case "up":
                Map.Entry<Double, TreeSet<Character>> ceilingEntry =
                        charBrightnessMap.ceilingEntry(brightness);
                if (ceilingEntry == null) {
                    // No ceiling entry, fallback to the highest entry in the map
                    return charBrightnessMap.lastEntry().getValue().first();
                }
                return ceilingEntry.getValue().first();

            case "down":
                Map.Entry<Double, TreeSet<Character>> floorEntry =
                        charBrightnessMap.floorEntry(brightness);
                if (floorEntry == null) {
                    // No floor entry, fallback to the lowest entry in the map
                    return charBrightnessMap.firstEntry().getValue().first();
                }
                return floorEntry.getValue().first();

            case "abs":
                Map.Entry<Double, TreeSet<Character>> floorAbsEntry =
                        charBrightnessMap.floorEntry(brightness);
                Map.Entry<Double, TreeSet<Character>> ceilingAbsEntry =
                        charBrightnessMap.ceilingEntry(brightness);

                // Handle cases where one of the entries is null
                if (floorAbsEntry == null) {
                    return ceilingAbsEntry.getValue().first();
                }
                if (ceilingAbsEntry == null) {
                    return floorAbsEntry.getValue().first();
                }

                // Compare the differences between brightness and floor/ceiling keys
                double floorDiff = Math.abs(floorAbsEntry.getKey() - brightness);
                double ceilingDiff = Math.abs(ceilingAbsEntry.getKey() - brightness);
                if (floorDiff <= ceilingDiff) {
                    return floorAbsEntry.getValue().first();
                } else {
                    return ceilingAbsEntry.getValue().first();

                }
            default:
                // Default case for invalid currentRound
                return ' ';
        }
    }


    /**
     * Returns a character based on the image brightness.
     *
     * @param brightness the brightness value.
     * @return the matched character.
     */
    public char getCharByImageBrightness(double brightness) {
      if(changeHasBeenMade){
          changeHasBeenMade = false;
          normalizeBrightness();
      }
      System.out.println(brightness);
        return returnCharByRound(brightness);

    }

    /**
     * Returns the character set.
     *
     * @return the character set.
     */
    public char[] returnCharset(){
        List<Character> sortedChars = new ArrayList<>();
        for (Map.Entry<Double, TreeSet<Character>> entry : charBrightnessMap.entrySet()) {
            sortedChars.addAll(entry.getValue());
        }
        Collections.sort(sortedChars);
        char[] charset = new char[sortedChars.size()];
        int i = 0;
        for (Character c : sortedChars) {
            charset[i++] = c;
        }
        return charset;
    }

    /**
     * Adds a character to the map.
     *
     * @param c the character.
     */
    public void addChar ( char c){
        for (TreeSet<Character> chars : charBrightnessMap.values()) {
            if (chars.contains(c)) {
                return;
            }
        }
        changeHasBeenMade = true;
        double brightness = getBrightness(c);
        charBrightnessMap.putIfAbsent(brightness, new TreeSet<>());
        charBrightnessMap.get(brightness).add(c);
    }

    /**
     * Removes a character from the map.
     *
     * @param c the character to remove.
     */
    public void removeChar ( char c){
        double brightness = getBrightness(c);
        TreeSet<Character> chars = charBrightnessMap.get(brightness);
        if (chars != null) {
            chars.remove(c);
            if (chars.isEmpty()) {
                charBrightnessMap.remove(brightness);
            }
            changeHasBeenMade = true;
        }
    }
}






