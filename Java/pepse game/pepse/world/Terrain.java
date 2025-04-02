package pepse.world;

import danogl.gui.rendering.RectangleRenderable;
import pepse.util.ColorSupplier;
import pepse.util.NoiseGenerator;
import danogl.util.Vector2;
import pepse.world.Block;

import java.awt.*;
import java.util.ArrayList;
import java.util.List;

import java.util.List;

/**
 * Represents the terrain in the game world.
 */
public class Terrain {
    private float groundHeightAtX0;//ground height at x
    private NoiseGenerator noiseGenerator;//noise generator
    private static final Color BASE_GROUND_COLOR = new Color(212, 123, 74);//base ground color
    private static final int GROUND_HEIGHT_DIV = 3;//division of the ground height
    private Vector2 windowDimensions;//window dimensions

    /**
     * Constructor
     * @param windowDimensions
     * @param seed
     */
    public Terrain(Vector2 windowDimensions, int seed){
        this.groundHeightAtX0 = windowDimensions.y()/ GROUND_HEIGHT_DIV;
        this.windowDimensions = windowDimensions;
        noiseGenerator = new NoiseGenerator(seed, (int) groundHeightAtX0);
    }

    /**
     * Returns the ground height at a given x coordinate.
     * @param x
     * @return
     */
    public float groundHeightAt(float x){
        float noise = (float) noiseGenerator.noise(x, Block.SIZE*7);
        return groundHeightAtX0 + noise;
    }

    /**
     * Creates a list of blocks in the given range.
     * @param minX
     * @param maxX
     * @return
     */
    public List<Block> createInRange(int minX, int maxX){
        RectangleRenderable renderable = new RectangleRenderable(ColorSupplier.
                approximateColor(BASE_GROUND_COLOR));
        List<Block> blocks = new ArrayList<Block>();
        System.out.println(groundHeightAtX0);
        float startWidth = (float) ((Math.floor(minX/Block.SIZE)) * Block.SIZE);
        double endWidth = (Math.floor(maxX/Block.SIZE) + 1) * Block.SIZE;
        int numOfBlocksOnWidth = (int) (endWidth - startWidth)/Block.SIZE;
        float curWidth = startWidth;
        for (int i = 0; i < numOfBlocksOnWidth; i++) {
            float curHeight = windowDimensions.y() - Block.SIZE;
            float maxHeight = (float) ((Math.floor(groundHeightAt(curWidth)/Block.SIZE) + 1) * Block.SIZE);
            for (int j = 0; j < maxHeight/Block.SIZE; j++) {
                Block block = new Block(new Vector2(curWidth, curHeight), renderable);
                blocks.add(block);
                curHeight -= Block.SIZE;
            }
            curWidth += Block.SIZE;
        }
        return blocks;
    }
}
