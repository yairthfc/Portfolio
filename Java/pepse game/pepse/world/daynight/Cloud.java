package pepse.world.daynight;

import danogl.GameObject;
import danogl.components.CoordinateSpace;
import danogl.components.Transition;
import danogl.gui.rendering.RectangleRenderable;
import danogl.util.Vector2;
import pepse.util.ColorSupplier;
import pepse.world.Block;

import java.awt.*;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

/**
 * Represents a cloud in the game world.
 */
public class Cloud {
    private static final Color BASE_CLOUD_COLOR = new Color(255, 255, 255);//base cloud color
    private List<List<GameObject>> cloud;//list of cloud
    private static final int CLOUD_ROWS=4;//number of rows of cloud
    private static final int CLOUD_COLUMNS = 6;//number of columns of cloud
    private static final int CLOUD_EDGE_RANDOMNESS = 2;//randomness of the cloud edge
    private static final float START_CLOUD_HEIGHT_RATIO = 0.25f;//start cloud height ratio
    private static final int EQUAL_TO_FIVE = 5;//equal to 5
    private static final int EQUAL_TO_THREE = 3;//equal to 3
    private static final int CLOUD_CYCLE_LENGTH = 5;//cloud cycle length




    /**
     * Generates cloud positions with randomness.
     *
     * @return A list of lists representing cloud positions.
     */
    private static List<List<Integer>> generateCloudPositions() {
        Random random = new Random();
        List<List<Integer>> cloudPositions = new ArrayList<>();

        for (int i = 0; i < CLOUD_ROWS; i++) { // 4 rows for height
            List<Integer> row = new ArrayList<>();
            for (int j = 0; j < CLOUD_COLUMNS; j++) { // 6 columns for width
                if (i == 0 || i == EQUAL_TO_THREE || j == 0 || j == EQUAL_TO_FIVE) {
                    row.add(random.nextInt(CLOUD_EDGE_RANDOMNESS)); // Randomly 0 or 1
                } else {
                    row.add(1);
                }
            }
            cloudPositions.add(row);
        }
        return cloudPositions;
    }


    /**
     * Creates a cloud in the game world.
     *
     * @param windowDimensions The dimensions of the game window.
     * @param cycleLength      The length of the cloud cycle.
     * @return A list of GameObjects representing the cloud.
     */
    public static List<GameObject> create(Vector2 windowDimensions, float cycleLength) {
        RectangleRenderable cloudBlock = new RectangleRenderable(ColorSupplier
                .approximateMonoColor(BASE_CLOUD_COLOR));

        // Dynamically generate cloud positions with thinner dimensions
        List<List<Integer>> cloudPositions = generateCloudPositions();

        float startCloudHeight = windowDimensions.y() / CLOUD_ROWS;
        float startCloudWidth = 0 - CLOUD_COLUMNS * Block.SIZE;
        List<GameObject> cloudFinal = new ArrayList<>();

        for (int i = 0; i < cloudPositions.size(); i++) {
            for (int j = 0; j < cloudPositions.get(i).size(); j++) {

                if (cloudPositions.get(i).get(j) == 1) {
                    Block block = new Block(
                            new Vector2(startCloudWidth + j * Block.SIZE, startCloudHeight + i * Block.SIZE),
                            cloudBlock
                    );
                    block.setCoordinateSpace(CoordinateSpace.CAMERA_COORDINATES);
                    Transition transition = new Transition<>(
                            block,
                            block::setCenter,
                            new Vector2(startCloudWidth + j * Block.SIZE, startCloudHeight + i * Block.SIZE),
                            new Vector2(windowDimensions.x() + j * Block.SIZE, block.getTopLeftCorner().y()),
                            Transition.LINEAR_INTERPOLATOR_VECTOR,
                            cycleLength,
                            Transition.TransitionType.TRANSITION_LOOP,
                            null
                    );
                    cloudFinal.add(block);
                }
            }
        }
        return cloudFinal;
    }





}
