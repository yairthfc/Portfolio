import danogl.GameManager;
import danogl.GameObject;
import danogl.collisions.Collision;
import danogl.collisions.Layer;
import danogl.components.GameObjectPhysics;
import danogl.components.ScheduledTask;
import danogl.components.SwitchComponent;
import danogl.components.Transition;
import danogl.components.movement_schemes.DirectionalMovementScheme;
import danogl.components.movement_schemes.DragMovementScheme;
import danogl.components.movement_schemes.PlatformerMovementScheme;
import danogl.components.movement_schemes.SteeringMovementScheme;
import danogl.components.movement_schemes.movement_directing.CommonMovementActions;
import danogl.components.movement_schemes.movement_directing.KeyboardMovementDirector;
import danogl.gui.ImageReader;
import danogl.gui.SoundReader;
import danogl.gui.UserInputListener;
import danogl.gui.WindowController;
import danogl.gui.mouse.MouseButton;
import danogl.gui.rendering.OvalRenderable;
import danogl.gui.rendering.RectangleRenderable;
import danogl.gui.rendering.SwitchRenderable;
import danogl.util.Border;
import danogl.util.Vector2;

import java.awt.*;
import java.awt.event.KeyEvent;
import java.util.List;

/**
 * The avatar (which is a small square) has 4 modes:
 * <br>Normally, it is a standard platformer, moving with left and right and jumping with up.
 * <br>When in water, it can swim in all directions using the arrow keys.
 * <br>While in the air (not touching land or water) and as long as the space key is pressed,
 * it flies in constant velocity, with left and right keys steering it.
 * <br>When pressed using the mouse cursor, it can be dragged around.
 * <br>The avatar changes between 4 colors, corresponding to the state it is currently in.
 *
 * <br>The example mainly shows the use of three MovementSchemes. It also uses
 * the SwitchComponent and SwitchRenderable classes. In creating the waves it also
 * shows an example of Transitions.
 * @author Dan Nirel
 */
public class AirEarthWater extends GameManager {
    public static void main(String[] args) {
        new AirEarthWater().run();
    }

    @Override
    public void initializeGame(ImageReader imageReader, SoundReader soundReader, UserInputListener inputListener, WindowController windowController) {
        super.initializeGame(imageReader, soundReader, inputListener, windowController);

        var dimensions = windowController.getWindowDimensions();

        windowController.setMouseCursor(new OvalRenderable(Color.BLACK), Vector2.ONES.mult(7), Vector2.ZERO);

        //add borders
        Border.addCompleteFrame(dimensions, 0, null, gameObjects(), Layer.STATIC_OBJECTS);

        //add avatar
        gameObjects().addGameObject(new FlyerAvatar(dimensions, inputListener));

        //init sky background
        gameObjects().addGameObject(new GameObject(
                Vector2.ZERO, dimensions, new RectangleRenderable(Color.CYAN)), Layer.BACKGROUND);

        initGround(dimensions);
        initWater(dimensions);
    }

    private void initGround(Vector2 dimensions) {
        for (int i = 0; i < 2; i++) {
            var earth =
                    new GameObject(Vector2.of(i * dimensions.x() * 2f / 3, dimensions.y() * 2f / 3),
                            dimensions.mult(1 / 3f),
                            new RectangleRenderable(Color.ORANGE));
            earth.physics().setMass(GameObjectPhysics.IMMOVABLE_MASS);
            earth.physics().preventIntersectionsFromDirection(Vector2.ZERO);
            gameObjects().addGameObject(earth, Layer.STATIC_OBJECTS);
        }
    }

