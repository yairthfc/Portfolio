package image;

//import exceptions.InvalidInputException;
import image_char_matching.SubImgCharMatcher;

import java.awt.*;


/**
 * Class to edit images and convert them to ASCII art.
 */
public class ImageEditor {
    private Color[][] image;//original image
    private Color[][][][] ListOfImages;//list of sub-images from the main image.
    private int resolution ; //resolution of the ascii image
    private int imageHeight; //height of the original image
    private int imageWidth;//width of the original image
    private final float redWeight = 0.2126f; // red weight
    private final float greenWeight = 0.7152f;// green weight
    private final float blueWeight = 0.0722f;// blue weight
    private final int maxBrightness = 255;//max brightness
    private final int two =2; //constant two
    private final float brightnessThreshold = 0.5f; // half o divided by the image height
    private int widthPadSize; //width padding size
    private int heightPadSize; //height padding size
    private boolean firstTime = true; //check if it is the first time we enter the function
    private boolean resulotionChanged = true; //check if the resolution is the same as the original image
    private char[][] asciiImage; //ascii image
    private double[][] doubleImage; //double image
    /**
     * Constructs a new ImageEditor with the specified image and resolution.
     *
     * @param image the image to be edited.
     * @param resolution the resolution for the ASCII art.
     */
    public ImageEditor(Image image,int resolution) {
        this.resolution = resolution;
        //this.asciiImage = new char[resolution][resolution];
        this.imageHeight = image.getHeight();
        this.imageWidth = image.getWidth();
      // this.doubleImage = new double[resolution][resolution];
        this.image = new Color[this.imageHeight][this.imageWidth];
        for (int i = 0; i < this.imageHeight; i++) {
            for (int j = 0; j < this.imageWidth; j++) {
              Color pixelColor  = image.getPixel(i,j);
                this.image[i][j] = new Color(pixelColor.getRed(),pixelColor.getGreen(),pixelColor.getBlue());
            }
        }
    }

    /**
     * Changes the resolution of the image based on the input.
     *
     * @param input the input to change the resolution ("up" or "down").
     * @throws IllegalArgumentException if the input is invalid.
     */
    public void changeResolution(String input) throws IllegalArgumentException {
        switch (input) {
            case "up":
                if ( this.resolution <= brightnessThreshold * this.imageWidth) {
                    this.resolution *= two;
                    resulotionChanged = true;
                }
                else {
                   throw new IllegalArgumentException();
                }
                break;
            case "down":
                if (this.resolution > Math.max(1,this.imageWidth/this.imageHeight )) {
                    this.resolution /= two;
                    resulotionChanged = true;
                }
                else {
                    throw new IllegalArgumentException();
                }
                break;
        }
    }


    /**
     * Returns the current resolution of the image.
     *
     * @return the current resolution.
     */
    public int returnResolution(){
        return this.resolution;
    }

    /**
     * Pads the image to make its dimensions a power of two.
     */
    private void PadImage() {
        int padWidth = this.imageWidth;
        int padHeight = this.imageHeight;
        int widthTimes = 2;
        while(padWidth>two){
            padWidth = padWidth/two;
            widthTimes++;
        }
        int heightTimes = 2;
        while(padHeight>two){

            padHeight = padHeight/two;
            heightTimes++;
        }
        int newWidth = (int) Math.pow(two,widthTimes);
        int newHeight =(int) Math.pow(two,heightTimes);
        widthPadSize = (newWidth - this.imageWidth)/two ;
        heightPadSize = (newHeight- this.imageHeight)/two ;
        Color[][] newImage = new Color[newHeight][newWidth];
        for(int i = 0; i < newHeight; i++){
            for(int j = 0; j < newWidth; j++){
                if(j<widthPadSize||i<heightPadSize||j>=widthPadSize+this.imageWidth
                        ||i>= heightPadSize+this.imageHeight){
                    newImage[i][j]=Color.white;
                }
                else {
                    newImage[i][j]= image[i-heightPadSize][j-widthPadSize];
                }
            }
        }
        this.imageHeight = newHeight;
        this.imageWidth = newWidth;
        this.image = newImage;
    }

    /**
     * Divides the image into smaller images based on the resolution.
     */
    private void DivideByResolution() {
        int resolutionInHeight = imageHeight/ this.resolution;
        int resolutionInWidth = imageWidth / this.resolution;

        ListOfImages = new Color[this.resolution][this.resolution][resolutionInHeight][resolutionInWidth];
        for (int i = 0; i < this.resolution;i++) {
            for (int j = 0; j < this.resolution;  j++) {
                for (int k = 0; k < resolutionInHeight; k++) {
                    for (int l = 0; l < resolutionInWidth; l++) {
                        ListOfImages[i][j][k][l] =
                                image[i * resolutionInHeight + k][j * resolutionInWidth + l];

                    }
                }
            }
        }

    }

    /**
     * Calculates the brightness of the sub-image.
     *
     * @param image the image to calculate the brightness.
     * @return the brightness of the sub-image.
     */
    private double BrightnessCalculation(Color[][] image)
    {
        double totalBrightness = 0;
        int imageHeight=image.length;
        int imageWidth=image[0].length;
        for (int i = 0; i < imageHeight; i++) {
            for (int j = 0; j < imageWidth; j++) {
                    totalBrightness+=image[i][j].getRed()*redWeight+
                            image[i][j].getGreen()*greenWeight+ image[i][j].getBlue()*blueWeight;
                }
        }
        return totalBrightness/(maxBrightness*imageHeight*imageWidth);
    }

    /**
     * Converts the image to an ASCII art representation.
     *
     * @param SubImgCharMatcher the character matcher.
     * @return a 2D array of characters representing the ASCII image.
     */
    public char[][] GetAsciiImage(SubImgCharMatcher SubImgCharMatcher){
        if (firstTime){
            PadImage();
            DivideByResolution();
            firstTime = false;
        }
       if (resulotionChanged){
            DivideByResolution();
            resulotionChanged = false;
           doubleImage = new double[this.resolution][this.resolution];
           asciiImage = new char[this.resolution][this.resolution];
           for(int i = 0; i < this.resolution; i++){
               for(int j = 0; j < this.resolution; j++){
                   doubleImage[i][j]= BrightnessCalculation(ListOfImages[i][j]);
               }
           }
        }
        for (int i = 0; i < this.resolution; i++) {
            for (int j = 0; j < this.resolution; j++) {
                asciiImage[i][j] = SubImgCharMatcher.getCharByImageBrightness(doubleImage[i][j]);
            }
        }
        return asciiImage;

    }

}


