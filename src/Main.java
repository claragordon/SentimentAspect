
import java.io.*;
import java.util.*;

public class Main {

	private static final int UNIGRAM_WINDOW = 5;

	public static void main(String[] args) throws IOException{
		printMalletFiles (args[0], "mallet_files/train");
		printMalletFiles (args[1], "mallet_files/test");
    }

	private static void printMalletFiles(String xmlFile, String malletFile) throws FileNotFoundException {

		File trainFile = new File(malletFile);
		PrintWriter writer = new PrintWriter(trainFile);
		List<Sentence> sentences = XMLReader.readFile(xmlFile);

		StanfordPipeLine pipeline = new StanfordPipeLine ();

		int counter = 0;
		String sText;
		int aspectIdx;
		for (Sentence s: sentences) {
			sText = s.getText ();
			for (Aspect a : s.getAspects()){
				// write instance name
				writer.print(String.format("Instance%d:", counter) + " ");
				// write label
				writer.print(a.getPolarity () + " ");
				aspectIdx = getAspectTokenIdx (sText, a);


				// FEATURES

				// sentiment rating: 1 - 5
				String sentiment  = pipeline.sentiment (sText, a);
			    writer.print("sentiment=" + sentiment + " ");


				// POS n_grams
				String posString = pipeline.posString (sText, a);
				writeNGrams (posString, a, 1, writer, aspectIdx, false);
            
            // surface distance to closest ADJ
            String closestAdjDistance = distanceOfClosestAdj(s, a, posString);
            writer.print("closestAdjDistance=" + closestAdjDistance + " ");


				// plain n-grams
				writeNGrams (sText, a, 1, writer, aspectIdx, true);
				writeNGrams (sText, a, 2, writer, aspectIdx, true);
   
            


				counter ++;

				writer.println ();
			}
		}
		writer.close();
	}

   private static String distanceOfClosestAdj(Sentence s, Aspect a, String posString){
      int start = getAspectTokenIdx(s.getText(), a);
      int min = 999; // 999 == no adjective
      String[] words = posString.split("\\s+");
      
      for (int i = 0; i < words.length; i++){
         String pos = words[i].split("_")[1];
         if (pos == "JJ"){
            if (Math.abs(i-start) < min){
               min = Math.abs(i-start);
            }
         }
      }
      
      return Integer.toString(min);
   }

   private String distanceFromAspect(Sentence s, Aspect a){
      //return the distance (in tokens and/or words) from this aspect to the nearest aspect
      //something like "distance_3"
      return "";
   }
   
   private String distanceFromStart(Sentence s, Aspect a){
      //return the distance (in tokens and/or words) from this aspect to the start of the sentence
      return "";
   }
   
   private String deepDistanceFromAspect(Sentence s, Aspect a){
      //return the distance in tree edges from this aspect to the nearest aspect
      //something like "tree_distance_3"
      return "";
   }
   
   private String deepDistanceFromStart(Sentence s, Aspect a){
      //return the distance in tree edges from this aspect to the start of the sentence
      return "";
   }

	private static void writeNGrams(String s, Aspect a, int n, PrintWriter writer, int aspectIdx, boolean raw) {



		if (raw) {
			// remove punc
			s = s.replaceAll ("[\\.\\?\\',:;]", "");
		}

		s = s.toLowerCase ();

		String [] split = s.trim().split(" ");



		String [] front_words = trimUnigrams (split, true, aspectIdx);
		String [] back_words = trimUnigrams (split, false, aspectIdx);

		// write front ngrams
		List<String> front_ngrams = ngrams(n, front_words);
		for (String ngram : front_ngrams) writer.print("before_" + ngram + " ");

		// write back ngrams
		List<String> back_ngrams = ngrams(n, back_words);
		for (String ngram : back_ngrams) writer.print("after_" + ngram + " ");

	}

	private static Map<String, Integer> updateMap(Map<String, Integer> map, String s) {
		// add to feature map
		int current_count;
		if (map.containsKey(s)) current_count = map.get(s);
		else current_count = 0;
		map.put (s, current_count + 1);
		return map;
	}

	public static List<String> ngrams(int n, String [] words) {

		List<String> ngrams = new ArrayList<String> ();
		for (int i = 0; i < words.length - n + 1; i++)
			ngrams.add(concat(words, i, i+n));

		return ngrams;
	}

	public static String concat(String[] words, int start, int end) {
		String ngram = "";
		for (int i = start; i < end - 1; i++)
			ngram += words[i] + "_";
		ngram += words[end - 1];
		return ngram;
	}

	public static String [] trimUnigrams(String [] words, boolean front, int aspectIdx) {

		int length = words.length;

		int start;
		int end;

		if ((front && aspectIdx == 0) || (!front && aspectIdx == length - 1))   {
			return new String [0];
		}

		if (front) {


			// assign start
			if (aspectIdx <= UNIGRAM_WINDOW + 1) {
				start = 0;
			} else {
				start = aspectIdx - UNIGRAM_WINDOW;
			}
			end = aspectIdx;

		} else {
			start = aspectIdx + 1;

			// assign end
			if (length <= aspectIdx + UNIGRAM_WINDOW + 1){
				end = length;
			} else {
				end = aspectIdx + UNIGRAM_WINDOW;
			}
		}

		if (end <= start) return new String [0];

		return Arrays.copyOfRange (words, start, end);
	}

	public static int getAspectTokenIdx(String s, Aspect a) {
		return s.substring (0, a.getStart ()).trim().split(" ").length;
	}

}
