class PlayerFactory {
    public PlayerFactory() {}

    /**
     * Creates a player instance based on the provided type.
     *
     * @param type The type of player to create (e.g., "human", "clever").
     * @return The corresponding player instance or null if the type is invalid.
     */
    public Player buildPlayer(String type){
        Player player;
        switch (type){
            case "human":
                player = new HumanPlayer();
                break;
            case "whatever":
                player = new WhateverPlayer();
                break;
            case "clever":
                player = new CleverPlayer();
                break;
            case "genius":
                player = new GeniusPlayer();
                break;
            default:
                player = null;
        }
        return player;
    }
}
