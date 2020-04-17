import org.python.util.PythonInterpreter;
import org.python.core.*;
//import org.python.modules.jarray;

public class Clustering {
    public static void test() {
    try(PythonInterpreter pi = new PythonInterpreter()) {
        pi.execfile("python/clustering/Cluster.py");
        pi.exec("k_means_pp(\"Passed a string to Python!\")");
        PyArray data = new PyArray(String.class, 10);
        for(int i=0; i < 10; i++) {
            data.set(i, new PyString("hi"));
        }

    }
  }
}
