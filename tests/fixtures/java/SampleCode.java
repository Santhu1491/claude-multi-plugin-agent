import java.util.List;
import java.util.stream.Collectors;

/**
 * Sample Java code for testing.
 */
public class SampleCode {
    
    /**
     * Calculate the sum of a list of numbers.
     */
    public static int calculateSum(List<Integer> numbers) {
        return numbers.stream()
            .mapToInt(Integer::intValue)
            .sum();
    }
    
    /**
     * Calculate the average of a list of numbers.
     */
    public static double calculateAverage(List<Integer> numbers) {
        if (numbers.isEmpty()) {
            return 0.0;
        }
        return numbers.stream()
            .mapToInt(Integer::intValue)
            .average()
            .orElse(0.0);
    }
    
    /**
     * Data analyzer class.
     */
    public static class DataAnalyzer {
        private final List<Integer> data;
        
        public DataAnalyzer(List<Integer> data) {
            this.data = data;
        }
        
        public int count() {
            return data.size();
        }
        
        public int findMax() {
            return data.stream()
                .mapToInt(Integer::intValue)
                .max()
                .orElse(0);
        }
        
        public int findMin() {
            return data.stream()
                .mapToInt(Integer::intValue)
                .min()
                .orElse(0);
        }
    }
}
