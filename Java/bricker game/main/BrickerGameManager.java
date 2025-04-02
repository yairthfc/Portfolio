package bricker.main;

import bricker.brick_strategies.*;
import danogl.GameManager;
import danogl.GameObject;
import danogl.collisions.Layer;
import danogl.gui.*;
import danogl.gui.rendering.Renderable;
import danogl.gui.rendering.TextRenderable;
import danogl.util.Vector2;
import bricker.gameobjects.Ball;
import bricker.gameobjects.Brick;
import bricker.gameobjects.Heart;
import bricker.gameobjects.Paddle;

import java.awt.*;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Iterator;
import java.util.Random;

/**
 * class BrickerGameManager implements a game of bricker.
 */
public class BrickerGameManager extends GameManager {
    // Constants: Define fixed values used throughout the game logic.
    private static final int DEFAULT_ROWS = 7; // Default number of brick rows.
    private static final int DEFAULT_COLS = 8; // Default number of brick columns.
    private static final Vector2 HEART_DIMENSIONS = new Vector2(10, 10); // Dimensions of heart icons.
    private static final Vector2 NUMBER_DIMENSIONS = new Vector2(10, 10); // Dimensions for displayed numbers.
    private static final int BRICK_START_POSITION = 6; // Initial brick position offset.
    private static final int ALL_STRATEGIES = 10; // Total number of brick strategies.
    private static final int SPECIAL_STRATEGIES = 5; // Number of special strategies (e.g., explosive bricks).
    private static final int SPECIAL_STRATEGIES_WITHOUT_DOUBLE = 4; // Special strategies excluding double effects.
    private static final Vector2 PADDLE_SIZE = new Vector2(100, 15); // Dimensions of the paddle.
    private static final Vector2 MAIN_BALL_SIZE = new Vector2(20, 20); // Dimensions of the main ball.
    private static final Vector2 PUCK_BALL_SIZE = new Vector2(15, 15); // Dimensions of puck balls.
    private static final Vector2 HEART_VELOCITY = new Vector2(0f, 100f); // Falling velocity of hearts.
    private static final int MAX_TURBO_COLLISION = 6; // Maximum collisions allowed in turbo mode.
    private static final String BALL_TAG = "mainBall"; // Tag identifier for the main ball.
    private static final String PADDLE_TAG = "mainPaddle"; // Tag identifier for the main paddle.
    private static final String LOSE_PROMPT = "You lose! Play again?"; // Message shown on losing.
    private static final String WIN_PROMPT = "You win! Play again?"; // Message shown on winning.
    private static final int BRICK_LENGTH = 15; // Length of a single brick in game units.
    private static final float BALL_SPEED = 175; // Default ball movement speed.
    private static final int HEART_STARTING_X_POSITION = 15;//Default starting x position for heart.
    private static final int HEART_Y_POSITION = 20;//Default starting y position for heart.
    private static final float TURBO_SIZE = 1.4f; //Control the size in turbo mode.
    private int ballCollisionCounter;//count the ball collisions


    // Game Objects: Hold references to key game components and objects.
    private final GameObject[] heartNumbersArray; // Array to track numbers for heart indicators.
    private Ball ball; // The main game ball object.
    private Paddle paddle; // Main paddle controlled by the player.
    private Paddle extraPaddle; // An additional paddle (e.g., for special game modes).
    private Heart[] hearts; // Array of hearts indicating lives left.
    private ArrayList<Ball> puckList; // List to manage all puck balls in play.
    private ArrayList<Heart> heartsList; // List of hearts currently active in the game.
    private GameObject number; // Game object representing a displayed number.

    // Dimensions and Positions: Store window dimensions and dynamic positioning data.
    private Vector2 windowDimensions; // Dimensions of the game window.
    private Vector2 bricksRowCol; // Number of rows and columns for bricks.
    private Vector2 numberPosition; // Position of the number display object.
    private float widthForBricks; // Width allocation for brick placement.
    private float heartsYStartPosition; // Y-axis starting position for hearts.
    private float heartsXStartPosition; // X-axis starting position for hearts.

