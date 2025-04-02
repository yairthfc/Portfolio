package bricker.gameobjects;

import danogl.GameObject;
import danogl.collisions.Collision;
import danogl.gui.rendering.Renderable;
import danogl.util.Vector2;

/**
 * a class of heart object.
 */
public class Heart extends GameObject {
    private boolean dead = false;
    private String tagName;

    /**
     * Construct a new GameObject instance.
     *
     * @param topLeftCorner Position of the object, in window coordinates (pixels).
     *                      Note that (0,0) is the top-left corner of the window.
     * @param dimensions    Width and height in window coordinates.
     * @param renderable    The renderable representing the object. Can be null, in which case
     */

    public Heart(Vector2 topLeftCorner, Vector2 dimensions, Renderable renderable) {
        super(topLeftCorner, dimensions, renderable);
    }

    /**
     * changes tag name.
     * @param tagName string of tag name
     */
    public void changeTagName(String tagName) {
        this.tagName = tagName;
    }

    /**
     * if its a falling heart make it collidable, and delete it in case of collision.
     * @param other     The GameObject with which a collision occurred.
     * @param collision Information regarding this collision.
     *                  A reasonable elastic behavior can be achieved with:
     *                  setVelocity(getVelocity().flipped(collision.getNormal()));
     */
    @Override
    public void onCollisionEnter(GameObject other, Collision collision) {
        if (other.getTag()==this.tagName) {
            super.onCollisionEnter(other, collision);
            if (shouldCollideWith(other)) {
                dead = true;
            }
        }
    }

    /**
     * should collide with a certain object.
     * @param other The other GameObject.
     * @return boolean
     */
    @Override
    public boolean shouldCollideWith(GameObject other)
    {
      return super.shouldCollideWith(other);
    }

    /**
     * is the heart dead?
     * @return boolean
     */
    public boolean isDead() {
        return dead;
    }

}