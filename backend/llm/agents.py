# agents.py
from langchain_openai import ChatOpenAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langgraph.graph import MessagesState
from config import settings
from utils import filter_reasoning_content

# Initialize the LLM

def get_embeddings_model():
    return GoogleGenerativeAIEmbeddings(
        model="gemini-embedding-001",
        google_api_key=settings.gemini_api_key,
    )

text1 = ''' 
The history of sourdough is a fascinating blend of accidental chemistry and human survival. It represents the oldest form of leavened bread, predating the isolation of commercial yeast by thousands of years.

---

## 1. The Ancient Egyptian Discovery
While flatbreads were common across the Fertile Crescent, sourdough as we know it likely originated in **Ancient Egypt around 3000–2000 BCE**. Historians believe it was a "happy accident." 

* **The Theory:** A mixture of flour and water was likely left out in the warm Egyptian climate. 
* **The Process:** Wild yeast spores and lactic acid bacteria (LAB) from the air and the flour itself settled into the dough, beginning the fermentation process. 
* **The Result:** Instead of a hard flatbread, the dough rose. When baked, it produced a soft, airy loaf with a distinctively complex flavor.



---

## 2. The Science of the "Starter"
The core of sourdough is the **levain** (or starter). Unlike modern bread that uses *Saccharomyces cerevisiae* (baker's yeast) for a rapid rise, sourdough relies on a symbiotic culture:

* **Wild Yeast:** Provides the carbon dioxide for leavening.
* **Lactobacillus:** A genus of bacteria that converts sugars into lactic and acetic acids. This creates the "sour" taste and acts as a natural preservative by lowering the $pH$ of the bread.

Because this culture is living, it can be maintained indefinitely by "feeding" it fresh flour and water. Some bakeries today use starters that are over **100 years old**, passing them down through generations.

---
'''

text2 = ''' 
## 3. The Gold Rush and "Sourdoughs"
Sourdough became a cultural icon during the **Klondike Gold Rush (1896–1899)**. In the freezing wilderness of the Yukon and Alaska, commercial yeast was impossible to keep alive or transport. 

Miners carried their starters in pouches around their necks or slept with them in their bedrolls to keep the cultures warm enough to stay active. These prospectors became so closely identified with the bread that they were nicknamed **"Sourdoughs,"** a term still used to describe veteran Alaskans today.



---

## 4. San Francisco and the *L. sanfranciscensis*
Perhaps no city is more famous for sourdough than San Francisco. During the California Gold Rush of 1849, French bakers noticed that the local sourdough tasted different—more pungent and tangy than elsewhere. 

Decades later, researchers discovered that the specific local environment favored a unique strain of bacteria, eventually named **Lactobacillus sanfranciscensis**. The foggy, temperate climate of the Bay Area provides the ideal "biolayer" for this specific microflora to thrive, making San Francisco sourdough a geographically distinct product.

---

## 5. The Industrial Decline and Modern Revival
With the advent of **commercial yeast** in the late 19th century and the "Chorleywood" industrial bread process in the 1960s, sourdough nearly went extinct in the commercial market because it takes too long to rise (often 12–24 hours). 

However, the late 20th and early 21st centuries saw a massive "artisan" revival. Consumers began seeking out sourdough not just for its flavor, but for its health benefits—the long fermentation process breaks down much of the gluten and phytic acid, making it easier to digest than standard white bread.
'''


def embedding_docs(state: dict):
    embeddings = get_embeddings_model()
      
    # Use embed_documents for a list of strings
    doc_vectors = embeddings.embed_documents([text1, text2])
    print(doc_vectors)
    return {"doc_vectors": doc_vectors}

def chat_process(model="gemma-4-26b-a4b-it", temperature=0.7, timeout=60):
    try:
        llm_chat = ChatOpenAI(
            model=model,
            openai_api_key=settings.gemini_api_key,
            openai_api_base="https://generativelanguage.googleapis.com/v1beta/openai/",
            temperature=temperature,
            max_tokens=120,
            timeout=timeout,
        )
        return llm_chat
    except Exception as e:
        print(f"An error occurred: {e}")
        raise e        
    
llm = ChatOpenAI(
    # model="gemma-3-27b-it",
    model="gemma-4-26b-a4b-it",
    openai_api_key=settings.gemini_api_key,
    openai_api_base="https://generativelanguage.googleapis.com/v1beta/openai/",
    temperature=0.7,
    max_tokens=120,
    timeout=30,
)

def call_model(state: MessagesState):
    """
    Primary agent node that calls the LLM and cleans reasoning tags.
    """
    response = llm.invoke(state["messages"])
    # print(response)
    clean_response = filter_reasoning_content(response)   
    return {"messages": [clean_response]}

def call_model(state: MessagesState):
    """
    Primary agent node that calls the LLM and cleans reasoning tags.
    """
    response = llm.invoke(state["messages"])
    # print(response)
    clean_response = filter_reasoning_content(response)   
    return {"messages": [clean_response]}