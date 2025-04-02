package pepse.world.daynight;

import danogl.GameObject;
import danogl.components.CoordinateSpace;
import danogl.components.Transition;
import danogl.gui.rendering.RectangleRenderable;
import danogl.util.Vector2;

import java.awt.*;

/**
 * Represents the night cycle in the game world.
 */
public class Night {
    private static final float MIDNIGHT_OPACITY = 0.5f;//midnight opacity
    private static final int TRANSITION_TIME_DIV = 2;//transition time division

    /**
     * Creates a night effect in the game world.
     *
     * @param windowDimensions The dimensions of the game window.
     * @param cycleLength      The length of the night-day cycle.
     * @return A GameObject representing the night effect.
     */
    public static GameObject create(Vector2 windowDimensions, float cycleLength){
        RectangleRenderable renderable = new RectangleRenderable(Color.BLACK);
        GameObject night = new GameObject(Vector2.ZERO, windowDimensions, renderable);
        night.setCoordinateSpace(CoordinateSpace.CAMERA_COORDINATES);
        night.setTag("night");
        Transition transition = new Transition<Float>(night, night.renderer()::setOpaqueness,0f,
                MIDNIGHT_OPACITY, Transition.CUBIC_INTERPOLATOR_FLOAT,
                cycleLength/TRANSITION_TIME_DIV,
                Transition.TransitionType.TRANSITION_BACK_AND_FORTH, null);
        return night;
    }
}
