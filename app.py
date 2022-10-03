# Import libraries needed for keyword extraction
import spacy
import random

# Import libraries needed for rest of program
from cs50 import SQL
from flask import Flask, render_template, request
from helpers import keywords

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///world_data.db")

# Load library needed for keyword extraction
nlp = spacy.load("en_core_web_lg")

# Define list of pre-determined keywords for each musical key
# Adapted from https://ledgernote.com/blog/interesting/musical-key-characteristics-emotions/
keys = [{"love", "unhappy", "sad", "lovesick", "languish", "longing", "lost", "search", "relationship", "cry", "frown", "yearn", "languish", "distress", "long"},
        {"innocent", "innocence", "happy", "pure", "naivety", "naive", "simplicity", "simple", "children", "child", "imagination", "earnest", "resolve", "religious", "imagine", "moral", "righteous", "virgin", "modest"},
        {"sorrow", "grief", "punishment", "penance", "wrongdoing", "forgiveness", "despair", "sad", "wail", "weep", "cry", "punish", "hit", "damage", "pain", "damnation", "penalty", "discipline", "justice"},
        {"sadness", "sad", "tears", "despair", "sonority", "tone", "euphony", "grief", "depression", "depressed", "hide", "choke", "grimace", "rapture", "sorrow", "heartbreak", "mourn"},
        {"serious", "pious", "ruminate", "melancholy", "feminine", "worry", "negativity", "negative", "pessimistic", "think", "consider", "muse", "ponder", "thought", "deliberate"},
        {"triumphant", "victory", "scream", "rejoice", "war", "holiday", "invitation", "win", "triumph", "achieve", "conquest", "game", "master", "beat", "supreme", "success", "vanqiush"},
        {"distress", "angst", "anxiety", "terror", "depression", "depressed", "dark", "fear", "hestiation", "shuddering", "goosebumps", "ghosts", "sad", "Halloween", "scary", "melancholy", "woe", "gloom", "dark"},
        {"cruel", "hard", "love", "devotion", "intimacy", "openness", "honesty", "god", "tough", "brutal", "savage", "vicious", "ferocious", "fierce", "murder", "kill", "homicide", "blunt"},
        {"effeminate", "amorous", "restless", "grief", "mournful", "restless", "princess", "lock", "wait", "patience", "edge", "uneasy", "nervous", "tense", "tower", "nerve", "uptight", "broke"},
        {"quarrelsome", "boisterous", "pleasure", "joy", "delight", "bickering", "fight", "punch", "dispute", "argue", "confront", "combat", "military", "gun", "sword", "knife", "kill", "fire", "shot", "shoot"},
        {"obscure", "plaintive", "funereal", "depression", "lament", "death", "loss", "misery", "harrowing", "melancholic", "demise", "departure", "pass", "rest", "eternal", "disease", "sad"},
        {"furious", "temper", "regret", "complaisance", "explosion", "angry", "composed", "religion", "boil", "control", "fuse", "fight", "pent", "tense", "fiery", "impatience", "impatient", "restless"},
        {"gloomy", "passionate", "resentment", "crying", "lamentation", "discontent", "power", "cry", "regret", "fire", "remorse", "sorrow", "sad", "repent", "guilt", "condemn", "dejection", "unhappy", "lament"},
        {"difficulty", "relief", "triumph", "victory", "rest", "clarity", "relax", "recline", "leisure", "win", "rejoice", "joy", "achieve", "ascend", "master", "landslide", "coup", "superior", "trounce", "beat"},
        {"discontent", "uneasiness", "worry", "concern", "struggle", "dislike", "teeth", "grind", "fret", "agonize", "brood", "bother", "trouble", "distress", "disturb", "perturb", "nerve", "fear", "stress", "dread"},
        {"serious", "magnificent", "fantasy", "rustic", "idyllic", "poetic", "lyrical", "calm", "satisfaction", "tenderness", "gratitude", "friendship", "faith", "gentle", "peace", "devotion", "goodwill", "harmony", "intimacy"},
        {"grumbling", "moaning", "wailing", "suffocation", "lament", "struggle", "negative", "competition", "smother", "choke", "strangle", "throttle", "stifle", "compete", "ruthless", "fierce", "cutthroat"},
        {"death", "eternity", "putrefaction", "ghosts", "ghouls", "goblins", "graveyards", "haunting", "lingering", "cosmos", "dark", "universe", "judgment", "judge", "supernatural", "weird", "eternal"},
        {"tender", "plaintive", "pious", "womanly", "graceful", "soothing", "calm", "elegant", "sophisticated", "dignified", "dignity", "poise", "poised", "fashion", "culture", "cultured", "style", "lovely", "fluid", "exquisite"},
        {"joy", "love", "innocence", "satisfaction", "optimistic", "belief", "heaven", "youthful", "cheerful", "trusting", "happy", "jolly", "bright", "sun", "joyful", "spirit", "spark", "sparkling", "bubble", "bubbles"},
        {"terrible", "mocking", "night", "surly", "blasphemous", "end", "pessimism", "defeat", "darkness", "dread", "awful", "appalling", "horror", "horrified", "terrify", "frightful", "fright", "atrocious", "abominable", "shock"},
        {"joyful", "quaint", "cheerful", "love", "conscience", "hopeful", "aspiration", "future", "optimistic", "peace", "optimism", "positive", "bright", "bubble", "bubbly", "hope", "encouragement", "promise", "promising", "favor", "favorable"},
        {"solitary", "melancholy", "patience", "fate", "destiny", "submission", "karma", "providence", "aura", "feeling", "end", "kismet", "damnation", "wait", "patient",  "end", "final", "finality", "conclusion", "terminate", "finish"},
        {"harsh", "strong", "wild", "rage", "passion", "angry", "jealous", "fury", "despair", "burden", "negative", "energy", "fight", "temper", "tantrum", "rant", "boil", "fit", "blowout", "moody", "desire", "aggressive", "aggression"}]
   
