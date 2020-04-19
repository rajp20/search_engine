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

import java.io.IOException;
import java.util.logging.FileHandler;
import java.util.logging.Logger;
import java.util.logging.SimpleFormatter;

public class SearchEngine {

    public static String moviesIndex = "../dataset/movies_index";
    public static String namesIndex = "../dataset/names_index/";

    public static String imdbMovieDatasetPath = "dataset/movie_review.json";

    public static Logger logger = Logger.getLogger("MyLog");

    public static void main(String[] args) {
        // System.out.println("Working Directory = " + System.getProperty("user.dir"));
        if (args.length != 1) {
          System.out.println("Fail. Please pass in a query.");
           return;
        }
        FileHandler fh;

        try {
            // This block configure the logger with handler and formatter
            fh = new FileHandler("GalagoSearch.log");
            logger.addHandler(fh);
            SimpleFormatter formatter = new SimpleFormatter();
            fh.setFormatter(formatter);
            logger.setUseParentHandlers(false);
        } catch (SecurityException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }

        String results = search(args[0]);
        System.out.println(results);
    }

    public static String search(String query) {
        logger.info("Searching...");
        JSONObject searchedMoviesIDs = searchWithGalago(query, moviesIndex);
        logger.info("Done searching.\n");
        return searchedMoviesIDs.toString();
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

            //- Do casefold
            queryParams.set("casefold", true);

            //- Set to Relevance Model1
            queryParams.set("relevanceModel", "org.lemurproject.galago.core.retrieval.prf.RelevanceModel1");

            //- Add title and actors fields
            String[] fields = {"title", "actors"};
            queryParams.set("fields", fields);

            //- Score set to jm
            queryParams.set("scorer", "jm");

            //- Add weights to fields
            Weights weights = new Weights(0.8, 0.2);
            queryParams.set("weights", String.valueOf(weights));

            //- Set the index to be searched
            Retrieval ret = RetrievalFactory.create(queryParams);

            //- Transform the query in compliance to the many traversals that might
            //  (or might not) apply to the query.
            String queryText = "#prms(" + query + ")";
            Node q = StructuredQuery.parse(queryText);

            //  Returned parsed query will be the root node of a query tree.
            logger.info("Parsed Query: " + q.toString());

            Node transq = ret.transformQuery(q, Parameters.create());
            logger.info("\nTransformed Query: " + transq.toString());

            //- Do the Retrieval
            Results results = ret.executeQuery(transq, queryParams);

            // View Results or inform search failed.
            if (results.scoredDocuments.isEmpty()) {
                logger.info("Search failed. Nothing retrieved.");
                toReturn.put("Stats", "No search results.");
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

                logger.info("Total documents containing the word '" + query + "': " + results.scoredDocuments.size());
            }
        } catch (Exception ex) {
            ex.printStackTrace();
        }
        return toReturn;
    }
}
