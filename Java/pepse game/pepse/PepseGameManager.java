package pepse;
import danogl.GameManager;
import danogl.GameObject;
import danogl.collisions.Layer;
import danogl.components.Component;
import danogl.components.CoordinateSpace;
import danogl.components.Transition;
import danogl.gui.ImageReader;
import danogl.gui.SoundReader;
import danogl.gui.UserInputListener;
import danogl.gui.WindowController;
import danogl.gui.rendering.Camera;
import danogl.gui.rendering.RectangleRenderable;
import danogl.gui.rendering.TextRenderable;
import danogl.util.Vector2;
import pepse.util.ColorSupplier;
import pepse.world.Avatar;
import pepse.world.Block;
import pepse.world.Sky;
import pepse.world.Terrain;
import pepse.world.daynight.*;
import pepse.world.trees.*;

import java.awt.*;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

/**
 * Manages the main game logic and initialization for the Pepse game.
 */
public class PepseGameManager extends GameManager {

    private static final Color RAIN_COLOR = new Color(0, 0, 255);//blue
    private List<Block> blocks = new ArrayList<>();//blocks of the terrain
    private List<Tree> trees = new ArrayList<>(); // trees in the game
    private List<GameObject> cloud = new ArrayList<>();//cloud in the game
    private Terrain terrain; //terrain of the game
    private Avatar avatar; //avatar of the game
    private GameObject energyBar;//energy bar of the avatar
    private Flora flora;//flora of the game
    private Camera camera;//camera of the game
    private float terrerianMaxX=1280;//max x position of the terrain
    private float terrerianMinX=0;//min x position of the terrain
    private float terrerianDif=750;//difference between max and min x position of the terrain
    private static final float deleteRange = 1800;//range to delete objects
    private static final float DROP_FADE_OUT_TIME = 1.0f; //time to fade out the drop
    private static final int DROP_IN_COL = 3;//number of drops in a column
    private static final int DROP_IN_ROW = 6;//number of drops in a row
    private static final int CYCLE_LEN = 30;//cycle length
    private static final int CLAUDE_CYCLE = 45;//cloud cycle
    private static final Vector2 ENERGY_BAR_POS =new Vector2(100, 20);//energy bar position
    private static final int ENERGY_TO_ADD = 10;//energy to add
    private static final Vector2 ENERGY_BAR_SIZE = new Vector2(10,10) ;//energy bar size
    private static final int FRAME_RATE = 240;//frame rate
    private static final Vector2 DROP_SIZE = new Vector2(10, 10);//drop size
    private static final int TERRAIN_SEED = 24;//terrain seed
    private static final int FLORA_SEED = 21;//flora seed
    private static final float AVATAR_WINDOW_MULT = 0.4f;//avatar window multiplier
    private static final int CAMERA_HEIGHT = 350;//camera height
    private static final int RANGE_TO_BUILD = 300;//range to build
    private static final double RAIN_CHANCE = 0.4;//rain chance
    private static final int ENERGY_BAR_X_DIF = 400;//energy bar x difference
    private static final int DROP_Y_DIV = 5;//drop y division
    private static final int DROP_X_DIV = 2;//drop x division

