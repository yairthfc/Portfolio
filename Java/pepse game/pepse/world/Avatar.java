package pepse.world;

import danogl.GameObject;
import danogl.collisions.Collision;
import danogl.collisions.Layer;
import danogl.gui.ImageReader;
import danogl.gui.UserInputListener;
import danogl.gui.rendering.AnimationRenderable;
import danogl.gui.rendering.Renderable;
import danogl.util.Vector2;

import java.awt.event.KeyEvent;

/**
 * Represents the player character in the game world.
 */
public class Avatar extends GameObject {
    private static final float VELOCITY_X = 400;//velocity of the avatar in the x direction
    private static final float VELOCITY_Y = -650;//velocity of the avatar in the y direction
    private static final float GRAVITY = 600;//gravity
    private static final float ENERGY_TO_JUMP = 10;//energy to jump
    private static final double MOVE_ENERGY = 0.5;//energy to move
    private static final double FRAME_TIME = 0.5;//frame time
    private static final Vector2 SRARTING_POSITION = new Vector2(50,50) ;//starting position
    private Vector2 topLeftCorner;//top left corner
    private UserInputListener inputListener;//input listener
    private ImageReader imageReader;//image reader
    private static final float maxEnergy = 100;//max energy
    private float energy;//energy
    private AnimationRenderable idleAnimationRenderable;//idle animation renderable
    private AnimationRenderable jumpAnimationRenderable;//jump animation renderable
    private AnimationRenderable runAnimationRenderable;//run animation renderable
    private EnergyChangeCallback energyChangeCallback;//energy change callback
    private Boolean isJumping = false;//is jumping

    /**
     * Constructs a new Avatar instance.
     *
     * @param topLeftCorner Position of the avatar, in window coordinates (pixels).
     * @param inputListener Listener for user input.
     * @param imageReader   Reader for loading images.
     */
    public Avatar(Vector2 topLeftCorner,
                  UserInputListener inputListener,
                  ImageReader imageReader){
        super(topLeftCorner, SRARTING_POSITION, null);
        this.topLeftCorner = topLeftCorner;
        this.inputListener = inputListener;
        this.imageReader = imageReader;
        idleAnimation();
        jumpAnimation();
        moveAnimation();
        this.energy = maxEnergy;
        transform().setAccelerationY(GRAVITY);
        physics().preventIntersectionsFromDirection(Vector2.ZERO);

    }

    /**
     * Controls the energy level of the avatar based on movement.
     *
     * @param movement The movement direction.
     */
    private void energyController(int movement){
        if (movement != 0){
            energy -= MOVE_ENERGY;
        }
        else {
            if (this.getVelocity().y() == 0){
                energy += 1;}

        }
        if (energy > maxEnergy){
            energy = maxEnergy;
        }
        if (energy < 0){
            energy = 0;
        }
        if (energyChangeCallback != null) {
            energyChangeCallback.onEnergyChange(this.energy);
        }
    }

    /**
     * Adds energy to the avatar.
     *
     * @param energy The amount of energy to add.
     */
    public void addEnergy(float energy){
        this.energy += energy;
        if (this.energy > maxEnergy){
            this.energy = maxEnergy;
        }
        if (energyChangeCallback != null) {
            energyChangeCallback.onEnergyChange(this.energy);
        }
    }


    /**
     * Handles collision with other game objects.
     *
     * @param other     The other game object.
     * @param collision The collision information.
     */
    @Override
    public void onCollisionEnter(GameObject other, Collision collision) {
        super.onCollisionEnter(other, collision);
        if(other.getTag().equals("block")){
            this.transform().setVelocityY(0);;
        }
    }

    /**
     * Initializes the idle animation for the avatar.
     */
    private void idleAnimation(){
        Renderable[] renderable ={this.imageReader.readImage("src/assets/idle_0.png",false),
                this.imageReader.readImage("src/assets/idle_1.png",false),
                this.imageReader.readImage("src/assets/idle_2.png",false),
                this.imageReader.readImage("src/assets/idle_3.png",false)};
        this.idleAnimationRenderable = new AnimationRenderable(renderable,FRAME_TIME );
    }

