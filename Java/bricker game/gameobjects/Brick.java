package bricker.gameobjects;

import bricker.brick_strategies.CollisionStrategy;
import danogl.GameObject;
import danogl.collisions.Collision;
import danogl.gui.rendering.Renderable;
import danogl.util.Vector2;

/**
 * a class for a game object of brick.
 */
public class Brick extends GameObject {
    private CollisionStrategy firstCollisionStrategy; // first collision strategy
    private CollisionStrategy secondCollisionStrategy; // second collision strategy
    private CollisionStrategy thirdCollisionStrategy; // third collision strategy
    private final static int MAX_NUM_OF_STRATEGIES = 3; // maximum number of strategies
    private int numOfStrategies; // number of strategies

    /**
     * Construct a new GameObject instance with a single strategy.
     *
     * @param topLeftCorner Position of the object, in window coordinates (pixels).
     *                      Note that (0,0) is the top-left corner of the window.
     * @param dimensions    Width and height in window coordinates.
     * @param renderable    The renderable representing the object. Can be null, in which case
     *                      the GameObject will not be rendered.
     * @param collisionStrategy the collision strategy of the brick.
     */
    public Brick(Vector2 topLeftCorner, Vector2 dimensions, Renderable renderable, CollisionStrategy collisionStrategy) {
        super(topLeftCorner, dimensions, renderable);
        this.firstCollisionStrategy = collisionStrategy;
        numOfStrategies = 1;
    }

    /**
     * Construct a new GameObject instance with 2 strategies.
     *
     * @param topLeftCorner Position of the object, in window coordinates (pixels).
     *                      Note that (0,0) is the top-left corner of the window.
     * @param dimensions    Width and height in window coordinates.
     * @param renderable    The renderable representing the object. Can be null, in which case
     *                      the GameObject will not be rendered.
     * @param collisionStrategy first collision strategy of the brick.
     * @param collisionStrategy2 second collision strategy of the brick.
     */
    public Brick(Vector2 topLeftCorner, Vector2 dimensions, Renderable renderable, CollisionStrategy collisionStrategy,CollisionStrategy collisionStrategy2) {
        super(topLeftCorner, dimensions, renderable);
        this.firstCollisionStrategy = collisionStrategy;
        this.secondCollisionStrategy = collisionStrategy2;
        numOfStrategies = 2;
    }

    /**
     * Construct a new GameObject instance with 3 strategies.
     *
     * @param topLeftCorner Position of the object, in window coordinates (pixels).
     *                      Note that (0,0) is the top-left corner of the window.
     * @param dimensions    Width and height in window coordinates.
     * @param renderable    The renderable representing the object. Can be null, in which case
     *                      the GameObject will not be rendered.
     * @param collisionStrategy first collision strategy of the brick.
     * @param collisionStrategy2 second collision strategy of the brick.
     * @param collisionStrategy3 third collision strategy of the brick.
     */
    public Brick(Vector2 topLeftCorner, Vector2 dimensions, Renderable renderable, CollisionStrategy collisionStrategy,CollisionStrategy collisionStrategy2, CollisionStrategy collisionStrategy3) {
        super(topLeftCorner, dimensions, renderable);
        this.firstCollisionStrategy = collisionStrategy;
        this.secondCollisionStrategy = collisionStrategy2;
        this.thirdCollisionStrategy = collisionStrategy3;
        numOfStrategies = 3;
    }

    /**
     * activates the bricks strategies in case of a collision with the brick.
     * @param other     The GameObject with which a collision occurred.
     * @param collision Information regarding this collision.
     *                  A reasonable elastic behavior can be achieved with:
     *                  setVelocity(getVelocity().flipped(collision.getNormal()));
     */
    @Override
    public void onCollisionEnter(GameObject other, Collision collision) {
        super.onCollisionEnter(other, collision);
        firstCollisionStrategy.onCollision(this, other);
        if(numOfStrategies >= 2) {
            secondCollisionStrategy.onCollision(this, other);
        }
        if(numOfStrategies == 3) {
            thirdCollisionStrategy.onCollision(this, other);
        }

    }
}
