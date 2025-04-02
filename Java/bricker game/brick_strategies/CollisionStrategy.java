package bricker.brick_strategies;

import danogl.GameObject;

/**
 * interface for collision strategy.
 */
public interface CollisionStrategy {
    /**
     * what happens on collision.
     * @param gameObject1 object 1
     * @param gameObject2 object 2
     */
    public void onCollision(GameObject gameObject1, GameObject gameObject2);
}
