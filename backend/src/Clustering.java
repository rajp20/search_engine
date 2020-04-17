import org.python.util.PythonInterpreter;

public class Clustering {
    public static void test() {
    try(PythonInterpreter pi = new PythonInterpreter()) {
        pi.execfile("python/clustering/Cluster.py");
        pi.exec("k_means_pp(\"Passed in value!\")");
    }
  }
}