    /**
     * Initializes the game, setting up the game objects and environment.
     *
     * @param imageReader      Reader for loading images.
     * @param soundReader      Reader for loading sounds.
     * @param inputListener    Listener for user input.
     * @param windowController Controller for the game window.
     */
    @Override
    public void initializeGame(ImageReader imageReader, SoundReader soundReader,
                               UserInputListener inputListener, WindowController windowController) {
        super.initializeGame(imageReader, soundReader, inputListener, windowController);
        windowController.setTargetFramerate(FRAME_RATE);
        // create sky
        GameObject createSky = Sky.create(windowController.getWindowDimensions());
        gameObjects().addGameObject(createSky, Layer.BACKGROUND);

        // create ground
        Terrain terrain = new Terrain(windowController.getWindowDimensions(), TERRAIN_SEED);
        this.terrain = terrain;
        List<Block> blocks = terrain.createInRange(0, (int) windowController.getWindowDimensions().x());
        for (Block block : blocks) {
            gameObjects().addGameObject(block, Layer.STATIC_OBJECTS);
        }

        // create night
        GameObject night = Night.create(windowController.getWindowDimensions(),CYCLE_LEN);
        gameObjects().addGameObject(night, Layer.DEFAULT);

        // create sun
        GameObject sun = Sun.create(windowController.getWindowDimensions(), CYCLE_LEN);
        gameObjects().addGameObject(sun, Layer.BACKGROUND);

        //create Halo
        GameObject sunHalo = SunHalo.create(sun);
        gameObjects().addGameObject(sunHalo, Layer.BACKGROUND);
        Component comp = (deltaTime) -> sunHalo.setCenter(sun.getCenter());
        sunHalo.addComponent(comp::update); //observer

        // create cloud
        this.cloud = Cloud.create(windowController.getWindowDimensions(), CLAUDE_CYCLE);
        for (int i = 0; i < cloud.size(); i++) {
            gameObjects().addGameObject(cloud.get(i), Layer.BACKGROUND);
        }

        // create avatar
        Vector2 avatarPosition = new Vector2(windowController.getWindowDimensions().mult(AVATAR_WINDOW_MULT));
        this.avatar = new Avatar(avatarPosition, inputListener, imageReader);
        gameObjects().addGameObject(avatar, Layer.DEFAULT);


        // create camera

        this.camera = new Camera(avatar, Vector2.ZERO,
                windowController.getWindowDimensions(), windowController.getWindowDimensions());
        setCamera(this.camera);
        //gameObjects().addGameObject(camera, Layer.UI);

        // create energy bar
        createEnergyBar();
        avatar.setEnergyChangeCallback(this::updateEnergyDisplay);

        // create trees
        Flora flora = new Flora(terrain::groundHeightAt, FLORA_SEED, windowController.getWindowDimensions());
        this.flora = flora;
        List<Tree> trees = flora.createInRange(0, (int) windowController.getWindowDimensions().x());
        for (Tree tree : trees) {
            gameObjects().addGameObject(tree, Layer.DEFAULT);
            for (Leaf leaf : tree.getLeafs()) {
                gameObjects().addGameObject(leaf, Layer.FOREGROUND);
            }
            for (Fruit fruit : tree.getFruits()) {
                gameObjects().addGameObject(fruit, Layer.DEFAULT);
            }
        }

    }

    /**
     * Creates the energy bar for the avatar.
     */
    private void createEnergyBar() {
        TextRenderable energyText = new TextRenderable( (int) avatar.getEnergy()+"%");
        energyBar = new GameObject(ENERGY_BAR_SIZE, ENERGY_BAR_POS, energyText);
        gameObjects().addGameObject(energyBar, Layer.UI);

    }

    /**
     * Updates the energy display based on the avatar's energy level.
     *
     * @param newEnergy The new energy level of the avatar.
     */
    private void updateEnergyDisplay(float newEnergy) {
        ((TextRenderable) energyBar.renderer().getRenderable()).setString("Energy: " + (int) newEnergy);
    }