    // Other Game Components: Auxiliary utilities and variables for game management.
    private WindowController windowController; // Controller for managing window interactions.
    private ImageReader imageReader; // Utility for loading and managing images.
    private SoundReader soundReader; // Utility for loading and managing sounds.
    private UserInputListener inputListener; // Listener for capturing player input.
    private int numOfStrikesLeft; // Tracks the number of strikes the player has left.
    private int numOfBricks; // Tracks the number of bricks remaining in the game.
    private boolean ballInTurboMode = false; // Flag to indicate if the ball is in turbo mode.
    private boolean canAddPaddle = true; // Flag to indicate if an extra paddle can be added.


    /**
     * Constructs a new BrickerGameManager instance.
     *
     * @param windowTitle Title of the game window.
     * @param windowDimensions Dimensions of the game window.
     * @param bricksRowCol Rows and columns of bricks in the game.
     * @param maxHearts Maximum number of lives (hearts).
     */
    public BrickerGameManager(String windowTitle, Vector2 windowDimensions, Vector2 bricksRowCol, int maxHearts) {
        super(windowTitle, windowDimensions);
        this.bricksRowCol = bricksRowCol;
        hearts = new Heart[maxHearts];
        //int puckListSize = (int)(bricksRowCol.y()*bricksRowCol.x());
        this.puckList = new ArrayList<Ball>();
        this.heartNumbersArray = new GameObject[maxHearts];
        this.heartsList = new ArrayList<Heart>();
    }


    /**
     * Initializes the game, setting up all required components like balls, bricks,
     * paddle, and other elements.
     *
     * @param imageReader Image loader to retrieve visual assets.
     * @param soundReader Sound loader to retrieve sound effects.
     * @param inputListener Listener for user input events.
     * @param windowController Controller for window interactions.
     */
    @Override
    public void initializeGame(ImageReader imageReader, SoundReader soundReader, UserInputListener inputListener, WindowController windowController) {
        super.initializeGame(imageReader, soundReader, inputListener, windowController);
        initializeFeatures(imageReader, soundReader, inputListener, windowController);

        //initialize number images
        initializeHeartsNumbers();

        // creating ball
        createBall(imageReader, soundReader, windowDimensions);

        //creating paddle
        createPaddle(imageReader, inputListener, windowDimensions);

        // crearting walls
        createWalls(windowDimensions);

        // creating background
        createBackground(imageReader, windowDimensions);

        // create bricks
        createBricks(imageReader, soundReader, windowDimensions);

        //create hearts
        createHearts(imageReader);

        //control collisions
        layerControl();
    }

    private void initializeFeatures(ImageReader imageReader, SoundReader soundReader, UserInputListener inputListener, WindowController windowController) {
        this.windowDimensions = windowController.getWindowDimensions();
        this.numOfBricks = (int) (bricksRowCol.x() * bricksRowCol.y());
        this.widthForBricks = windowDimensions.x() - 12;
        this.heartsXStartPosition = HEART_STARTING_X_POSITION;
        this.heartsYStartPosition = windowDimensions.y() - HEART_Y_POSITION;
        this.windowController = windowController;
        this.imageReader = imageReader;
        this.numOfStrikesLeft = 3;
        this.numberPosition = new Vector2(3, windowDimensions.y() - HEART_Y_POSITION);
        this.soundReader = soundReader;
        this.inputListener = inputListener;
        this.ballInTurboMode = false;
        this.canAddPaddle = true;

    }

    private void initializeHeartsNumbers() {
        for (int i = 1; i < heartNumbersArray.length + 1; i++) {
            TextRenderable scoreImage = new TextRenderable("Score");
            String num = String.valueOf(i);
            scoreImage.setString(num);
            if(i == 1){
                scoreImage.setColor(Color.RED);
            }
            if(i == 2){
                scoreImage.setColor(Color.YELLOW);
            }
            else{
                scoreImage.setColor(Color.GREEN);
            }
            GameObject number = new GameObject(numberPosition, NUMBER_DIMENSIONS,scoreImage);
            heartNumbersArray[i-1] = number;
        }
        gameObjects().addGameObject(heartNumbersArray[numOfStrikesLeft - 1],Layer.UI);
    }

