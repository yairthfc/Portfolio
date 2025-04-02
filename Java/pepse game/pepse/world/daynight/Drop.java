package pepse.world.daynight;

import danogl.GameObject;
import danogl.collisions.GameObjectCollection;
import danogl.components.GameObjectPhysics;
import danogl.components.Transition;
import danogl.gui.rendering.Renderable;
import danogl.util.Vector2;

import java.util.Timer;
import java.util.TimerTask;

/**
 * Represents a drop object in the game world. It has gravity applied to it and can fade out over time.
 */
public class Drop extends GameObject {

    private static final float GRAVITY = 600;//gravity

    /**
     * Constructs a new Drop instance.
     *
     * @param topLeftCorner Position of the drop, in window coordinates (pixels).
     * @param dimensions    Width and height in window coordinates.
     * @param renderable    The renderable representing the drop. Can be null, in which case
     *                      the drop will not be rendered.
     */
    public Drop(Vector2 topLeftCorner, Vector2 dimensions, Renderable renderable) {
        super(topLeftCorner, dimensions, renderable);

        physics().preventIntersectionsFromDirection(Vector2.ZERO);
        physics().setMass(GameObjectPhysics.IMMOVABLE_MASS);
        transform().setAccelerationY(GRAVITY);

    }

    /**
     * Fades out the drop over a specified duration.
     *
     * @param fadeOutTime  The duration over which the drop will fade out.
     * @param afterFadeOut A runnable to execute after the fade-out is complete.
     */
    public void fadeOut(float fadeOutTime, Runnable afterFadeOut) {
        new Transition<>(
                this,
                this.renderer()::setOpaqueness,
                this.renderer().getOpaqueness(),
                0f,
                Transition.LINEAR_INTERPOLATOR_FLOAT,
                fadeOutTime,
                Transition.TransitionType.TRANSITION_ONCE,
                afterFadeOut
        );
    }



    }
