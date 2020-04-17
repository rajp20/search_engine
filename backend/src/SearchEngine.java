import jdk.nashorn.internal.parser.JSONParser;
import org.json.JSONObject;


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
import org.python.antlr.ast.Str;

import org.apache.commons.io.IOUtils;

import java.io.FileInputStream;
import java.io.InputStream;

public class SearchEngine {

    public static String moviesIndex = "backend/movies_index/";
    public static String namesIndex = "backend/names_index/";

    public static String imdbMovieDatasetPath = "dataset/IMDb/movies_pretty.json";

    public JSONObject movieDataset;

    public SearchEngine() {
        movieDataset = loadJSON(imdbMovieDatasetPath);
    }

    public JSONObject loadJSON(String file) {
        System.out.println("Loading JSON dataset...");
        JSONObject toReturn = new JSONObject();
        try {
            InputStream is = new FileInputStream(file);
            String jsonText = IOUtils.toString(is, "UTF-8");
            toReturn = new JSONObject(jsonText);
        } catch (Exception ex) {
            ex.printStackTrace();
        }
        System.out.println("Done.\n");
        return toReturn;
    }

    public String search(String query) {
        System.out.println("Searching...");
        JSONObject searchedMoviesIDs = searchWithGalago(query, moviesIndex);
        JSONObject searchedMoviesData = getMovieDataFromIDs(searchedMoviesIDs);
        System.out.println("Done searching.\n");
        return searchedMoviesData.toString();
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

    public static JSONObject searchWithGalago(String query, String indexPath) {
        JSONObject toReturn = new JSONObject();
        try {
            Parameters queryParams = Parameters.create();
            queryParams.set("index", indexPath);

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
}
