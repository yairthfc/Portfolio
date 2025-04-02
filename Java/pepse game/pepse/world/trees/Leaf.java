package pepse.world.trees;

import danogl.GameObject;
import danogl.components.GameObjectPhysics;
import danogl.components.ScheduledTask;
import danogl.components.Transition;
import danogl.gui.rendering.Renderable;
import danogl.util.Vector2;
import java.util.Random;

/**
 * Represents a leaf in the game world.
 */
public class Leaf extends GameObject {
    private static final float LEAF_CYCLE = 30;//cycle of the leaf
    private static final float TRANSITION_DURATION = 2;//duration of the transition
    /**
     * Constructs a new Leaf instance.
     *
     * @param topLeftCorner Position of the leaf, in window coordinates (pixels).
     * @param dimensions    Width and height in window coordinates.
     * @param renderable    The renderable representing the leaf. Can be null, in which case
     *                      the leaf will not be rendered.
     */
    public Leaf(Vector2 topLeftCorner, Vector2 dimensions, Renderable renderable) {
        super(topLeftCorner, dimensions, renderable);
        physics().preventIntersectionsFromDirection(Vector2.ZERO);
        physics().setMass(GameObjectPhysics.IMMOVABLE_MASS);
        Random random = new Random();
        ScheduledTask leafMovement = new ScheduledTask
                (this, random.nextFloat(), true,this::leafMovement);

    }
    /**
     * Defines the movement behavior of the leaf.
     */
    private void leafMovement(){

            new Transition<>(
                    this,
                    renderer()::setRenderableAngle,
                    0f,
                    LEAF_CYCLE,
                    Transition.LINEAR_INTERPOLATOR_FLOAT,
                    TRANSITION_DURATION,
                    Transition.TransitionType.TRANSITION_BACK_AND_FORTH,
                    null
            );setDimensions(Vector2.of(getDimensions().x(), getDimensions().y()*5));

            new Transition<>(
                    this,
                    angle -> renderer().setRenderableAngle(angle),
                    0f,
                    LEAF_CYCLE,
                    Transition.LINEAR_INTERPOLATOR_FLOAT,
                    TRANSITION_DURATION,
                    Transition.TransitionType.TRANSITION_BACK_AND_FORTH,
                    null
            );
            setDimensions(Vector2.of(getDimensions().x(), getDimensions().y()/5));
        }

    }


