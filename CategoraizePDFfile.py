import os
import re
import PyPDF2

class trieNode:
    def __init__(self):
        self.children = {}
        self.categories = set()

class trie:
    def __init__(self):
        self.root = trieNode()

    def insert(self, phrase, category):
        words = phrase.lower().split()
        node = self.root
        for word in words:
            if word not in node.children:
                node.children[word] = trieNode()
            node = node.children[word]
        node.categories.add(category)

    def search(self, words):
        node = self.root
        for word in words:
            if word in node.children:
                node = node.children[word]
            else:
                return set()
        return node.categories

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    return text.split()

def trie_document_classification(document, Trie, categories):
    words = clean_text(document)
    scores = {category: 0 for category in categories}

    i = 0
    while i < len(words):
        for length in range(3, 0, -1):
            phrase = " ".join(words[i:i + length])
            matchedCategories = Trie.search(phrase.split())

            for category in matchedCategories:
                scores[category] += 1

            if matchedCategories:
                i += length - 1
                break
        i += 1

    bestCategory = "Uncategorized"
    maxCount = 0
    for category, score in scores.items():
        if score > maxCount:
            maxCount = score
            bestCategory = category

    return bestCategory


def read_pdf_file(filePath):
    # Check if the file is a PDF
    if filePath.lower().endswith(".pdf"):
        try:
            with open(filePath, "rb") as file:
                reader = PyPDF2.PdfReader(file)
                text = ""
                for page_num in range(len(reader.pages)):
                    page = reader.pages[page_num]
                    text += page.extract_text()
                return text
        except Exception as e:
            print(f"Error reading PDF file: {e}")
            return None
    else:
        print("Error: The file is not a PDF.")
        return None

