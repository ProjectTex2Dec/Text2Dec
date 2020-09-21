#############################################################
# TEXT2DEC DECISION MODEL EXTRACTOR #########################
#############################################################
# First import the full model extractor
from text2dec.text2dec import *

# ---- Step 1: Make a spacy document of the texual description
doc = sp("If the day is rainy, sell waffles.")

# ---- Step 2: Extract decision model deom text using Text2Dec
drd = dep_extractor(doc)

#############################################################
# TEXT2DEC INDIVIDUAL STAGES DEMO ###########################
#############################################################