    private void createHearts(ImageReader imageReader) {

        Renderable heartImage = imageReader.readImage("assets/heart.png", true);
        for (int i = 0; i < numOfStrikesLeft; i++) {
            createSingleHeart(heartImage, i);
        }
    }

    private void createSingleHeart(Renderable heartImage, int location) {
        Heart heart = new Heart(new Vector2(heartsXStartPosition ,heartsYStartPosition),new Vector2(HEART_DIMENSIONS), heartImage);
        gameObjects().addGameObject(heart, Layer.UI);
        hearts[location] = heart;
        heartsXStartPosition += HEART_DIMENSIONS.x() + 2;
    }


    /**
     * Updates the game state each frame.
     *
     * @param deltaTime Time elapsed since the last frame.
     */
    @Override
    public void update(float deltaTime) {
        super.update(deltaTime);
        checkLose();
        checkWin();
        if(ballInTurboMode)
        {
            ballMode("Regular");
        }
        if(!canAddPaddle)
        {
            deleteExtraPuddle(extraPaddle);
        }
        if (!puckList.isEmpty()){
            Iterator<Ball> puckIterator = puckList.iterator();
            while(puckIterator.hasNext()) {
                Ball puck = puckIterator.next();
                float puckHeight = puck.getCenter().y();
                if (puckHeight>windowDimensions.y())
                {
                    //System.out.println("delete puck");
                    puckIterator.remove();
                    gameObjects().removeGameObject(puck);

                }
            }
        }
        if (!heartsList.isEmpty()){
            deleteHeart();
        }
    }

    private void checkWin() {
        if(numOfBricks == 0){
            if(!windowController.openYesNoDialog(WIN_PROMPT)){
                windowController.closeWindow();
            }
            else{
                windowController.resetGame();
            }
        }
    }

    private void layerControl(){
        if ( ! this.gameObjects().layers().doLayersCollide(Layer.DEFAULT,Layer.FOREGROUND)){
            System.out.println("not collide 1");
        this.gameObjects().layers().shouldLayersCollide(Layer.DEFAULT,Layer.FOREGROUND,true);}
        if ( ! this.gameObjects().layers().doLayersCollide(Layer.STATIC_OBJECTS,Layer.FOREGROUND)){
            System.out.println("not collide 2");
            this.gameObjects().layers().shouldLayersCollide(Layer.STATIC_OBJECTS,Layer.FOREGROUND,true);
        }

       this.gameObjects().layers().shouldLayersCollide(Layer.DEFAULT,Layer.STATIC_OBJECTS,false);

    }

    private void checkLose(){
        float ballHeight = ball.getCenter().y();
        if(ballHeight > windowDimensions.y()){
            if(numOfStrikesLeft > 1){
                deleteOrAddHeart("delete");
                ball.setCenter(windowDimensions.mult(0.5f));
            }
            else{
                if(!windowController.openYesNoDialog(LOSE_PROMPT)){
                    windowController.closeWindow();
                }
                else{
                    windowController.resetGame();
                }
            }
        }
    }

    private void deleteOrAddHeart(String action){
        switch (action) {
            case "delete":
                gameObjects().removeGameObject(hearts[numOfStrikesLeft - 1], Layer.UI);
                hearts[numOfStrikesLeft - 1] = null;
                heartsXStartPosition -= HEART_DIMENSIONS.x() +2;
                numOfStrikesLeft--;
                //change number
                gameObjects().removeGameObject(heartNumbersArray[numOfStrikesLeft],Layer.UI);
                gameObjects().addGameObject(heartNumbersArray[numOfStrikesLeft - 1],Layer.UI);
                break;
            case "add":
                System.out.println("1");
                Renderable heartImage = imageReader.readImage("assets/heart.png", true);
                System.out.println("2");
                createSingleHeart(heartImage, numOfStrikesLeft);
                System.out.println("3");
                //change number
                System.out.println("4");
                gameObjects().addGameObject(heartNumbersArray[numOfStrikesLeft],Layer.UI);
                gameObjects().removeGameObject(heartNumbersArray[numOfStrikesLeft - 1],Layer.UI);
                System.out.println("5");
                numOfStrikesLeft++;
                System.out.println("6");
                break;
        }
    }