# Define global variables needed for Data
popAvg = 0
valAvg = 0.0
tempAvg = 0.0

# Render homepage
@app.route("/")
def index():
    """Returns the homepage."""
    return render_template("index.html")

# Render about page
@app.route("/about")
def about():
    "Returns the about page."
    return render_template("about.html")

# Render get started page
@app.route("/getstarted", methods=["GET", "POST"])
def getstarted():
    """Allows users to submit a form necessary for generating the playlist."""
    # If request method was by post
    if request.method == "POST":
        text = request.form.get("text")
        dance = int(request.form.get("dance"))
        energy = int(request.form.get("energy"))

        # List of keywords, but remove duplicates
        setKeys = set(keywords(text))

        # Keep track of which keys the keywords occur in
        keyTracker = [0]*24
        for keyWord in setKeys:
            for i in range(24):
                if keyWord in keys[i]:
                    keyTracker[i] += 1
        
        # Extract actual key needed, convert key to SQL database format
        maxVal = max(keyTracker)
        maxIndices = []
        for i in range(24):
            if keyTracker[i] == maxVal:
                maxIndices.append(i)
        random.shuffle(maxIndices) 
        chosenKey = maxIndices[0]
        key1 = chosenKey // 2
        mode = 0
        if chosenKey % 2 == 1:
            mode = 1

        # SQL Query based on user input
        table = db.execute("SELECT track_name, artist_name, popularity, valence, tempo FROM mytable WHERE key = ? AND mode = ? AND (danceability BETWEEN ? AND ?) AND (energy BETWEEN ? AND ?) ORDER BY RANDOM() LIMIT 15", 
                           key1, mode, dance/10 - 0.15, dance/10 + 0.15, energy/10-0.15, energy/10+0.15)

        # Calculate data
        length = len(table)
        global popAvg
        global valAvg
        global tempAvg

        # Calculate averages
        for item in table:
            popAvg += item["popularity"]
            valAvg += item["valence"] * 100
            tempAvg += item["tempo"]

        # Round to two decimal places
        popAvg = round((popAvg / length), 2)
        valAvg = round((valAvg / length), 2)
        tempAvg = round((tempAvg / length), 2)
        
        # Render template 
        return render_template("results.html", table=table)
    else:
        # Render template
        return render_template("getstarted.html")

# Render Data page
@app.route("/data")
def data():
    return render_template("data.html", popAvg=popAvg, valAvg=valAvg, tempAvg=tempAvg)