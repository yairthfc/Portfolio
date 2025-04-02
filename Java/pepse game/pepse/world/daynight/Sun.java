package pepse.world.daynight;

import danogl.GameObject;
import danogl.components.CoordinateSpace;
import danogl.components.Transition;
import danogl.gui.rendering.OvalRenderable;
import danogl.util.Vector2;

import java.awt.*;

/**
 * Represents the sun in the game world.
 */
public class Sun {
    private static final Vector2 SUN_SIZE = new Vector2(100, 100);//sun size
    private static final float FULL_ROTATION = 360f;//full rotation
    private static final float SUN_DIV = 2;//sun division
    private static final float CYCLE_LENGTH = 30;//cycle length
    private static final float WINDOW_DIV = 3;//window division

    /**
     * Creates a sun effect in the game world.
     *
     * @param windowDimensions The dimensions of the game window.
     * @param cycleLength      The length of the sun's movement cycle.
     * @return A GameObject representing the sun.
     */
    public static GameObject create(Vector2 windowDimensions, float cycleLength){
        OvalRenderable ovalRenderable = new OvalRenderable(Color.YELLOW);
        GameObject sun = new GameObject(new Vector2((windowDimensions.x()/SUN_DIV) - (SUN_SIZE.x()/SUN_DIV),
                windowDimensions.y()/WINDOW_DIV - (SUN_SIZE.x()/SUN_DIV)),SUN_SIZE, ovalRenderable);
        sun.setCoordinateSpace(CoordinateSpace.CAMERA_COORDINATES);
        sun.setTag("sun");
        Vector2 initialSunCenter = sun.getCenter();
        Vector2 cycleCenter = new Vector2(windowDimensions.x()/SUN_DIV,
                windowDimensions.y() * SUN_DIV / WINDOW_DIV);
        Transition transition = new Transition<Float>(sun, (Float angle) ->
                sun.setCenter(initialSunCenter.subtract(cycleCenter).rotated(angle).add(cycleCenter)),
                FULL_ROTATION, 0f,Transition.LINEAR_INTERPOLATOR_FLOAT,
                CYCLE_LENGTH, Transition.TransitionType.TRANSITION_LOOP, null);
        return sun;
    }
}
