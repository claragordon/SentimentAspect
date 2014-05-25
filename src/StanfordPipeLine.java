

import edu.stanford.nlp.io.*;
import edu.stanford.nlp.ling.*;
import edu.stanford.nlp.pipeline.*;
import edu.stanford.nlp.semgraph.SemanticGraph;
import edu.stanford.nlp.semgraph.SemanticGraphCoreAnnotations;
import edu.stanford.nlp.trees.*;
import edu.stanford.nlp.util.*;

import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.List;
import java.util.Properties;

/**
 * @author Clara Gordon
 */
public class StanfordPipeLine {

	private StanfordCoreNLP pipeline;

	public StanfordPipeLine() {
		Properties props = new Properties ();
		props.put("annotators", "tokenize, ssplit, pos, parse, sentiment");
		pipeline = new StanfordCoreNLP(props);
	}

	public String posString(String text, Aspect a) {

		int start = a.getStart ();
		int end = a.getEnd ();

		text = text.replaceAll ("[\\.\\?\\',:;]", "");


	    // create an empty Annotation just with the given text
	    Annotation document = new Annotation(text);

	    // run all Annotators on this text
	    this.pipeline.annotate(document);

	    // these are all the sentences in this document
	    // a CoreMap is essentially a Map that uses class objects as keys and has values with custom types
	    List<CoreMap> sentences = document.get(CoreAnnotations.SentencesAnnotation.class);

//		List<String> posTagged = new ArrayList<String> ();
		String add;
	    String result = "";
		for(CoreMap sentence: sentences) {
		    // traversing the words in the current sentence
		    // a CoreLabel is a CoreMap with additional token-specific methods

		    for (CoreLabel token: sentence.get(CoreAnnotations.TokensAnnotation.class)) {
			    add = "";
			    // this is the text of the token
			    String word = token.get(CoreAnnotations.TextAnnotation.class);
			    add += word;
			    // this is the POS tag of the token
			    String pos = token.get(CoreAnnotations.PartOfSpeechAnnotation.class);
			    add += "_" + pos;
			    // this is the NER label of the token
			    String ne = token.get(CoreAnnotations.NamedEntityTagAnnotation.class);

			    result += add + " ";
		    }

		    System.out.println(result);
		    // this is the parse tree of the current sentence
		    Tree tree = sentence.get(TreeCoreAnnotations.TreeAnnotation.class);

		    // this is the Stanford dependency graph of the current sentence
		    SemanticGraph dependencies;
		    dependencies = sentence.get(SemanticGraphCoreAnnotations.CollapsedCCProcessedDependenciesAnnotation.class);
	    }

		return result;
	}




//	public static void stanford() {
//
//
//		Properties props = new Properties();
//		props.setProperty("annotators", "tokenize, ssplit, parse, sentiment");
//		PrintWriter out = new PrintWriter (System.out);
//
//
//		StanfordCoreNLP pipeline = new StanfordCoreNLP(props);
//
//
//		List<Sentence> sentences = XMLReader.readFile("data/test/Laptops_Test_data_phaseB.xml");
//		for (Sentence s : sentences) {
////                  System.out.print(s);
//
//
//			Annotation annotation = pipeline.process(s.getText());
//			for (CoreMap sentence : annotation.get(CoreAnnotations.SentencesAnnotation.class)) {
//				Tree tree = sentence.get (SentimentCoreAnnotations.AnnotatedTree.class);
//				List<LabeledScoredTreeNode> list  = tree.getLeaves ();
//
//				double score = list.get(0).score ();
//
//
//				SentimentCostAndGradient RNNCoreAnnotations;
//				int sentiment = RNNCoreAnnotations.getPredictedClass (tree);
//
//				System.out.println(s.getText());
//				System.out.println(sentiment);
//
//			}
//
//		}
//	}


}
