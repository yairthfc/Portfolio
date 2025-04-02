package ascii_art;


import image.ImageEditor;
import image_char_matching.SubImgCharMatcher;

/**
 * Class to generate ASCII art from an image.
 */
public class AsciiArtAlgorithm {


    private ImageEditor imageEditor;//image editor
    private SubImgCharMatcher subImgCharMatcher; // sub image character matcher

    /**
     * Constructs a new AsciiArtAlgorithm with the specified image editor and sub-image character matcher.
     *
     * @param imageEditor the image editor.
     * @param subImgCharMatcher the sub-image character matcher.
     */
    public AsciiArtAlgorithm(ImageEditor imageEditor, SubImgCharMatcher subImgCharMatcher) {
        this.imageEditor = imageEditor;
        this.subImgCharMatcher = subImgCharMatcher;
    }

    /**
     * Runs the algorithm to generate the ASCII art.
     *
     * @return the ASCII art.
     */
    public char[][] run() {
        return imageEditor.GetAsciiImage(subImgCharMatcher);
    }


}
