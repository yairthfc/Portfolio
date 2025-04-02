package bricker.gameobjects;

import danogl.GameObject;
import danogl.collisions.Collision;
import danogl.gui.UserInputListener;
import danogl.gui.rendering.Renderable;
import danogl.util.Vector2;

import java.awt.event.KeyEvent;

/**
 * a class for a paddle object
 */
public class Paddle extends GameObject {
    private static final float MOVEMENT_SPEED = 300f; // paddle speed
    private final UserInputListener inputListener; // input listener
    private final Vector2 windowDimensions; // the window dimensions
    private int collisionCounter; // the collision counter of the paddle

    /**
     * Construct a new GameObject instance.
     *
     * @param topLeftCorner Position of the object, in window coordinates (pixels).
     *                      Note that (0,0) is the top-left corner of the window.
     * @param dimensions    Width and height in window coordinates.
     * @param renderable    The renderable representing the object. Can be null, in which case
     *                      the GameObject will not be rendered.
     * @param inputListener the input listener
     * @param windowDimensions the window dimensions
     */
    public Paddle(Vector2 topLeftCorner, Vector2 dimensions, Renderable renderable, UserInputListener inputListener, Vector2 windowDimensions) {
        super(topLeftCorner, dimensions, renderable);
        this.inputListener = inputListener;
        this.windowDimensions = windowDimensions;
    }

    /**
     * update the location and monenment of the paddle according to user input.
     * @param deltaTime The time elapsed, in seconds, since the last frame. Can
     *                  be used to determine a new position/velocity by multiplying
     *                  this delta with the velocity/acceleration respectively
     *                  and adding to the position/velocity:
     *                  velocity += deltaTime*acceleration
     *                  pos += deltaTime*velocity
     */
    @Override
    public void update(float deltaTime) {
        super.update(deltaTime);

        Vector2 movementDir = Vector2.ZERO;
        if (inputListener.isKeyPressed(KeyEvent.VK_LEFT)) {
            movementDir = movementDir.add(Vector2.LEFT);
        }
        if (inputListener.isKeyPressed(KeyEvent.VK_RIGHT)) {
            movementDir = movementDir.add(Vector2.RIGHT);
        }
        setVelocity(movementDir.mult(MOVEMENT_SPEED));

        // prevent from hitting the walls
        if(this.getTopLeftCorner().x() < 0 ) {
            this.setTopLeftCorner(new Vector2(0, getTopLeftCorner().y()));
        }
        if(this.getTopLeftCorner().x() > windowDimensions.x() - this.getDimensions().x()) {
            this.setTopLeftCorner(new Vector2(windowDimensions.x() - this.getDimensions().x(), getTopLeftCorner().y()));
        }
    }

    /**
     * change the direction of an object that hits the paddle and update the counter.
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
        collisionCounter++;
    }

    /**
     * get collision counter
     * @return collisionCounter
     */
    public int getCollisionCounter() {
        return collisionCounter;
    }

}
