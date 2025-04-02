package bricker.gameobjects;

import danogl.GameObject;
import danogl.collisions.Collision;
import danogl.gui.Sound;
import danogl.gui.rendering.Renderable;
import danogl.util.Vector2;

/**
 * class of a game ball object.
 */
public class Ball extends GameObject {
    private final Sound collisionSound; // sound of collision.
    private int collisionCounter; //number of times the ball hit anything.
    /**
     * Construct a new GameObject instance.
     *
     * @param topLeftCorner Position of the object, in window coordinates (pixels).
     *                      Note that (0,0) is the top-left corner of the window.
     * @param dimensions    Width and height in window coordinates.
     * @param renderable    The renderable representing the object. Can be null, in which case
     *                      the GameObject will not be rendered.
     */
    public Ball(Vector2 topLeftCorner, Vector2 dimensions, Renderable renderable,
                Sound collisionSound) {
        super(topLeftCorner, dimensions, renderable);
        this.collisionSound = collisionSound;
        collisionCounter = 0;
    }

    /**
     * change the direction of the ball when hit, make a sound and raise the counter.
     * @param other     The GameObject with which a collision occurred.
     * @param collision Information regarding this collision.
     *                  A reasonable elastic behavior can be achieved with:
     *                  setVelocity(getVelocity().flipped(collision.getNormal()));
     */
    @Override
    public void onCollisionEnter(GameObject other, Collision collision) {
        super.onCollisionEnter(other, collision);
        Vector2 newVal1 = getVelocity().flipped(collision.getNormal());
        setVelocity(newVal1);
        collisionSound.play();
        collisionCounter++;
    }

//    /**
//     * reset collision counter.
//     */
//    public void resetCollisionCounter() {
//        collisionCounter = 0;
//    }

    /**
     * get collision counter.
     * @return collisionCounter
     */
    public int getCollisionCounter() {
        return collisionCounter;
    }
}