    private void createBricks(ImageReader imageReader, SoundReader soundReader, Vector2 windowDimensions) {
        Renderable brickImage = imageReader.readImage("assets/brick.png",false);

        float corXPosition = BRICK_START_POSITION;
        float corYPosition = BRICK_START_POSITION;
        float brickWidth = (widthForBricks - bricksRowCol.y() + 1) / bricksRowCol.y();


        for (int i = 0; i < bricksRowCol.x(); i++) {
            for (int j = 0; j < bricksRowCol.y(); j++) {

                Brick brick = null;
                brick = getBrick(corXPosition, corYPosition, brickWidth, brickImage);
                gameObjects().addGameObject(brick);
                corXPosition += brickWidth + 1;
            }
            corXPosition = BRICK_START_POSITION;
            corYPosition += BRICK_LENGTH + 1;
        }
    }

    private Brick getBrick(float corXPosition, float corYPosition, float brickWidth, Renderable brickImage) {
        Brick brick = null;
        String collisionStrategyString =  getCollisionStrategy(ALL_STRATEGIES);
        boolean twoDoubleCollision = false;
        switch (collisionStrategyString) {
            case "doubleCollisionStrategy":
                String stringStrategy1 = getCollisionStrategy(SPECIAL_STRATEGIES);
                String stringStrategy2 = getCollisionStrategy(SPECIAL_STRATEGIES);
                if ((!stringStrategy1.equals("doubleCollisionStrategy")) && (!stringStrategy2.equals("doubleCollisionStrategy"))) {
                    brick = new Brick(new Vector2(corXPosition, corYPosition), new Vector2(brickWidth, BRICK_LENGTH), brickImage, getStrategyByString(stringStrategy1,true), getStrategyByString(stringStrategy2,false));
                    break;
                }
                else{
                    if(stringStrategy1.equals("doubleCollisionStrategy")){
                        brick = new Brick(new Vector2(corXPosition, corYPosition), new Vector2(brickWidth, BRICK_LENGTH), brickImage, getStrategyByString(stringStrategy2,true), getStrategyByString(getCollisionStrategy(SPECIAL_STRATEGIES_WITHOUT_DOUBLE),false), getStrategyByString(getCollisionStrategy(SPECIAL_STRATEGIES_WITHOUT_DOUBLE),false));
                    }
                    if(stringStrategy2.equals("doubleCollisionStrategy")){
                        brick = new Brick(new Vector2(corXPosition, corYPosition), new Vector2(brickWidth, BRICK_LENGTH), brickImage, getStrategyByString(stringStrategy1,true), getStrategyByString(getCollisionStrategy(SPECIAL_STRATEGIES_WITHOUT_DOUBLE),false), getStrategyByString(getCollisionStrategy(SPECIAL_STRATEGIES_WITHOUT_DOUBLE),false));
                    }
                    if((stringStrategy1.equals("doubleCollisionStrategy")) && (stringStrategy2.equals("doubleCollisionStrategy"))){
                        brick = new Brick(new Vector2(corXPosition, corYPosition), new Vector2(brickWidth, BRICK_LENGTH), brickImage, getStrategyByString(getCollisionStrategy(SPECIAL_STRATEGIES_WITHOUT_DOUBLE),true), getStrategyByString(getCollisionStrategy(SPECIAL_STRATEGIES_WITHOUT_DOUBLE),false),getStrategyByString(getCollisionStrategy(SPECIAL_STRATEGIES_WITHOUT_DOUBLE),false));
                    }
                }
            default:
                CollisionStrategy collisionStrategy = getStrategyByString(collisionStrategyString,true);
                brick = new Brick(new Vector2(corXPosition, corYPosition), new Vector2(brickWidth, BRICK_LENGTH), brickImage, collisionStrategy);
        }
        return brick;
    }


