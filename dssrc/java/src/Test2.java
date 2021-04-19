import org.nd4j.linalg.factory.Nd4jBackend;
import org.nd4j.linalg.factory.Nd4j;


public class Test2 {

	public static void main(String args[]){

		Nd4jBackend b = Nd4j.getBackend();
		System.out.println("Test1");
		if(b!=null){
			System.out.println("Test2");
			boolean gpuBackendAvailable = b.getClass().getCanonicalName().toLowerCase().contains("jcublas");
			System.out.println("Result : " + gpuBackendAvailable);
		}
	}

}
