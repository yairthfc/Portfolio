package bricker.brick_strategies;

import danogl.GameObject;
import bricker.gameobjects.Brick;
import bricker.main.BrickerGameManager;

/**
 * heart collision strategy which drops a heart to collect from the brick.
 */
public class HeartCollisionStrategy implements CollisionStrategy{
    protected final BrickerGameManager brickerGameManager; // game manager
    private boolean isFirst; // is it the first strategy

    /**
     * constructor
     * @param brickerGameManager game manager
     * @param isFirst is it first
     */
    public HeartCollisionStrategy(BrickerGameManager brickerGameManager, boolean isFirst) {
        this.brickerGameManager = brickerGameManager;
        this.isFirst = isFirst;
    }

    /**
     * creating a collectable heart falling from the sky and deletes brick.
     * @param gameObject1 object 1
     * @param gameObject2 object 2
     */
    @Override
    public void onCollision(GameObject gameObject1, GameObject gameObject2) {
        this.brickerGameManager.createHeart(gameObject1.getCenter());
        System.out.println("collision with heart brick detected");
        if(isFirst) {
            brickerGameManager.removeBrick((Brick) gameObject1);
        }
    }
}
