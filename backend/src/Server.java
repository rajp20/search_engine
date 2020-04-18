import com.sun.net.httpserver.Headers;
import com.sun.net.httpserver.HttpContext;
import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpServer;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.InetSocketAddress;
import java.net.URI;
import java.net.URL;
import java.util.HashMap;
import java.util.Map;

import org.apache.http.HttpEntity;
import org.apache.http.HttpHeaders;
import org.apache.http.client.methods.CloseableHttpResponse;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.client.methods.HttpPatch;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.entity.StringEntity;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.impl.client.HttpClients;
import org.apache.http.util.EntityUtils;
import org.python.antlr.ast.Str;

public class Server {

    public static SearchEngine searchEngine = new SearchEngine();

    public static void main(String[] args) throws IOException {
        HttpServer server = HttpServer.create(new InetSocketAddress("localhost", 8000), 0);
        HttpContext context = server.createContext("/search");
        context.setHandler(Server::handleSearch);
        System.out.println("Started Server...\n");
        server.start();
    }

    public static void handleSearch(HttpExchange exchange) throws IOException {
        URI requestURI = exchange.getRequestURI();
        Map<String, String> query = queryToMap(requestURI.getQuery());
        String searchQuery = query.get("search_query");
        System.out.println("Search query: " + searchQuery);

        String response;
        if (searchQuery == null) {
            response = "{Bad search.}";
        } else {
            response = searchEngine.search(searchQuery);
        }

        String clusteredResults = clusterResults(response);
        System.out.println(clusteredResults);

//        System.out.println("JSON Response:");
//        System.out.println(response);
//        System.out.println();

        Headers headers = exchange.getResponseHeaders();
        headers.add("Content-Type", "application/json");
        headers.add("Access-Control-Allow-Origin", "*");

        exchange.sendResponseHeaders(200, response.getBytes().length);
        OutputStream os = exchange.getResponseBody();
        os.write(response.getBytes());
        os.close();
    }

    public static Map<String, String> queryToMap(String query) {
        Map<String, String> result = new HashMap<>();
        for (String param : query.split("&")) {
            String[] entry = param.split("=");
            if (entry.length > 1) {
                result.put(entry[0], entry[1]);
            }else{
                result.put(entry[0], "");
            }
        }
        return result;
    }

    public static String clusterResults(String results) throws IOException {
        System.out.println("Making cluster request...");
        CloseableHttpClient httpClient = HttpClients.createDefault();
        String toReturn = "";
        try {
            HttpPost request = new HttpPost("http://localhost:8001/cluster");
            StringEntity resultsEntity = new StringEntity(results, "UTF-8");
            request.setEntity(resultsEntity);
            request.setHeader("Content-Type", "application/json");

            CloseableHttpResponse response = httpClient.execute(request);
            try {
                HttpEntity entity = response.getEntity();
                if (entity != null) {
                    toReturn = EntityUtils.toString(entity);
                }
            } finally {
                response.close();
            }
        } finally {
            httpClient.close();
        }
        System.out.println("Done.\n");
        return toReturn;
    }

}