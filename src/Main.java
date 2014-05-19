import java.io.*;
import java.util.*;

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
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.DocumentBuilder;
import org.xml.sax.SAXException;
import org.xml.sax.SAXParseException;

public class Main {

    public static void main(String[] args) throws IOException {

	    Properties props = new Properties();
	    props.setProperty("annotators", "tokenize, ssplit, parse, sentiment");
	    PrintWriter out = new PrintWriter (System.out);


	    StanfordCoreNLP pipeline = new StanfordCoreNLP(props);


	    List<Sentence> sentences = XMLReader.readFile("data/test/Laptops_Test_data_phaseB.xml");
	    for (Sentence s : sentences) {
//		    System.out.print(s);


		    Annotation annotation = pipeline.process(s.getText());
		    for (CoreMap sentence : annotation.get(CoreAnnotations.SentencesAnnotation.class)) {
			    Tree tree = sentence.get (SentimentCoreAnnotations.AnnotatedTree.class);
			    List<LabeledScoredTreeNode> list  = tree.getLeaves ();

			    double score = list.get(0).score ();


			    int sentiment = RNNCoreAnnotations.getPredictedClass (tree);

			    System.out.println(s.getText());
			    System.out.println(sentiment);

	        }

	    }

//	    Properties props = new Properties();
//	    props.put("annotators", "tokenize, ssplit, sentiment");
//	    StanfordCoreNLP pipeline = new StanfordCoreNLP(props);
//
//	    // read some text in the text variable
//	    String text = "the quick fox jumps over the lazy dog";
//
//	    // create an empty Annotation just with the given text
//	    Annotation document = new Annotation(text);
//
//	    // run all Annotators on this text
//	    pipeline.annotate(document);
//
//	    // these are all the sentences in this document
//	    // a CoreMap is essentially a Map that uses class objects as keys and has values with custom types
//	    List<CoreMap> sentences = document.get(CoreAnnotations.SentencesAnnotation.class);
//
//	    for(CoreMap sentence: sentences) {
//		    // traversing the words in the current sentence
//		    // a CoreLabel is a CoreMap with additional token-specific methods
//		    for (CoreLabel token: sentence.get(CoreAnnotations.TokensAnnotation.class)) {
//			    // this is the text of the token
//			    String word = token.get(CoreAnnotations.TextAnnotation.class);
//			    // this is the POS tag of the token
//			    String pos = token.get(CoreAnnotations.PartOfSpeechAnnotation.class);
//			    // this is the NER label of the token
//			    String ne = token.get(CoreAnnotations.NamedEntityTagAnnotation.class);
//		    }
//
//		    // this is the parse tree of the current sentence
//		    Tree tree = sentence.get(TreeCoreAnnotations.TreeAnnotation.class);
//
//		    // this is the Stanford dependency graph of the current sentence
//		    SemanticGraph dependencies = sentence.get(SemanticGraphCoreAnnotations.CollapsedCCProcessedDependenciesAnnotation.class);
//	    }

//	    PrintWriter out;
//	    if (args.length > 1) {
//		    out = new PrintWriter(args[1]);
//	    } else {
//		    out = new PrintWriter(System.out);
//	    }
//	    PrintWriter xmlOut = null;
//	    if (args.length > 2) {
//		    xmlOut = new PrintWriter(args[2]);
//	    }
//
//
//	    Properties props = new Properties();
//	    props.put("annotators", "tokenize, ssplit, pos, parse");
//	    AnnotationPipeline pipeline = new StanfordCoreNLP(props);
//
//	    SentimentAnnotator annotator = new SentimentAnnotator ("name", props);
//
//	    Annotation annotation;
//	    if (args.length > 0) {
//		    annotation = new Annotation(IOUtils.slurpFileNoExceptions(args[0]));
//	    } else {
//		    annotation = new Annotation("Kosgi Santosh sent an email to Stanford University. He didn't get a reply.");
//	    }
//
//	    annotator.annotate (annotation);
//	    pipeline.annotate(annotation);
//
//	    pipeline.prettyPrint(annotation, out);
//	    if (xmlOut != null) {
//		    pipeline.xmlPrint(annotation, xmlOut);
//	    }
	    // An Annotation is a Map and you can get and use the various analyses individually.
	    // For instance, this gets the parse tree of the first sentence in the text.
//	    List<CoreMap> sentences = annotation.get(CoreAnnotations.SentencesAnnotation.class);
//	    if (sentences != null && sentences.size() > 0) {
//		    CoreMap sentence = sentences.get(0);
//		    Tree tree = sentence.get(TreeCoreAnnotations.TreeAnnotation.class);
//		    out.println();
//		    out.println("The first sentence parsed is:");
////		    tree.pennPrint(out);
//	    }









    }









}
