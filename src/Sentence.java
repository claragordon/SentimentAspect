import java.util.HashMap;
import java.util.HashSet;
import java.util.List;

/**
 * @author Clara Gordon
 */
public class Sentence {

	private String text;
	private String docId;
	private List<Aspect> aspects;

	public Sentence(String text, String docId, List<Aspect> aspects) {
		this.text = text;
		this.docId = docId;
		this.aspects = aspects;
	}


	public String getText() {
		return this.text;
	}

	public String docId() {
		return this.docId;
	}

	public List<Aspect> getAspects() {
		return this.aspects;
	}

	public String toString()  {

		String returnString =  ("Text: \"" + text + "\" DocId: " + docId);
		for (Aspect a : aspects) {
			returnString += "\n\t" + a;
		}
		int a;
		return returnString + "\n";

	}


}