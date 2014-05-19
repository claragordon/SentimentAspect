import java.io.*;
import java.util.*;
/*
import edu.stanford.nlp.dcoref.CorefChain;
import edu.stanford.nlp.dcoref.CorefCoreAnnotations;
import edu.stanford.nlp.io.*;
import edu.stanford.nlp.ling.*;
import edu.stanford.nlp.pipeline.*;
import edu.stanford.nlp.semgraph.SemanticGraph;
import edu.stanford.nlp.semgraph.SemanticGraphCoreAnnotations;
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
    
      List<Sentence> sentences = XMLReader.readFile("../data/train/Laptop_Train_v2.xml");
      
      Sentence s = sentences.get(3);
      System.out.println(s.getText());
      
     
//       String[] split = s.getText().split("\\s+");
//       for (String w : split){
//          System.out.println(w);
//       }
      
      for (Aspect a : s.getAspects()){
         System.out.println("ASPECT: " + a.getText());
         String[] parts = s.getText().split(a.getText());
         
         List front_ngrams = ngrams(1, parts[0]);
         if (front_ngrams.size() > 5){
            for (int i = 1; i < 6; i++){
            
               String target = front_ngrams.get(front_ngrams.size() - i);
               features.put(target, features.get(target)+1);
               System.out.println(front_ngrams.get(front_ngrams.size() - i));
               
            }
         }
         else{
            for (int i = 1; i < front_ngrams.size()+1; i++){
               System.out.println(front_ngrams.get(front_ngrams.size() - i));
            }
         }
         
         List ngrams = ngrams(1, parts[1]);
         if (ngrams.size() > 5){
            for (int i = 1; i < 6; i++){
               System.out.println(ngrams.get(i));
            }
         }
         else{
            for (int i = 1; i < ngrams.size()+1; i++){
               System.out.println(ngrams.get(i));
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
      
      
// 	    for (Sentence s : sentences) {
// 		    System.out.print(s.getDocId());
// 	    }

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
