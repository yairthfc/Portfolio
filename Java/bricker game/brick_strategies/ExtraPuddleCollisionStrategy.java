package bricker.brick_strategies;

import danogl.GameObject;
import bricker.gameobjects.Brick;
import bricker.main.BrickerGameManager;

/**
 * extra paddle collision strategy that adds a paddle to the game
 */
public class ExtraPuddleCollisionStrategy implements CollisionStrategy {
    private boolean isFirst; //is it the bricks first strategy
    protected final BrickerGameManager brickerGameManager; //bricker game manager

    /**
     * constructor
     * @param brickerGameManager game manager
     * @param isFirst if irs first strategy
     */
    public ExtraPuddleCollisionStrategy(BrickerGameManager brickerGameManager, boolean isFirst) {
        this.brickerGameManager = brickerGameManager;
        this.isFirst = isFirst;

    }

    /**
     * creating extra paddle and deleting brick.
     * @param gameObject1 object 1
     * @param gameObject2 object 2
     */
    @Override
    public void onCollision(GameObject gameObject1, GameObject gameObject2) {
        this.brickerGameManager.createExtraPaddle();
        System.out.println("collision with extra puddle brick detected");
        if(isFirst) {
            brickerGameManager.removeBrick((Brick) gameObject1);
        }
    }
}