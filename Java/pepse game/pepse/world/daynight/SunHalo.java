package pepse.world.daynight;

import danogl.GameObject;
import danogl.components.CoordinateSpace;
import danogl.gui.rendering.OvalRenderable;
import danogl.util.Vector2;

import java.awt.*;
/**
 * Represents the sun halo in the game world.
 */
public class SunHalo {
    private static final Vector2 SUN_HALO_SIZE = new Vector2(200, 200);//sun halo size
    private static final Color SUN_HALO_COLOR = new Color(255,255,0,20);//sun halo color
    private static final float SUN_HALO_DIV = 2;//sun halo division

    /**
     * Creates a sun halo effect in the game world.
     *
     * @param sun The sun GameObject around which the halo will be created.
     * @return A GameObject representing the sun halo.
     */
    public static GameObject create(GameObject sun){
        OvalRenderable ovalRenderable = new OvalRenderable(SUN_HALO_COLOR);
        GameObject sunHalo = new GameObject(new Vector2(sun.getCenter().x() - (SUN_HALO_SIZE.x()/SUN_HALO_DIV)
                , sun.getCenter().y() - (SUN_HALO_SIZE.x()/SUN_HALO_DIV)),SUN_HALO_SIZE, ovalRenderable);
        sunHalo.setCoordinateSpace(CoordinateSpace.CAMERA_COORDINATES);
        sunHalo.setTag("sunHalo");
        return sunHalo;
    }
}
