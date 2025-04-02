package pepse.world.trees;

import danogl.GameObject;
import danogl.collisions.Collision;
import danogl.components.GameObjectPhysics;
import danogl.components.ScheduledTask;
import danogl.components.Transition;
import danogl.gui.rendering.Renderable;
import danogl.util.Vector2;
import pepse.world.Avatar;
/**
 * Represents a fruit in the game world. The fruit can be collected by the avatar to gain energy.
 */
public class Fruit extends GameObject {
    private static final int FRUIT_NEW_PLACE = -10000;//new place for the fruit
    private static final int ENERGY_TO_ADD = 10;// Energy to add to the player
    private static final int FRUIT_CYCLE = 30;//cycle of the fruit

    private final Renderable renderable;
    /**
     * Constructs a new Fruit instance.
     *
     * @param topLeftCorner Position of the fruit, in window coordinates (pixels).
     * @param dimensions    Width and height in window coordinates.
     * @param renderable    The renderable representing the fruit. Can be null, in which case
     *                      the fruit will not be rendered.
     */
    public Fruit(Vector2 topLeftCorner, Vector2 dimensions, Renderable renderable) {
        super(topLeftCorner, dimensions, renderable);
        this.renderable = renderable;
        physics().preventIntersectionsFromDirection(Vector2.ZERO);
        physics().setMass(GameObjectPhysics.IMMOVABLE_MASS);
    }

    /**
     * Handles collision with other game objects.
     *
     * @param other     The other game object.
     * @param collision The collision information.
     */
    @Override
    public void onCollisionEnter(GameObject other, Collision collision) {
        super.onCollisionEnter(other, collision);
        if (other instanceof Avatar) {
            //renderer().setRenderable(null);
            Vector2 originalPosition = getCenter();
            //System.out.println(getCenter());
            setTopLeftCorner(new Vector2(originalPosition.x(), FRUIT_NEW_PLACE));
            ((Avatar) other).addEnergy(ENERGY_TO_ADD);
            new ScheduledTask(
                    this,
                    FRUIT_CYCLE,
                    false,
                    () -> {renderer().setRenderable(this.renderable);
                            setTopLeftCorner(originalPosition);

                    }


            );
        }
    }
}


