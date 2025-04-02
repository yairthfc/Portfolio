package bricker.brick_strategies;

import danogl.GameObject;
import bricker.gameobjects.Brick;
import bricker.main.BrickerGameManager;

/**
 * creates a puck of extra balls on collision with the brick
 */
public class PuckCollisionStrategy implements CollisionStrategy {
    protected final BrickerGameManager brickerGameManager; // game manager
    private boolean isFirst; // is it the first strategy


    /**
     * constructor
     * @param brickerGameManager game manager
     * @param isFirst is it first
     */
    public PuckCollisionStrategy(BrickerGameManager brickerGameManager, boolean isFirst) {
        this.brickerGameManager = brickerGameManager;
        this.isFirst = isFirst;
    }

    /**
     * creates the puck and deletes the brick.
     * @param gameObject1 object 1
     * @param gameObject2 object 2
     */
    @Override
    public void onCollision(GameObject gameObject1, GameObject gameObject2) {
        this.brickerGameManager.createPuck(gameObject1.getCenter());
        this.brickerGameManager.createPuck(gameObject1.getCenter());
        System.out.println("collision with puck brick detected");
        if(isFirst) {
            this.brickerGameManager.removeBrick((Brick) gameObject1);
        }
    }
}
