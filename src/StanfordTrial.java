import java.io.*;
import java.util.*;

import edu.stanford.nlp.io.*;
import edu.stanford.nlp.ling.*;
import edu.stanford.nlp.pipeline.*;
import edu.stanford.nlp.semgraph.SemanticGraph;
import edu.stanford.nlp.semgraph.SemanticGraphCoreAnnotations;
import edu.stanford.nlp.trees.*;
import edu.stanford.nlp.util.*;

public class StanfordTrial {

   public static void main(String[] args) throws IOException {
       // creates a StanfordCoreNLP object, with POS tagging, lemmatization, NER, parsing, and coreference resolution 
       Properties props = new Properties();
       props.put("annotators", "tokenize, ssplit, pos, lemma, ner, parse");
       StanfordCoreNLP pipeline = new StanfordCoreNLP(props);
       
       // read some text in the text variable
       String text = "This is my text sentence."; // Add your text here!
       
       // create an empty Annotation just with the given text
       Annotation document = new Annotation(text);
       
       // run all Annotators on this text
       pipeline.annotate(document);    
       
       // these are all the sentences in this document
       // a CoreMap is essentially a Map that uses class objects as keys and has values with custom types
       List<CoreMap> sentences = document.get(SentencesAnnotation.class);
       
//        for(CoreMap sentence: sentences) {
//          // traversing the words in the current sentence
//          // a CoreLabel is a CoreMap with additional token-specific methods
//           for (CoreLabel token: sentence.get(TokensAnnotation.class)) {
//               // this is the text of the token
//               String word = token.get(TextAnnotation.class);
//               // this is the POS tag of the token
//               String pos = token.get(PartOfSpeechAnnotation.class);
//               // this is the NER label of the token
//               String ne = token.get(NamedEntityTagAnnotation.class);       
//             }
//        }
 
 
 
   }
}