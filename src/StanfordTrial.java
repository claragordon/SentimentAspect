import java.io.*;
import java.util.*;

import edu.stanford.nlp.io.*;
import edu.stanford.nlp.ling.*;
import edu.stanford.nlp.pipeline.*;
import edu.stanford.nlp.semgraph.SemanticGraph;
import edu.stanford.nlp.semgraph.SemanticGraphCoreAnnotations;
import edu.stanford.nlp.trees.*;
import edu.stanford.nlp.util.*;


public class StanfordTrial{

   public static void main(String[] args) throws IOException {
   String xmlFile = "../data/train/laptop--train.xml";
   List<Sentence> sentences = XMLReader.readFile(xmlFile);
   
   Sentence s = sentences.get(0);
   List<Aspect> list_of_a = s.getAspects();
   Aspect a = list_of_a.get(0);

   StanfordPipeLine p = new StanfordPipeLine();
   String tagged = p.posString(s.getText(), a);
   System.out.println(tagged);
   

   }
      
}