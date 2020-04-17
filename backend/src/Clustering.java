import org.python.util.PythonInterpreter;

public class Clustering {
    public static void test() {
    try(PythonInterpreter pyInterp = new PythonInterpreter()) {
      pyInterp.exec("print('Hello Python World!')");
    }
  }
}