    private CollisionStrategy getStrategyByString(String strategy, boolean isFirst){
        switch (strategy) {
            case "TurboCollisionStrategy":
                return new TurboCollisionStrategy(this,isFirst);
            case "HeartCollisionStrategy":
                return new HeartCollisionStrategy(this,isFirst);
            case "ExtraPuddleCollisionStrategy":
                return new ExtraPuddleCollisionStrategy(this,isFirst);
            case "PuckCollisionStrategy":
                return new PuckCollisionStrategy(this,isFirst);
            default:
                return new BasicCollisionStrategy(this);
//            default: return null;
        }

    }

    private String getCollisionStrategy(int num) {
        Random random = new Random();
        int randomNumber = random.nextInt(num)+1;
        switch (randomNumber) {
            case 1:
                return "TurboCollisionStrategy";
            case 2:
                return "HeartCollisionStrategy";
            case 3:
                return "ExtraPuddleCollisionStrategy";
            case 4:
                return "PuckCollisionStrategy";
            case 5:
                return "doubleCollisionStrategy";
            default:
                return "BasicCollisionStrategy";
            //default: return null;
        }
    }

    private void createBackground(ImageReader imageReader, Vector2 windowDimensions) {
        Renderable backgroundImage = imageReader.readImage("assets/DARK_BG2_small.jpeg", false);
        GameObject background = new GameObject(Vector2.ZERO, windowDimensions, backgroundImage);
        gameObjects().addGameObject(background, Layer.BACKGROUND);
    }


    private void createPaddle(ImageReader imageReader, UserInputListener inputListener, Vector2 windowDimensions) {
        Renderable paddleImage = imageReader.readImage("assets/paddle.png", true);
        this.paddle = new Paddle(Vector2.ZERO, PADDLE_SIZE, paddleImage, inputListener, windowDimensions);
        paddle.setCenter(new Vector2(windowDimensions.x()/2, windowDimensions.y()- 30));
        paddle.setTag(PADDLE_TAG);
        gameObjects().addGameObject(paddle,Layer.FOREGROUND);
    }

    /**
     * creates an extra paddle for the extra paddle collision strategy
     */
    public void createExtraPaddle(){
        if(canAddPaddle){
            canAddPaddle=false;
            Renderable paddleImage = imageReader.readImage("assets/paddle.png", true);
            this.extraPaddle = new Paddle(Vector2.ZERO, PADDLE_SIZE, paddleImage,inputListener, windowDimensions);
            extraPaddle.setCenter(new Vector2(windowDimensions.x()/2, windowDimensions.y()/2));
            gameObjects().addGameObject(extraPaddle);}
    }

    private void deleteExtraPuddle(Paddle extraPaddle){
        if(extraPaddle==null){
            return;
        }
        if (extraPaddle.getCollisionCounter()==4)
        {
            gameObjects().removeGameObject(extraPaddle);
            canAddPaddle=true;
        }

    }

    private void createBall(ImageReader imageReader, SoundReader soundReader, Vector2 windowDimensions) {
        Renderable ballImage = imageReader.readImage("assets/ball.png", true);
        Sound collisionSound = soundReader.readSound("assets/blop.wav");
        Ball ball = new Ball(Vector2.ZERO, MAIN_BALL_SIZE, ballImage, collisionSound);
        this.ball = ball;
        float ballVX = BALL_SPEED;
        float ballVY = BALL_SPEED;
        Random rand = new Random();
        if (rand.nextBoolean()) {
            ballVX *= -1;
        }
        if (rand.nextBoolean()) {
            ballVY *= -1;
        }
        ball.setVelocity(new Vector2(ballVX, ballVY));
        ball.setTag(BALL_TAG);
        ball.setCenter(windowDimensions.mult(0.5f));
        this.gameObjects().addGameObject(ball);
    }

    /**
     * defines what happens when the turbo mode is activated or disabled for the turbo collision strategy.
     * @param mode the string to determine what happens/
     */
    public void ballMode(String mode)
    {
        switch (mode) {
            case "Turbo":
                if(!ballInTurboMode)
                {

                    ballInTurboMode=true;
                    ballCollisionCounter = ball.getCollisionCounter();
                    ball.setVelocity(new Vector2(BALL_SPEED*TURBO_SIZE, BALL_SPEED*TURBO_SIZE));
                    ball.renderer().setRenderable(imageReader.readImage("assets/ball.png",false));
                    ball.renderer().setRenderable(imageReader.readImage("assets/redBall.png", true));
                }

            case "Regular":
                if (ball.getCollisionCounter()==ballCollisionCounter+MAX_TURBO_COLLISION)
                {
                    ballInTurboMode=false;
                    ball.setVelocity(new Vector2(BALL_SPEED, BALL_SPEED));
                    ball.renderer().setRenderable(imageReader.readImage("assets/redBall.png", false));
                    ball.renderer().setRenderable(imageReader.readImage("assets/ball.png",true));
                }
        }
    }


