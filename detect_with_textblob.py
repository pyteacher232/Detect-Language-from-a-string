from iso639 import languages
from textblob import TextBlob

str = "156-315.71 Check Point Security Expert R71 Practice  Exam"
try:
    language = languages.get(alpha2=TextBlob(str).detect_language()).name
except:
    language = ""

print(language)