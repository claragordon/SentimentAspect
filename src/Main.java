import java.io.*;
import java.util.*;
/*
import edu.stanford.nlp.dcoref.CorefChain;
import edu.stanford.nlp.dcoref.CorefCoreAnnotations;
import edu.stanford.nlp.io.*;
import edu.stanford.nlp.ling.*;
import edu.stanford.nlp.neural.rnn.RNNCoreAnnotations;
import edu.stanford.nlp.pipeline.*;
import edu.stanford.nlp.semgraph.SemanticGraph;
import edu.stanford.nlp.semgraph.SemanticGraphCoreAnnotations;
import edu.stanford.nlp.sentiment.SentimentCoreAnnotations;
import edu.stanford.nlp.trees.*;
import edu.stanford.nlp.util.*;
*/
public class Main {

    public static List<String> ngrams(int n, String str) {
        List<String> ngrams = new ArrayList<String>();
        String[] words = str.split(" ");
        for (int i = 0; i < words.length - n + 1; i++)
            ngrams.add(concat(words, i, i+n));
        return ngrams;
    }
    
    public static String concat(String[] words, int start, int end) {
        StringBuilder sb = new StringBuilder();
        for (int i = start; i < end; i++)
            sb.append((i > start ? " " : "") + words[i]);
        return sb.toString();
    }

    public static void main(String[] args) throws IOException {

	    Map<String, Integer> features = new HashMap<String, Integer>();
    
        List<Sentence> sentences = XMLReader.readFile("data/train/Laptop_Train_v2.xml");
      
        Sentence s = sentences.get(3);
        System.out.println(s.getText());
      
     
//       String[] split = s.getText().split("\\s+");
//       for (String w : split){
//          System.out.println(w);
//       }

		for (Aspect a : s.getAspects()){
            System.out.println("ASPECT: " + a.getText());
            String[] parts = s.getText().split(a.getText());
         
            List<String> front_ngrams = ngrams(1, parts[0]);
            if (front_ngrams.size() > 5){
                for (int i = 1; i < 6; i++){
            
                    String target = front_ngrams.get(front_ngrams.size() - i);
                    features.put(target, features.get(target)+1);
                    System.out.println(front_ngrams.get(front_ngrams.size() - i));
                }
            } else {
                for (int i = 1; i < front_ngrams.size()+1; i++){
                System.out.println(front_ngrams.get(front_ngrams.size() - i));
                }
            }

			int current_count;
			String feature;
            List<String> ngrams = ngrams(1, parts[1]);
            if (ngrams.size() > 5){
                for (int i = 1; i < 6; i++){
	                feature = ngrams.get(i);
	                System.out.println(feature);

		            // add to feature map
		            if (features.containsKey(feature)) current_count = features.get(feature);
		            else current_count = 0;
		            features.put(feature, current_count + 1);

                }
            } else {
                for (int i = 1; i < ngrams.size()+1; i++) {
                    feature = ngrams.get(i);
	                System.out.println(feature);

		            // add to feature map
		            if (features.containsKey(feature)) current_count = features.get(feature);
		            else current_count = 0;
		            features.put(feature, current_count + 1);
            }
         }

        System.out.println("FINISHED ASPECT: " + a.getText());


//          System.out.println(temp.sublist(0,5));
//          System.out.println(ngrams(1, parts[1]));
      
//          System.out.println(s.getText().indexOf(a.getText()));
//          int start = s.getText().indexOf(a.getText());
//          
//          String secondPart = s.getText().substring(s.getText().indexOf(a.getText()));
//          System.out.println(s.getText());
//          System.out.println(a.getText());
//          System.out.println(firstPart);
//          System.out.println(s.getText()[)
//          System.out.println(a.getText());
//          System.out.println(a.getPolarity());
      }
    }
      


}