    /**
     * Initializes the jump animation for the avatar.
     */
   private void jumpAnimation(){
       Renderable[] renderable ={this.imageReader.readImage("src/assets/jump_0.png",false),
               this.imageReader.readImage("src/assets/jump_1.png",false),
               this.imageReader.readImage("src/assets/jump_2.png",false),
               this.imageReader.readImage("src/assets/jump_3.png",false)};
       this.jumpAnimationRenderable = new AnimationRenderable(renderable, FRAME_TIME);
    }

    /**
     * Initializes the move animation for the avatar.
     */
    private void moveAnimation(){
        Renderable[] renderable ={this.imageReader.readImage("src/assets/run_0.png",false),
                this.imageReader.readImage("src/assets/run_1.png",false),
                this.imageReader.readImage("src/assets/run_2.png",false),
                this.imageReader.readImage("src/assets/run_3.png",false),
                this.imageReader.readImage("src/assets/run_3.png",false),
                this.imageReader.readImage("src/assets/run_3.png",false)};
        this.runAnimationRenderable = new AnimationRenderable(renderable, FRAME_TIME);
    }

    /**
     * Controls the animation of the avatar based on its state.
     */
    private void animationConttroller()
    {
        float yVelocity= this.getVelocity().y();
        float xVelocity = this.getVelocity().x();
        this.renderer().setIsFlippedHorizontally(xVelocity<0);
        if (yVelocity!=0)
        {
            this.renderer().setRenderable(jumpAnimationRenderable);
            return;
        }
        if (xVelocity!=0)
        {
            this.renderer().setRenderable(runAnimationRenderable);

            return;
        }
        this.renderer().setRenderable(idleAnimationRenderable);
    }



    /**
     * Updates the avatar's state based on user input.
     *
     * @param deltaTime The time elapsed since the last update.
     */
    public void update(float deltaTime){
        super.update(deltaTime);
        int movement = 0;
        float velocityX = 0;
        //float velocityY = 0;
        if (inputListener.isKeyPressed('A')&& energy >0) {
          velocityX += -VELOCITY_X;
            movement-=1;
        }
        if (inputListener.isKeyPressed('D')&& energy >0) {
          velocityX += VELOCITY_X;
            movement+=1;
        }
        if (inputListener.isKeyPressed(KeyEvent.VK_SPACE)&& energy >= 10) {
            if (this.getVelocity().y() == 0){
            isJumping = true;
            energy -= ENERGY_TO_JUMP;
            this.transform().setVelocityY(VELOCITY_Y);
            }
        }

        energyController(movement);
        animationConttroller();

        this.transform().setVelocityX(velocityX);

    }

    /**
     * Returns whether the avatar is jumping.
     *
     * @return True if the avatar is jumping, false otherwise.
     */
    public boolean returnIsJumping(){
        if (isJumping){
            isJumping = false;
            return true;
        }
        return false;
    }


    /**
     * Sets the energy level of the avatar.
     *
     * @param energy The new energy level.
     */
    public void setEnergy(float energy) {
        this.energy = energy;
        if (energyChangeCallback != null) {
            energyChangeCallback.onEnergyChange(energy);
        }
    }
    /**
     * Returns the current energy level of the avatar.
     *
     * @return The current energy level.
     */
    public float getEnergy(){
        return this.energy;
    }

    /**
     * Sets the callback for energy changes.
     *
     * @param callback The callback to set.
     */
    public void setEnergyChangeCallback(EnergyChangeCallback callback) {
            this.energyChangeCallback = callback;
}

    /**
     * Callback interface for energy changes.
     */
    public interface EnergyChangeCallback {
        /**
         * Called when the energy level of the avatar changes.
         *
         * @param newEnergy The new energy level.
         */
        void onEnergyChange(float newEnergy);
    }

}