    private void initWater(Vector2 dimensions) {
        var water = new GameObject(
                Vector2.of(dimensions.x() / 3, dimensions.y() * 2f / 3+20),
                dimensions.mult(1 / 3f),
                new RectangleRenderable(Color.BLUE));
        water.setTag("water");
        water.renderer().setOpaqueness(.8f);
        gameObjects().addGameObject(water);

        //init waves
        final int waveCount = 20;
        float waveWidth = water.getDimensions().x()/waveCount;

        for(int i = 0 ; i < waveCount ; i++) {
            var wave = new GameObject(
                    water.getTopLeftCorner().add(Vector2.RIGHT.mult(i*waveWidth)),
                    Vector2.ONES.mult(waveWidth), water.renderer().getRenderable());
            new ScheduledTask(wave, i/10f, false,
                    ()-> {
                        new Transition<Float>(
                                wave,
                                height -> wave.transform().setCenterY(water.getTopLeftCorner().y() + height),
                                -10f, 10f, Transition.CUBIC_INTERPOLATOR_FLOAT,
                                .75f, Transition.TransitionType.TRANSITION_BACK_AND_FORTH, null);
                        new Transition<Float>(
                                wave, wave.renderer()::setOpaqueness,
                                .1f, .4f, Transition.LINEAR_INTERPOLATOR_FLOAT, .75f,
                                Transition.TransitionType.TRANSITION_BACK_AND_FORTH, null);
                    }
            );
            gameObjects().addGameObject(wave, Layer.FOREGROUND);
        }
    }
}

class FlyerAvatar extends GameObject {
    private static final Color AIR_COLOR = Color.WHITE;
    private static final Color WATER_COLOR = Color.GREEN;
    private static final Color EARTH_COLOR = Color.GRAY;
    private static final Object FLIGHT_VELOCITY = 1.5f;
    private static final Color DRAG_COLOR = Color.YELLOW;
    private static final MouseButton DRAG_BUTTON = MouseButton.LEFT_BUTTON;
    private final UserInputListener inputListener;
    private SteeringMovementScheme steeringScheme;
    private String currentlyOn = "earth";
    private DragMovementScheme dragController;

    public FlyerAvatar(Vector2 widowDimensions, UserInputListener inputListener) {
        super(
                widowDimensions.multX(1/6f).multY(.3f),
                Vector2.of(30, 50), null);
        this.inputListener = inputListener;

        transform().setAccelerationY(1000);
        physics().preventIntersectionsFromDirection(Vector2.ZERO);

        setMovementScheme();

        //change render color based on state
        renderer().setRenderable(new SwitchRenderable(
                List.of(
                        ()->dragController.isDragging(),
                        ()->currentlyOn.equals("air"),
                        ()->currentlyOn.equals("water")
                ),
                List.of(
                        new RectangleRenderable(DRAG_COLOR),
                        new RectangleRenderable(AIR_COLOR),
                        new RectangleRenderable(WATER_COLOR)
                ),
                new RectangleRenderable(EARTH_COLOR)));
    }

    private void setMovementScheme() {
        var moveDirector = inputListener.keyboardMovementDirector();
        //set the up arrow to signal jumping (instead of space)
        moveDirector.setKeyboardKey(KeyboardMovementDirector.INPUT_JUMP, KeyEvent.VK_UP);
        //make this MovementDirector always return the constant value when queried
        //on forwards/backwards movement. Since that value is queried, in the scope of this
        //example, only by the SteeringMovementScheme, this makes the avatar constantly fly
        //forwards when flying. Without this line, the flying avatar would only move
        //forwards when the up button is pressed.
        moveDirector.registerAction(CommonMovementActions.FORWARDS_BACKWARDS_FLOAT, ()->FLIGHT_VELOCITY);

        steeringScheme =
                new SteeringMovementScheme(this, moveDirector, this.renderer());

        dragController = new DragMovementScheme(
                this, inputListener.mouseMovementDirector(null));
        addComponent(dragController);

        addComponent(new SwitchComponent(
                List.of(
                        ()->currentlyOn.equals("air"),
                        ()->currentlyOn.equals("water")
                ),
                List.of(
                        steeringScheme,
                        new DirectionalMovementScheme(this, moveDirector)
                ),
                new PlatformerMovementScheme(this, moveDirector),
                true)
        );
    }

    @Override
    public void onCollisionStay(GameObject other, Collision collision) {
        super.onCollisionStay(other, collision);
        if(other.getTag().equals("water"))
            currentlyOn = "water";
    }

    @Override
    public void update(float deltaTime) {
        super.update(deltaTime);

        if(!currentlyOn.equals("water") && inputListener.isKeyPressed(KeyEvent.VK_SPACE)) {
            if(getVelocity().y() != 0)
                currentlyOn = "air";
        }
        else {
            currentlyOn = "earth";
            renderer().setRenderableAngle(0);
            steeringScheme.setForwardsDir(Vector2.UP);
        }
    }
}