categories = {
    "Technology": ["computer", "software", "AI", "Data", "Information", "machine learning", "ML", "programming", "cloud computing", "iot", "data science", "cybersecurity", "virtual reality", "blockchain", "networking", "app development", "robotics", "C++", "Python", "Code", "Java", "Innovation", "System", "Devices", "Developer", "Algorithm", "Library", "Framework", "Debugging", "Databases", "Database", "Server", "PHP", "JavaScript", "CSS", "HTML", "Protocols", "Infrastructure", "Deep Learning", "Reinforcement Learning", "Ethical Hacking", "Cloud Computing", "Cyber Attack"],
    "Sports": ["football", "basketball", "tennis", "player", "coach", "team", "training", "stadium", "referee", "match", "athlete", "tournament", "swimming", "cricket", "Competition","Loss", "Win", "Training", "Performance", "Strategy", "Analysis", "Tactics", "Injury", "Recovery", "Season", "Results", "Goals", "Records", "Forward", "Defender", "Team Captain", "Level", "Rival", "Formula 1", "Car Racing", "Fitness", "Exercises", "Endurance", "Strength", "Training Program", "Rest", "Training Techniques", "Willpower", "League", "Qualifiers", "Medal", "Semi-Final", "Professional Athlete"],
    "Health": ["medicine", "doctor", "hospital", "treatment", "nutrition", "exercise", "mental health", "disease", "surgery", "therapy", "wellness", "diet", "healthcare", "vaccination", "nurse", "patient", "Recovery", "Immunity", "Prevention", "Diagnosis", "Cancer", "Diabetes", "Blood Pressure", "Inflammation", "Protein", "Vitamins", "BMI", "Insulin Resistance", "Preventive Measures", "Influenza", "Stomach", "Liver", "Brain", "Heart Disease", "Arthritis", "Asthma", "Stroke", "Migraine"],
    "Physics": ["Force", "Energy", "Matter", "Mass", "Velocity", "Acceleration", "Rate", "Motion", "Gravity", "Resistance", "Pressure", "Dynamics", "Mechanics", "Electricity", "Magnetism", "Wave", "Sound Waves", "Light Waves", "Electromagnetic Waves", "Heat", "Time", "Vacuum", "Relativity", "Quantum Mechanics","Planck's Constant", "Gravitational Constant", "General Relativity", "Momentum", "Newton's Law", "Heisenberg's Uncertainty Principle", "Law of Thermodynamics", "Conservation of Energy"],
    "Chemistry": ["Chemistry", "Compound", "Element", "Molecule", "Substance", "Ion", "Oxidation", "Atom", "Reduction", "Solution", "Density", "Organic Chemistry", "Inorganic Chemistry", "Covalent Bond", "Metallic Bond", "Ionic Bond", "Hydrogen Bond", "Liquid", "Solid", "Ideal Gas Law", "Charles' Law", "Boyle's Law", "Periodic Table", "Metals", "crystal lattice", "volatic cells", "heat of fusion", "Melting", "freezing", "sublimation", "Non-metals", "Metalloids", "Alkanes", "Alkenes", "Alkynes", "Molar mass", "stoichiomestry", "Enthalpy", "calorimetry", "intromolecular forces", "Dipole-dipole", "London forces", "Hydrogen bonding", "Redox Reactions", "Electrolytic Cells", "Thermodynamics", "Heat of vaporization", "Esters", "Amines", "Concentration of Reactants", "Precipitation Reaction", "Acid-Base Reaction", "Crystalline", "Electrochemistry", "Acids", "Oxidation", "Mole", "Reduction"],
    "Mathematics": ["algebra", "geometry", "calculus", "equation", "Equations", "statistics", "probability", "trigonometry", "integrals", "derivatives", "functions", "number theory", "logic", "combinatorics", "Number", "Constant", "Ratio", "Decimal", "Percentage", "Square Root", "set", "Probability", "Linear Equation", "Quadratic Equation", "Differential Equations", "Exponent", "Vectors", "Triangle", "Circle", "Rectangle", "Square", "Spherical", "Angle", "Pythagorean Theorem", "Coordinates", "Derivative", "Integral", "Partial Derivative", "Definite Integral", "Indefinite Integral", "Probability Distribution", "Sample", "Prime Number", "Union", "Intersection", "Relation"],
    "History": ["ancient", "medieval", "modern", "war", "civilization", "revolution", "empire", "kingdom", "timeline", "archaeology", "dynasty", "battle", "colonialism", "history", "Time Period", "Era", "Past", "Future", "Assyrians", "Sumer", "Pharaohs", "Greeks", "Roman Empire", "Persian Empire", "Phoenicians", "Middle Ages", "Crusades", "Abbasid Caliphate", "Umayyad Caliphate", "Vikings", "Catholic Church", "Feudalism", "Feudal Wars", "Reformation", "Renaissance", "French Revolution", "Colonialism", "British Empire", "World War I", "World War II", "Independence Movements", "Age of Enlightenment", "Modernism", "Postmodernism"],
    "Economics": ["market", "supply", "demand", "currency", "inflation", "gdp", "unemployment", "recession", "taxation", "trade", "business", "investment", "capital", "Money", "Investment", "Income", "Recession", "Price Index", "Market Equilibrium", "Taxes", "Budget Surplus", "Budget Deficit", "Monetary Policy", "Currency", "Utility", "Monopoly", "Fixed Costs", "Price Determination", "World Trade Organization", "WTO", "Stocks", "Investing"],
    "Languages": ["english", "spanish", "french", "grammar", "vocabulary", "language learning", "phonetics", "pronunciation", "sentence structure", "translation", "conjugation", "linguistics", "dialects", "Pronunciation", "Interpretation", "Spelling", "Syntax", "Morphology", "Semantics", "Listening", "Reading", "Speaking", "Noun", "Adjective", "Verb"],
    "Psychology": [ "Mind", "behavior", "cognition", "emotion", "therapy","memory", "counseling", "neuroscience", "social psychology", "personality", "clinical psychology", "developmental psychology", "Consciousness", "Behavior", "Motivation", "Thinking", "Decision Making", "Strategic Thinking", "Anxiety", "Calmness", "Depression", "Personality Types", "Psychopathology", "Personality Traits", "Schizophrenia", "Hallucinations", "OCD", "Social Roles", "Psychological Research"],
}

Trie = trie()
for category, keywords in categories.items():
    for keyword in keywords:
        Trie.insert(keyword, category)


filePath = input("enter your pdf file path: ")
document = read_pdf_file(filePath)

if document:
    result = trie_document_classification(document, Trie, categories)
    print("\ncategory are: ", result)