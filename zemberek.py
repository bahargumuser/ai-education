import jpype
import jpype.imports
from jpype.types import JString
from jpype import JPackage
import json

# Specify the path to the Zemberek jar file / Zemberek JAR dosyasının yolunu belirtin
zemberek_jar_path = "zemberek-full.jar"

def start_jvm():
    if not jpype.isJVMStarted():
        print("Starting JVM...")
        jpype.startJVM(classpath=[zemberek_jar_path])
        print("JVM started.")

def shutdown_jvm():
    if jpype.isJVMStarted():
        print("Shutting down JVM...")
        jpype.shutdownJVM()
        print("JVM shut down.")

def get_root_words(sentence):
    start_jvm()
    
    # Import the Zemberek classes / Zemberek sınıflarını içe aktarın
    TurkishMorphology = JPackage('zemberek').morphology.TurkishMorphology
    morphology = TurkishMorphology.createWithDefaults()
    analysis = morphology.analyzeSentence(JString(sentence))
    
    roots = []
    for word_analysis in analysis:
        for single_analysis in word_analysis.getAnalysisResults():
            root = single_analysis.getLemmas()[0]
            roots.append(root)
    
    # shutdown_jvm()
    
    return roots

def load_synonyms(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        synonyms_dict = json.load(f)
    return synonyms_dict

def find_synonyms(roots, synonyms_dict):
    synonyms = {}
    for root in roots:
        if root in synonyms_dict:
            synonyms[root] = synonyms_dict[root]
        else:
            synonyms[root] = []
    return synonyms

# Load the synonyms dictionary from the json file / Eş anlamlılar sözlüğünü JSON dosyasından yükle
synonyms_dict = load_synonyms("synonyms.json")

# Örnek cümle
sentence = "vizyondaki filmler"
roots = get_root_words(sentence)
print("Kökler:", roots)

# Eş anlamlıları bul
synonyms = find_synonyms(roots, synonyms_dict)
print("Eş anlamlılar:", synonyms)
