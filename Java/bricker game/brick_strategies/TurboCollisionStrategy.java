package bricker.brick_strategies;

import danogl.GameObject;
import bricker.gameobjects.Brick;
import bricker.main.BrickerGameManager;

import java.util.Objects;

/**
 * turbo collision strategy that changes the behavior of the main ball
 */
public class TurboCollisionStrategy implements CollisionStrategy {
    private boolean isFirst; //is it the first strategy
    protected final BrickerGameManager brickerGameManager; //game manager
    private final static String mainBall = "mainBall"; //string for ball mode

    /**
     * constructor
     * @param brickerGameManager game manager
     * @param isFirst is it first
     */
    public TurboCollisionStrategy(BrickerGameManager brickerGameManager, boolean isFirst) {
        this.brickerGameManager = brickerGameManager;
        this.isFirst = isFirst;
    }

    /**
     * changes the ball mode and deletes the brick on collision.
     * @param gameObject1 object 1
     * @param gameObject2 object 2
     */
    @Override
    public void onCollision(GameObject gameObject1, GameObject gameObject2) {
        if(Objects.equals(gameObject2.getTag(), mainBall)){
            this.brickerGameManager.ballMode("Turbo");
        }
        System.out.println("collision with turbo brick detected");
        if(isFirst) {
            this.brickerGameManager.removeBrick((Brick) gameObject1);
        }
    }
}
