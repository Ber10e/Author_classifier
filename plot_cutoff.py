"""Dummy voorbeeld hoe je een plot van je scores kunt genereren. Vereist matplotlib.
"""

from pylab import *


cutoff = [1,2,3,4,5,6,7]              # getallen op de X-as

score1 = [34.5,44.5,45,46,47,46,44]   # Te plotten reeks. Je kan zoveel reeksen plotten als je wilt.
score2 = [44.5,54.5,56,64,76,60,54]

plot(cutoff, score1, linewidth=1.0,label='reeks1')   #Scores worden geplot. Elke reeks krijgt automatisch een andere kleur.
plot(cutoff, score2, linewidth=1.0,label='reeks2')   #Labels worden in de legende weergegeven.

legend()
xlabel('cut-off')                       #Onderschrift X-as
ylabel('accuracy scores (%)')           #Onderschrift Y-as
title('Impact van frequentie cut-offs') #Titel van je plot
grid(True)
savefig("test.png")                    #Sla een png van figuur in dezelfde directory als dit script op
show()
