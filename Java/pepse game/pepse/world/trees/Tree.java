package pepse.world.trees;

import danogl.GameObject;
import danogl.components.GameObjectPhysics;
import danogl.gui.rendering.ImageRenderable;
import danogl.gui.rendering.OvalRenderable;
import danogl.gui.rendering.RectangleRenderable;
import danogl.gui.rendering.Renderable;
import danogl.util.Vector2;
import pepse.util.ColorSupplier;

import java.awt.*;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

/**
 * Represents a tree in the game world.
 */
public class Tree extends GameObject {
    private List<Leaf> leafs;//list of leaves
    private List< Fruit> fruits;//list of fruits
    private static final int LEAF_ROW = 8;//number of rows of leaves
    private static final int LEAF_SIZE = 15;//size of the leaf
    private static final int LEAF_SPREAD = 3;//spread of the leaf
    private static final Color LEAF_COLOR = new Color(50, 100, 30);//color of the leaf
    private static final double FRUIT_PROBABILITY = 0.1;//probability of fruit
    private static final double LEAF_PROBABILITY = 0.5;//probability of leaf

    /**
     * Construct a new GameObject instance.
     *
     * @param topLeftCorner Position of the object, in window coordinates (pixels).
     *                      Note that (0,0) is the top-left corner of the window.
     * @param dimensions    Width and height in window coordinates.
     * @param renderable    The renderable representing the object. Can be null, in which case
     *                      the GameObject will not be rendered.
     */
    public Tree(Vector2 topLeftCorner, Vector2 dimensions, Renderable renderable) {
        super(topLeftCorner, dimensions, renderable);
        physics().preventIntersectionsFromDirection(Vector2.ZERO);
        physics().setMass(GameObjectPhysics.IMMOVABLE_MASS);
        createLeafs();
    }



    /**
     * Creates the leaves for the tree.
     */
    private void createLeafs() {
        this.leafs = new ArrayList<>();
        this.fruits = new ArrayList<>();
        float startY = this.getCenter().y() - LEAF_ROW * LEAF_SIZE;
        float startX = this.getCenter().x() - LEAF_SIZE * LEAF_ROW / 2;

        for (int i = 0; i < LEAF_ROW; i++) {
            float y = startY + i * LEAF_SIZE + LEAF_SIZE;
            for (int j = 0; j < LEAF_ROW; j++) {
                float x = startX + j * LEAF_SIZE;
                if (Math.random() <LEAF_PROBABILITY) {
                    RectangleRenderable renderable = new
                            RectangleRenderable(ColorSupplier.approximateColor(LEAF_COLOR));
                    this.leafs.add(new Leaf(new Vector2(x, y), new Vector2(LEAF_SIZE, LEAF_SIZE),
                            renderable));
                } else if (Math.random() < FRUIT_PROBABILITY) {
                    OvalRenderable renderable = new OvalRenderable(Color.YELLOW);
                    fruits.add(new Fruit(new Vector2(x, y), new Vector2(LEAF_SIZE, LEAF_SIZE), renderable));
                }
            }
        }
    }

    /**
     * Returns the list of leaves.
     *
     * @return List of leaves.
     */
    public List<Leaf> getLeafs() {
        return this.leafs;
    }

    /**
     * Returns the list of fruits.
     *
     * @return List of fruits.
     */
    public List<Fruit> getFruits() {
        return this.fruits;
    }

}
