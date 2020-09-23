#Step III: BUILD DMN
#Generate DRD as DMN'compatible XML
from lxml import etree

# create XML
header = """<?xml version="1.0" encoding="UTF-8"?>"""
root = etree.Element('definitions')

#inputdata or base concepts
baseconcepts = ["Height", "Weight"] #nouns
derivedconcepts = ["BMI Value"] #nouns
actions = ["Calculated"] #verbs
decisionaction = ["Calculate BMI Value"] #verb+noun
dependencies = [["Calculate BMI Value","BMI Value",["Height","Weight"]]] #action, output, inputs

i = 1
for bc in baseconcepts:
   inputdata = etree.Element('inputdata')
   inputdata.set("id", "InputData"+str(i))
   inputdata.set("name", bc)
   root.append(inputdata)
   i = i + 1

i = 1;
#outputs or derived concepts
for dc in derivedconcepts:
   output = etree.Element('output')
   output.set("id", "OutputData"+str(i))
   output.set("name", dc)
   root.append(output)
   i = i + 1

#decisions
i = 1
for dep in dependencies:
   decision = etree.Element('decision')
   decision.set("id", "Decision"+str(i))
   decision.set("name", dep[0])
   decision.set("output", dep[1])
   for ip in dep[2]: #information requirement or dependencies
        informationRequirement = etree.Element('informationRequirement')
        requiredInput =  etree.Element('requiredInput')
        requiredInput.set("name", ip)
        informationRequirement.append(requiredInput)
        decision.append(informationRequirement)
   root.append(decision)
   i = i + 1

# pretty string
s = header +'\n'+ etree.tostring(root, pretty_print=True, encoding="unicode")
print(s)
