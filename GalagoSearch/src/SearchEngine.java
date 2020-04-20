import org.json.JSONObject;

import org.lemurproject.galago.core.eval.Eval;
import org.lemurproject.galago.core.index.Index;
import org.lemurproject.galago.core.index.corpus.DocumentReader;
import org.lemurproject.galago.core.index.stats.FieldStatistics;
import org.lemurproject.galago.core.index.stats.IndexPartStatistics;
import org.lemurproject.galago.core.parse.Document;
import org.lemurproject.galago.core.parse.Document.DocumentComponents;
import org.lemurproject.galago.core.retrieval.*;
import org.lemurproject.galago.core.retrieval.processing.ScoringContext;
import org.lemurproject.galago.core.retrieval.query.Node;
import org.lemurproject.galago.core.retrieval.query.StructuredQuery;
import org.lemurproject.galago.utility.Parameters;
import org.lemurproject.galago.core.*;

import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.PrintStream;
import java.util.ArrayList;
import java.util.List;
import java.util.logging.FileHandler;
import java.util.logging.Logger;
import java.util.logging.SimpleFormatter;

public class SearchEngine {

    public static String moviesIndex = "../dataset/movies_index";
    public static final String judgmentFile = "../dataset/movies.qrels";

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
        JSONObject bestToReturn = new JSONObject();
        Double bestAverage = Double.MIN_VALUE;
        for (int i = 0; i < 5; i++) {
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
                String[] fields = {"title", "actors", "reviews", "director", "description", "genre"};
                queryParams.set("fields", fields);

                //- Score set to jm
                queryParams.set("scorer", "jm");

                //- Add weights to fields
                Parameters weightParams = Parameters.create();
                if (i == 0) {
                    weightParams.set("title", 0.4);
                    weightParams.set("director", 0.2);
                    weightParams.set("actors", 0.2);
                    weightParams.set("description", 0.1);
                    weightParams.set("genre", 0.05);
                    weightParams.set("reviews", 0.05);
                } else if (i == 1) {
                    weightParams.set("title", 0.2);
                    weightParams.set("director", 0.4);
                    weightParams.set("actors", 0.2);
                    weightParams.set("description", 0.1);
                    weightParams.set("genre", 0.05);
                    weightParams.set("reviews", 0.05);
                } else if (i == 2) {
                    weightParams.set("title", 0.2);
                    weightParams.set("director", 0.2);
                    weightParams.set("actors", 0.4);
                    weightParams.set("description", 0.1);
                    weightParams.set("genre", 0.05);
                    weightParams.set("reviews", 0.05);
                } else if (i == 3) {
                    weightParams.set("description", 0.6);
                    weightParams.set("genre", 0.3);
                    weightParams.set("reviews", 0.1);
                } else {
                    weightParams.set("description", 0.3);
                    weightParams.set("genre", 0.6);
                    weightParams.set("reviews", 0.1);
                }
                queryParams.set("weights", weightParams);

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

                    List<Double> scores = new ArrayList<>();
                    Double minScore = Double.MAX_VALUE;
                    Double maxScore = Double.MIN_VALUE;

                    for (ScoredDocument sd : results.scoredDocuments) {
                        int rank = sd.rank;

                        double score = sd.score;
                        scores.add(score);
                        minScore = Math.min(minScore, score);
                        maxScore = Math.max(maxScore, score);

                        //- Get the external ID (ID in the text) of the document.
                        String eid = ret.getDocumentName(sd.document);

                        ret.getDocument(eid, dcs);

//                    System.out.printf ("Rank : %d \t ID: %s [%d] \t Score: %f \t Len: %d \n",
//                            rank, eid, iid, score, len);

                        JSONObject toAdd = new JSONObject();
                        toAdd.put("Rank", rank);
                        toAdd.put("ID", eid);
                        toAdd.put("Score", score);

                        toReturn.put(eid, toAdd);
                    }

//                    Evaluate(results.scoredDocuments);

                    logger.info("Getting average of scores...");
                    Double average = 0.0;
                    // Get mean of the scores
                    for (int j = 0; j < scores.size(); j++) {
                        Double mean = (scores.get(j) - minScore) / (maxScore - minScore);
                        average += mean;
                    }
                    average /= 50;

                    logger.info(average.toString());
                    if (bestAverage < average) {
                        bestAverage = average;
                        bestToReturn = toReturn;
                    }

                    logger.info("Total documents containing the word '" + query + "': " + results.scoredDocuments.size());
                }
            } catch (Exception ex) {
                ex.printStackTrace();
            }
        }
        return bestToReturn;
    }

    public static void Evaluate(List<ScoredDocument> scoredDocuments) {
        try {
            // Evaluate and it's parameters
            ResultWriter resultWriter = new ResultWriter("movies.list", false);
            resultWriter.write("1", scoredDocuments);
            Eval evaluate = new Eval();
            Parameters evalParam = Parameters.create();
            evalParam.set("baseline", "movies.list");
            evalParam.set("judgments", judgmentFile);
            evalParam.set("verbose", true);
            List<String> metrics = new ArrayList<String>();
            metrics.add("MAP");
            metrics.add("nDCG");
            evalParam.set("metrics", metrics);

            // Evaluate
            logger.info("Evaluating queries...");

            // To store in string
            // Create a stream to hold the output
            ByteArrayOutputStream baos = new ByteArrayOutputStream();
            PrintStream ps = new PrintStream(baos);
            // IMPORTANT: Save the old System.out!
            PrintStream old = System.out;
            // Tell Java to use your special stream
            System.setOut(ps);

            evaluate.run(evalParam, System.out);

            // Put things back
            System.out.flush();
            System.setOut(old);
            logger.info(baos.toString());
            logger.info("Done.\n");
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }
}