    /**
     * Updates the game state, including the avatar's position and the game world.
     *
     * @param deltaTime The time elapsed since the last update.
     */
    @Override
    public void update(float deltaTime) {
    super.update(deltaTime);
    if (this.avatar != null) {
        if(this.avatar.returnIsJumping()){
            createRain();
        }
        //System.out.println(this.avatar.getCenter().x());
        Vector2 newCenter = new Vector2(this.avatar.getCenter().x(), CAMERA_HEIGHT);
        this.camera.setCenter(newCenter);
        this.energyBar.setCenter(new Vector2(this.avatar.getCenter().x() - ENERGY_BAR_X_DIF,
                energyBar.getCenter().y()));
        if (this.avatar.getCenter().x() > terrerianMaxX - terrerianDif) {
            createMap((int) terrerianMaxX, (int) (terrerianMaxX + RANGE_TO_BUILD));
            terrerianMaxX += RANGE_TO_BUILD;
            if (terrerianMaxX - terrerianMinX > deleteRange) {
                deleteObjectsFromLeft();
            }
        }
        if (this.avatar.getCenter().x() < terrerianMinX + terrerianDif) {
            createMap((int)(terrerianMinX-RANGE_TO_BUILD), (int) (terrerianMinX));
            terrerianMinX -= RANGE_TO_BUILD;
            if (terrerianMaxX - terrerianMinX > deleteRange) {
                deleteObjectsFromRight();}
        }

    }

}
    /**
     * Creates rain drops in the game world.
     */
    private void createRain(){
        int rainRow=new Random().nextInt(DROP_IN_ROW) + 1 ;
        int rainColumn=new Random().nextInt(DROP_IN_COL) + 1 ;
        for (int i = 0; i<rainRow; i++){
            for (int j = 0; j<rainColumn; j++){
                if(Math.random()<RAIN_CHANCE){
                    continue;
                }
                Vector2 cloudPosition = cloud.get(0).getCenter();
                Vector2 dropPosition = new Vector2(
                        cloudPosition.x() + i * Block.SIZE+cloud.size()/DROP_X_DIV,
                        cloudPosition.y() + j * Block.SIZE+cloud.size()*DROP_Y_DIV
                );
                Drop drop = new Drop(
                        dropPosition,
                        DROP_SIZE,
                        new RectangleRenderable(ColorSupplier.approximateMonoColor(RAIN_COLOR))
                );
                drop.setCoordinateSpace(cloud.get(0).getCoordinateSpace());
                drop.fadeOut(DROP_FADE_OUT_TIME, () -> gameObjects()
                        .removeGameObject(drop, Layer.BACKGROUND));

                gameObjects().addGameObject(drop, Layer.BACKGROUND);

            }
        }

    }

    /**
     * Creates the game map in the specified range.
     *
     * @param min The minimum x-coordinate of the range.
     * @param max The maximum x-coordinate of the range.
     */
    private void createMap(int min, int max) {

        List<Block> newBlocks = this.terrain.createInRange(min, max);
        for (Block block : newBlocks) {
            gameObjects().addGameObject(block, Layer.STATIC_OBJECTS);
            blocks.add(block);
        }
        List<Tree> newTrees = this.flora.createInRange(min, max);
        for (Tree tree : newTrees) {
            gameObjects().addGameObject(tree, Layer.DEFAULT);
            trees.add(tree);
            for (Leaf leaf : tree.getLeafs()) {
                gameObjects().addGameObject(leaf, Layer.FOREGROUND);
            }
            for (Fruit fruit : tree.getFruits()) {
                gameObjects().addGameObject(fruit, Layer.DEFAULT);
            }
        }
    }
    /**
     * Deletes objects from the left side of the game world.
     */
    private void deleteObjectsFromLeft() {
        while (!blocks.isEmpty() && blocks.get(0).getCenter().x() < terrerianMinX) {
            gameObjects().removeGameObject(blocks.remove(0), Layer.STATIC_OBJECTS);
        }
        while (!trees.isEmpty() && trees.get(0).getCenter().x() < terrerianMinX) {
            Tree tree = trees.remove(0);
            gameObjects().removeGameObject(tree, Layer.DEFAULT);
            for (Leaf leaf : tree.getLeafs()) {
                gameObjects().removeGameObject(leaf, Layer.FOREGROUND);
            }
            for (Fruit fruit : tree.getFruits()) {
                gameObjects().removeGameObject(fruit, Layer.DEFAULT);
            }
        }
    }

    /**
     * Deletes objects from the right side of the game world.
     */
    private void deleteObjectsFromRight() {
        while (!blocks.isEmpty() && blocks.get(blocks.size() - 1).getCenter().x() > terrerianMaxX) {
            gameObjects().removeGameObject(blocks.remove(blocks.size() - 1), Layer.STATIC_OBJECTS);
        }
        while (!trees.isEmpty() && trees.get(trees.size() - 1).getCenter().x() > terrerianMaxX) {
            Tree tree = trees.remove(trees.size() - 1);
            gameObjects().removeGameObject(tree, Layer.DEFAULT);
            for (Leaf leaf : tree.getLeafs()) {
                gameObjects().removeGameObject(leaf, Layer.FOREGROUND);
            }
            for (Fruit fruit : tree.getFruits()) {
                gameObjects().removeGameObject(fruit, Layer.DEFAULT);
            }
        }
    }


    /**
     * The main entry point for the game.
     *
     * @param args Command-line arguments.
     */
    public static void main(String[] args) {
        new PepseGameManager().run();
    }
}