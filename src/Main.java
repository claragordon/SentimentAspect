
import java.io.*;
import java.util.*;

public class Main {

	private static final int UNIGRAM_WINDOW = 5;

	public static void main(String[] args) throws IOException {
		printMalletFiles (args[0], "mallet_files/train");
		printMalletFiles (args[1], "mallet_files/test");

    }

	private static void printMalletFiles(String xmlFile, String malletFile) throws FileNotFoundException {

		File trainFile = new File(malletFile);
		PrintWriter writer = new PrintWriter(trainFile);
		List<Sentence> sentences = XMLReader.readFile(xmlFile);

		int counter = 0;
		for (Sentence s: sentences) {
			for (Aspect a : s.getAspects()){
				// write instance name
				writer.print(String.format("Instance%d:", counter) + " ");
				// write label
				writer.print(a.getPolarity () + " ");

				writeNGrams (s, a, 1, writer);
				writeNGrams (s, a, 2, writer);


				counter ++;

				writer.println ();
			}
		}
		writer.close();
	}


	private static void writeNGrams(Sentence s, Aspect a, int n, PrintWriter writer) {

		String front_span = s.getText ().toLowerCase ().substring (0, a.getStart ()).trim().replaceAll ("\\.\\?\\',:;", " ");
		String back_span = s.getText ().toLowerCase ().substring (a.getEnd ()).trim();
		// remove punc
		back_span = back_span.replaceAll ("[\\.\\?\\',:;]", " ");
		front_span = front_span.replaceAll ("[\\.\\?\\',:;]", " ");

		String [] front_words = trimUnigrams(front_span.trim().split(" "), true);
		String [] back_words = trimUnigrams(back_span.split(" "), false);

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

	public static String [] trimUnigrams(String [] words, boolean front) {

		int length = words.length;
		if (UNIGRAM_WINDOW >= length) return words;
		else if (front) return Arrays.copyOfRange (words, length - UNIGRAM_WINDOW, length);
		else return Arrays.copyOfRange (words, 0, UNIGRAM_WINDOW);


	}

}