    /**
     * creates the puck of balls for the puck collision strategy.
     */
    public void createPuck(Vector2 position){
        Renderable ballImage = imageReader.readImage("assets/mockBall.png", true);
        Sound collisionSound = soundReader.readSound("assets/blop.wav");
        Ball puck = new Ball(Vector2.ZERO, PUCK_BALL_SIZE, ballImage, collisionSound);
        Random rand = new Random();
        double angle = rand.nextDouble()*Math.PI;
        float velocityX = (float) Math.cos(angle)*BALL_SPEED;
        float velocityY = (float) Math.sin(angle)*BALL_SPEED;
        puck.setVelocity(new Vector2(-velocityX, -velocityY));
        puck.setCenter(position);
        this.gameObjects().addGameObject(puck);
        puckList.add(puck);
    }

    /**
     * creates the heart that falls from the brick according to the heart collision strategy.
     * @param brickPosition the position of the brick where the heart drops from.
     */
    public void createHeart(Vector2 brickPosition)
    {
        Renderable heartImage = imageReader.readImage("assets/heart.png", true);
        Heart heart = new Heart(brickPosition ,new Vector2(HEART_DIMENSIONS),heartImage);
        heart.setVelocity(HEART_VELOCITY);
        heart.setCenter(brickPosition);
        heart.changeTagName(PADDLE_TAG);
        heartsList.add(heart);
        this.gameObjects().addGameObject(heart,Layer.STATIC_OBJECTS);

    }

    private void deleteHeart()
    {
        Iterator<Heart> heartIterator = heartsList.iterator();
        while(heartIterator.hasNext()) {
            Heart heart = heartIterator.next();
            boolean heartCollision = heart.isDead();
            if(heartCollision) {
                if (numOfStrikesLeft < heartNumbersArray.length) {
                    deleteOrAddHeart("add");
                }
                heartIterator.remove();
                heartsList.remove(heart);
                gameObjects().removeGameObject(heart,Layer.STATIC_OBJECTS);
                break;
            }
            else {
                    float heartHeight = heart.getCenter().y();
                    if (heartHeight>windowDimensions.y()){
                        heartIterator.remove();
                        heartsList.remove(heart);
                        gameObjects().removeGameObject(heart,Layer.STATIC_OBJECTS);
                    }
                    break;
            }
        }

    }



    private void createWalls(Vector2 windowDimensions) {
        GameObject leftWall = new GameObject(new Vector2(-5,0), new Vector2(10, windowDimensions.y()), null);
        gameObjects().addGameObject(leftWall);
        GameObject upWall = new GameObject(Vector2.LEFT, new Vector2(windowDimensions.x(), 5), null);
        gameObjects().addGameObject(upWall);
        GameObject rightWall = new GameObject(new Vector2(windowDimensions.x()-5, 0), new Vector2(10, windowDimensions.y()), null);
        gameObjects().addGameObject(rightWall);
    }

    /**
     * removes the brick.
     * @param brick the brick to remove.
     */
    public void removeBrick(Brick brick) {
        gameObjects().removeGameObject(brick);
        numOfBricks--;
    }

    /**
     * main method.
     * @param args arguments from the user.
     */
    public static void main(String[] args) {
        int row = DEFAULT_ROWS;
        int col = DEFAULT_COLS;
        if(args.length == 2){
            row = Integer.parseInt(args[1]);
            col = Integer.parseInt(args[0]);
        }

        GameManager gameManager = new BrickerGameManager("BrickerGameManager", new Vector2(700, 500), new Vector2((float)row, (float)col), 4);
        gameManager.run();
    }
}
