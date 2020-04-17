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
import java.io.InputStreamReader;

import org.apache.commons.csv.*;

public class SearchEngine {

    public static String moviesIndex = "backend/movies_index/";
    public static String namesIndex = "backend/names_index/";

    public static String imdbMovieDatasetPath = "dataset/IMDb/imdb-extensive-dataset/IMDb_movies.csv";

    public SearchEngine() {
        CSVParser movieDataset = loadCSV(imdbMovieDatasetPath);
    }

    public static CSVParser loadCSV(String path) {
        try {
            FileInputStream csvFile = new FileInputStream(path);
            InputStreamReader input = new InputStreamReader(csvFile);
            CSVParser parser = CSVFormat.EXCEL.withFirstRecordAsHeader().parse(input);
            return parser;
        } catch (Exception ex) {
            ex.printStackTrace();
        }
        return null;
    }

    public static String search(String query) {
        JSONObject searchedMovies = searchMovies(query);
        JSONObject obj = new JSONObject();
        obj.put("Result", "Hello World!");

        return obj.toJSONString();
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

                    System.out.printf ("Rank : %d \t ID: %s [%d] \t Score: %f \t Len: %d \n",
                            rank, eid, iid, score, len);

                    toReturn.put("Rank", rank);
                    toReturn.put("ID", eid);
                    toReturn.put("Score", score);
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
