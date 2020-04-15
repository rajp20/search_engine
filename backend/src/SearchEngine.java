import org.json.simple.JSONObject;

public class SearchEngine {

    public static String search(String query) {
        JSONObject obj = new JSONObject();
        obj.put("Result", "Hello World!");

        return obj.toJSONString();
    }
}
