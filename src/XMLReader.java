import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.DocumentBuilder;

import org.xml.sax.SAXException;
import org.xml.sax.SAXParseException;

import java.io.File;
import java.util.ArrayList;
import java.util.List;

import org.w3c.dom.Document;
import org.w3c.dom.*;

/**
 * @author Clara Gordon
 */

public class XMLReader{

	public static List<Sentence> readFile (String filename){

		List<Sentence> sentences = new ArrayList<Sentence> ();

		try {

			DocumentBuilderFactory docBuilderFactory = DocumentBuilderFactory.newInstance();
			DocumentBuilder docBuilder = docBuilderFactory.newDocumentBuilder();
			Document doc = docBuilder.parse (new File(filename));

			// normalize text representation
			doc.getDocumentElement ().normalize ();
			NodeList sentenceNodes = doc.getElementsByTagName("sentence");

			String docId;
			String text;
			String aspectTerm;
			int start;
			int end;
			boolean polarity;
			ArrayList<Aspect> aspects;

			for(int s=0; s<sentenceNodes.getLength() ; s++){

				Node sentenceNode = sentenceNodes.item(s);
				if(sentenceNode.getNodeType() == Node.ELEMENT_NODE){

					Element sentenceElement = (Element)sentenceNode;
					docId = sentenceElement.getAttribute ("id");

					// extract text
					Element textElement = (Element)sentenceElement.getElementsByTagName("text").item(0);
					text = ((Node)textElement.getChildNodes().item(0)).getNodeValue().trim();

					Element aspectElement = (Element)sentenceElement.getElementsByTagName("aspectTerms").item (0);


					if (aspectElement != null)	{
						NodeList aspectTermNodes = aspectElement.getElementsByTagName ("aspectTerm");
						aspects = new ArrayList<Aspect> ();

						for (int i = 0; i < aspectTermNodes.getLength (); i ++) {
							NamedNodeMap aspectElements = aspectTermNodes.item (i).getAttributes();
							aspectTerm = aspectElements.getNamedItem ("term").getTextContent ();
							start = Integer.parseInt (aspectElements.getNamedItem ("from").getTextContent ());
							end = Integer.parseInt (aspectElements.getNamedItem ("to").getTextContent ());

							aspects.add(new Aspect(aspectTerm, start, end));
						}

						for (Aspect a : aspects) {
							sentences.add(new Sentence(text, docId, aspects));
						}
					}
				}
			}


		}catch (SAXParseException err) {
			System.out.println ("** Parsing error" + ", line "
					                    + err.getLineNumber () + ", uri " + err.getSystemId ());
			System.out.println(" " + err.getMessage ());

		}catch (SAXException e) {
			Exception x = e.getException ();
			((x == null) ? e : x).printStackTrace ();

		}catch (Throwable t) {
			t.printStackTrace ();
		}


// 		for (Sentence s: sentences) {
// 			System.out.print(s);
// 		}

		return sentences;

	}

}
