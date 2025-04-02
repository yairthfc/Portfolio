package pepse.world.trees;

import danogl.gui.rendering.RectangleRenderable;
import danogl.util.Vector2;
import pepse.util.ColorSupplier;
import pepse.world.Block;
import pepse.world.trees.Tree;

import java.awt.*;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;
import java.util.function.Function;

/**
 * Manages the creation and placement of trees in the game world.
 */
public class Flora {
    private Random random;// = new Random();
    private Function<Float, Float> groundHeightAt; // Accepts a float and returns a float

    /**
     * The dimensions of the trees to be created.
     */
    public static final Vector2 TREE_DIMENSIONS = new Vector2(30, 180);
    private static final float THRESHOLD = 0.1f;//threshold for tree creation;
    private static final int TREEHEIGHT = 6; //height of the tree
    private final Color TREE_COLOR = new Color(100, 50, 20);//color of the tree
    private float screenHeigth;//height of the screen
    private static final float SCREEN_DIV = 240;//division of the screen

    /**
     * Constructs a new Flora instance.
     *
     * @param groundHeightAt Function to determine the ground height at a given x-coordinate.
     * @param seed           Seed for random number generation.
     * @param treeDimensions Dimensions of the trees to be created.
     */
    public Flora(Function<Float, Float> groundHeightAt, int seed, Vector2 treeDimensions) {
        this.groundHeightAt = groundHeightAt;
        this.random = new Random(seed);
        this.screenHeigth = treeDimensions.y();
    }

    /**
     * Determines whether a tree should be planted at a given location.
     *
     * @return true if a tree should be planted, false otherwise.
     */
    public boolean plantHere() {
        // Your logic here
        return random.nextFloat() < THRESHOLD; // Example
    }

    /**
     * Creates trees in the specified range.
     *
     * @param minX Minimum x-coordinate.
     * @param maxX Maximum x-coordinate.
     * @return List of trees created.
     */
    public List<Tree> createInRange(int minX, int maxX) {
        List<Tree> trees = new ArrayList<>();
        float startWidth = (float) ((Math.floor(minX / Block.SIZE)) * Block.SIZE);
        float endWidth = (float) ((Math.floor(maxX / Block.SIZE) + 1) * Block.SIZE);
        float curWidth = startWidth;


        while (curWidth < endWidth)
        {
            if (plantHere()) {
                float groundHeight = groundHeightAt.apply(curWidth);
                float treeTopLeftCorner =-groundHeight+TREE_DIMENSIONS.y()*screenHeigth/SCREEN_DIV;
                RectangleRenderable renderable =
                        new RectangleRenderable(ColorSupplier.approximateColor(TREE_COLOR));
                trees.add(new Tree(new Vector2(curWidth,treeTopLeftCorner),TREE_DIMENSIONS, renderable));
            }
            curWidth += Block.SIZE;
        }
        return trees;
    }

}
