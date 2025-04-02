package bricker.brick_strategies;

import bricker.gameobjects.Brick;
import bricker.main.BrickerGameManager;
import danogl.GameObject;

/**
 * basic collision strategy for a brick which just removes it.
 */
public class BasicCollisionStrategy implements CollisionStrategy {
    protected final BrickerGameManager brickerGameManager;

    /**
     * constructor for the strategy.
     * @param brickerGameManager the game manager.
     */
    public BasicCollisionStrategy(BrickerGameManager brickerGameManager) {
        this.brickerGameManager = brickerGameManager;
    }

    /**
     * removes the brick on collision.
     * @param gameObject1 first object
     * @param gameObject2 second object
     */
    @Override
    public void onCollision(GameObject gameObject1, GameObject gameObject2) {
        System.out.println("collision with brick detected");
        brickerGameManager.removeBrick((Brick) gameObject1);

    }
}
