public class RendererFactory {
    public RendererFactory() {}

    /**
     * Creates a renderer instance based on the provided type and size.
     *
     * @param type The type of renderer (e.g., "void", "console").
     * @param size The size parameter, used for console rendering.
     * @return The corresponding renderer instance or null if the type is invalid.
     */
    public Renderer buildRenderer(String type, int size){
        Renderer renderer;
        switch (type) {
            case "void":
                renderer = new VoidRenderer();
                break;
            case "console":
                renderer = new ConsoleRenderer(size);
                break;
            default:
                renderer = null;
        }
        return renderer;
    }
}
