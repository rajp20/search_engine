import org.json.simple.JSONObject;

import org.lemurproject.galago.core.index.Index;
import org.lemurproject.galago.core.index.corpus.DocumentReader;
import org.lemurproject.galago.core.index.stats.FieldStatistics;
import org.lemurproject.galago.core.index.stats.IndexPartStatistics;
import org.lemurproject.galago.core.parse.Document;
import org.lemurproject.galago.core.parse.Document.DocumentComponents;
import org.lemurproject.galago.core.retrieval.*;
import org.lemurproject.galago.core.retrieval.iterator.LengthsIterator;
import org.lemurproject.galago.core.retrieval.processing.ScoringContext;
import org.lemurproject.galago.core.retrieval.query.Node;
import org.lemurproject.galago.core.retrieval.query.StructuredQuery;
import org.lemurproject.galago.utility.Parameters;
import org.lemurproject.galago.core.*;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileWriter;
import java.io.InputStreamReader;

import org.apache.commons.csv.*;

public class SearchEngine {

    public static String moviesIndex = "backend/movies_index/";
    public static String namesIndex = "backend/names_index/";

    public static String imdbMovieDatasetPath = "dataset/IMDb/imdb-extensive-dataset/IMDb_movies.csv";

    public JSONObject movieDataset;

    public SearchEngine() {
        movieDataset = loadCSV(imdbMovieDatasetPath);
    }

    public static JSONObject loadCSV(String path) {
        JSONObject toReturn = new JSONObject();
        try {
            FileInputStream csvFile = new FileInputStream(path);
            InputStreamReader input = new InputStreamReader(csvFile);
            CSVParser parser = CSVFormat.EXCEL.withFirstRecordAsHeader().parse(input);
            for (CSVRecord record : parser) {
                JSONObject toAdd = new JSONObject();
                String id = record.get("imdb_title_id").substring(2);
                toAdd.put("ID", id);
                toAdd.put("Title", record.get("title"));
                toAdd.put("Year", record.get("year"));
                toAdd.put("Date Published", record.get("date_published"));
                toAdd.put("Genre", record.get("genre"));
                toAdd.put("Duration", record.get("duration"));
                toAdd.put("Country", record.get("country"));
                toAdd.put("Language", record.get("language"));
                toAdd.put("Director", record.get("director"));
                toAdd.put("Writer", record.get("writer"));
                toAdd.put("Production Company", record.get("production_company"));
                toAdd.put("Actors", record.get("actors"));
                toAdd.put("Description", record.get("description"));
                toAdd.put("Avg Vote", record.get("avg_vote"));
                toAdd.put("Votes", record.get("votes"));
                toAdd.put("Budget", record.get("budget"));
                toAdd.put("USA Gross Income", record.get("usa_gross_income"));
                toAdd.put("Worldwide Gross Income", record.get("worlwide_gross_income"));
                toAdd.put("Metascore", record.get("metascore"));
                toAdd.put("Reviews From Users", record.get("reviews_from_users"));
                toAdd.put("Reviews From Critics", record.get("reviews_from_critics"));
                toReturn.put(id, toAdd);
            }
            System.out.println("Writing to JSON file...");
            FileWriter jsonFile = new FileWriter("dataset/IMDb/movies.json");
            jsonFile.write(toReturn.toJSONString());
            jsonFile.flush();
            jsonFile.close();
            return toReturn;
        } catch (Exception ex) {
            ex.printStackTrace();
            return null;
        }
    }

    public String search(String query) {
        JSONObject searchedMoviesIDs = searchMovies(query);
        JSONObject searchedMoviesData = getMovieDataFromIDs(searchedMoviesIDs);
        return searchedMoviesData.toJSONString();
    }

    public JSONObject getMovieDataFromIDs(JSONObject movieIDs) {
        System.out.println("Getting movie data...");
        JSONObject toReturn = new JSONObject();
        for (Object ID : movieIDs.keySet()) {
            String id = (String) ID;
            JSONObject toAdd = (JSONObject) movieDataset.get(id);
            JSONObject movieIDData = (JSONObject) movieIDs.get(id);
            toAdd.put("Rank", movieIDData.get("Rank"));
            toAdd.put("Score", movieIDData.get("Score"));
            toReturn.put(id, toAdd);
        }
        System.out.println("Done.\n");
        return toReturn;
    }

    public static JSONObject searchMovies(String query) {
        JSONObject toReturn = new JSONObject();
        try {
            Parameters queryParams = Parameters.create();
            queryParams.set("index", moviesIndex);

            //- Set how many docs to return
            queryParams.set("requested", 50);

            //- Do verbose output
            queryParams.set("verbose", true);

            //- Set the index to be searched
            Retrieval ret = RetrievalFactory.create(queryParams);


            //  Returned parsed query will be the root node of a query tree.
            Node q = StructuredQuery.parse(query);
            System.out.println("Parsed Query: " + q.toString());

            //- Transform the query in compliance to the many traversals that might
            //  (or might not) apply to the query.
            Node transq = ret.transformQuery(q, Parameters.create());
            System.out.println("\nTransformed Query: " + transq.toString());

            //- Do the Retrieval
            Results results = ret.executeQuery(transq, queryParams);

            // View Results or inform search failed.
            if (results.scoredDocuments.isEmpty()) {
                System.out.println("Search failed. Nothing retrieved.");
            } else {
                //- The DocumentComponents object stores information about a
                //  document.
                DocumentComponents dcs = new DocumentComponents();

                for (ScoredDocument sd : results.scoredDocuments) {
                    int rank = sd.rank;

                    //- internal ID (indexing sequence number)of document
                    long   iid = sd.document;
                    double score = sd.score;

                    //- Get the external ID (ID in the text) of the document.
                    String eid = ret.getDocumentName(sd.document);

                    //- Get document length based on the internal ID.
                    int len = ret.getDocumentLength(sd.document);

                    ret.getDocument(eid, dcs);

//                    System.out.printf ("Rank : %d \t ID: %s [%d] \t Score: %f \t Len: %d \n",
//                            rank, eid, iid, score, len);

                    JSONObject toAdd = new JSONObject();
                    toAdd.put("Rank", rank);
                    toAdd.put("ID", eid);
                    toAdd.put("Score", score);

                    toReturn.put(eid, toAdd);
                }

                System.out.println("Total documents containing the word '" + query + "': " + results.scoredDocuments.size());
            }
        } catch (Exception ex) {
            ex.printStackTrace();
        }
        return toReturn;
    }

    public static void searchActors(String query) {

    }
}
