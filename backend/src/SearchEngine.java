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

import org.python.util.PythonInterpreter;

public class SearchEngine {

    public static String indexPath = "backend/movies_index/";

    public static String search(String query) {
        galagoSearch(query);
        JSONObject obj = new JSONObject();
        obj.put("Result", "Hello World!");

        return obj.toJSONString();
    }

    public static void galagoSearch(String query) {
        System.out.println("Searching with galago...");
//        System.out.println("Working Directory = " + System.getProperty("user.dir"));
        try {
            Parameters queryParams = Parameters.create();
            queryParams.set("index", indexPath);


//            queryParams.set("inputPath", inputPath);
//            queryParams.set("filetype", "trectext");
            //- Set how many docs to return
            queryParams.set("requested", 5);

            //- Do verbose output
            queryParams.set("verbose", true);

            //- Set the index to be searched
            Retrieval ret = RetrievalFactory.create(queryParams);
            LocalRetrieval localRet = new LocalRetrieval(indexPath, queryParams);


            FieldStatistics fs = ret.getCollectionStatistics("#lengths:part=lengths()");

            int maxDocLength = 0;
            String maxDocName = "";
            for (long i = 0; i < fs.documentCount; i++) {
                String name = localRet.getDocumentName(i);
                int len = localRet.getDocumentLength(i);
                if (len > maxDocLength) {
                    maxDocLength = len;
                    maxDocName = name;
                }
            }

            //            LengthsIterator iterator = localRet.getDocumentLengthsIterator();
//            ScoringContext sc = new ScoringContext();
//            while (!iterator.isDone()) {
//                sc.document = iterator.currentCandidate();
//                if (iterator.hasMatch(sc)) {
//                    String name = localRet.getDocumentName(sc.document);
//                    int len = iterator.length(sc);
//                    if (len > maxDocLength) {
//                        maxDocName = name;
//                        maxDocLength = len;
//                    }
//                }
//                iterator.movePast(sc.document);
//            }

            System.out.println("Max Length of a Document");
            System.out.println("Length: " + maxDocLength);
            System.out.println("ID: " + maxDocName);

            System.out.println("\nFieldStatistics...");
            System.out.println("Field Name           : " + fs.fieldName);
            System.out.println("Collection Length    : " + fs.collectionLength);
            System.out.println("Document Count       : " + fs.documentCount);
            System.out.println("Max Length           : " + fs.maxLength);
            System.out.println("Min Length           : " + fs.minLength);
            System.out.println("Ave Length           : " + fs.avgLength);
            System.out.println("Non Zero Len Doc Cnt : " + fs.nonZeroLenDocCount);
            System.out.println("First Doc ID: " + fs.firstDocId +
                    "      Last Doc ID: " + fs.lastDocId);

            IndexPartStatistics ips = ret.getIndexPartStatistics ("postings");
            System.out.println ("\nIndexPartStatistics...");
            System.out.println ("Part Name              : " + ips.partName);
            System.out.println ("Collection Length      : " + ips.collectionLength);
            System.out.println ("Highest Document Count : " + ips.highestDocumentCount);
            System.out.println ("Vocabulary Count       : " + ips.vocabCount);
            System.out.println ("Highest Frequency      : " + ips.highestFrequency);

            //- Construct initial query.  Could be a simple or complex type.
            String qText = query;

            //  Returned parsed query will be the root node of a query tree.
            Node q = StructuredQuery.parse(qText);
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
          }

                System.out.println("Total documents containing the word '" + query + "': " + results.scoredDocuments.size());
            }
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }
}
