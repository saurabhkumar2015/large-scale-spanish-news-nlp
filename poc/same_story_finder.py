import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.chunk import conlltags2tree, tree2conlltags
from pprint import pprint

import spacy
from spacy import displacy
from collections import Counter
import es_core_news_sm
nlp = es_core_news_sm.load()


pattern = 'NP: {<DT>?<JJ>*<NN>}'
cp = nltk.RegexpParser(pattern)

ex1 = "Tras el ataque en la Comandancia Norte de Policía Municipal de Celaya, el juez calificador que fue atacado en el lugar, falleció.El Juez Calificador, identificado solamente por su primer nombre, Francisco, recibió atención médica, pero pese a esto, falleció ante las agresiones que recibió del grupo armado." \
      "También, después del operativo, elementos de Policía Militar, Policía Municipal y Fuerzas de Seguridad del Estado, incautaron dos automóviles, uno de la marca Volvo y una camioneta Ford, color blanco, que tenía impactos de bala." \
      "En el camino de terracería que va de San Elías hasta Santa Teresita, fue detenida una persona. Al parecer, es de las personas del grupo armado que participó en el ataque a la Comandancia."

ex2 = "Las autoridades le marcaron el alto y al revisarlo encontraron un arma de fuego al igual que cartuchos útiles y dos bolsas pequeñas de plástico con un polvo blanco https://www.milenio.com/policia/detienen-a-menor-con-arma-de-fuego" \
      "Esta mañana, en el municipio de León fue detenido un menor de edad que portaba un arma de fuego al igual que al menos nueve cartuchos útiles. https://www.milenio.com/policia/detienen-a-menor-con-arma-de-fuego" \
      "El adolecente circulaba en un auto color rojo, modelo reciente cuando fue detenido por autoridades municipales y estatales. Hasta el momento se desconoce el motivo de la detención, se presume el auto circulaba a exceso de velocidad y realizaba conductas sospechosas. https://www.milenio.com/policia/detienen-a-menor-con-arma-de-fuego" \
      "Las autoridades le marcaron el alto y al realizarle una revisión encontraron un arma de fuego al igual que cartuchos útiles y dos bolsas pequeñas de plástico con un polvo blanco. https://www.milenio.com/policia/detienen-a-menor-con-arma-de-fuego" \
      "Cerca de donde fue detenido el joven se ubican otros fraccionamientos residenciales como Punta del Este, Sierra Nogal, Bosques del Pedregal, entre otros. https://www.milenio.com/policia/detienen-a-menor-con-arma-de-fuego"

ex3 = "El presidente de Estados Unidos dijo que los soldados apuntaron sus armas probablemente como táctica para distracción de los narcotraficantes. https://www.milenio.com/internacional/trump-acusa-soldadados-mexicanos-dispararon-guardias-fronterizos" \
      "El presidente de Estados Unidos, Donald Trump, acusó a soldados mexicanos de apuntar sus armas contra guardias fronterizos y advirtió que eso no debe pasar de nuevo. https://www.milenio.com/internacional/trump-acusa-soldadados-mexicanos-dispararon-guardias-fronterizos" \
      "Autoridades estadunidenses informaron ayer que dos soldados de ese país fueron confrontados por militares mexicanos en una zona remota de Texas, porque pensaron que habían ingresado a México. https://www.milenio.com/internacional/trump-acusa-soldadados-mexicanos-dispararon-guardias-fronterizos" \
      "En Twitter, Trump explicó hoy que probablemente la agresión fue como una táctica para distraer a los narcotraficantes en la frontera. https://www.milenio.com/internacional/trump-acusa-soldadados-mexicanos-dispararon-guardias-fronterizos" \
      "El Comando Norte de Estados Unidos, que administra el respaldo militar para la Oficina de Aduanas y Protección Fronteriza (CBP por sus siglas en inglés), informó que el incidente entre soldados estadunidenses y mexicanos ocurrió el 13 de abril pasado cerca de Clint, Texas. https://www.milenio.com/internacional/trump-acusa-soldadados-mexicanos-dispararon-guardias-fronterizos" \
      "De acuerdo con los reportes, las tropas mexicanas quitaron el arma a uno de los soldados estadunidenses, quienes estaban en un vehículo de la CBP. https://www.milenio.com/internacional/trump-acusa-soldadados-mexicanos-dispararon-guardias-fronterizos" \
      "Después de una breve discusión entre los soldados de ambos países, los militares mexicanos abandonaron el área”, explicó el Comando Norte, que inició una investigación del hecho. https://www.milenio.com/internacional/trump-acusa-soldadados-mexicanos-dispararon-guardias-fronterizos"

ex4 = "El presidente Donald Trump advirtió hoy que acudirá directamente a la Corte Suprema de Estados Unidos \"si los demócratas partidistas\" tratan alguna vez de hacerle un juicio político." \
      "Sin embargo, la estrategia de Trump pudiera encontrarse con un obstáculo: el propio tribunal máximo del país, que en 1993 dijo que los autores de la Constitución nunca tuvieron la intención de que la Corte tuviera el poder para intervenir en un proceso de juicio político." \
      "La Corte Suprema falló entonces que el juicio político y la destitución del presidente corresponden solamente al Congreso." \
      " tuiteó Trump hoy. Agregó que no solamente no hay \"Delitos Graves ni Menores\", una de las bases para un posible juicio político que están expresadas en la Constitución. \"No hay Delitos cometidos por mí en absoluto\", añadió." \
      'Aseguró que los demócratas sí han cometido delitos y que ellos acuden al "Congreso como su última esperanza" porque "Esperamos a Mueller y GANAMOS", en referencia al informe del fiscal especial Robert Mueller sobre la interferencia de Rusia en las elecciones de 2016.' \
      'El informe de Mueller, publicado la semana pasada, reveló que Trump intentó tomar el control de la pesquisa sobre Rusia. En él, Mueller presenta varios momentos en los que Trump instruyó a otras personas para que influyeran o restringieran la investigación tras el nombramiento del fiscal especial en 2017.' \
      'Parece que la advertencia de Trump de acudir directamente a la Corte Suprema significaría una batalla difícil. En su fallo de 1993, el principal juez William Rehnquist escribió que la apelación de un juez federal al juicio político no estaba sujeta a revisión por los tribunales.' \
      'Agregó que los legisladores de la Constitución "no tenían la intención de que las cortes tuvieran el poder de revisar los procesos de juicio político".' \
      'Si las cortes lo pudieran hacer, escribió Rehnquist, podría llevar al país a "meses, o quizás años, de caos".'



def preprocess(sent):
    sent = nltk.word_tokenize(sent)
    sent = nltk.pos_tag(sent)
    return sent

sent1 = preprocess(ex1)
sent2 = preprocess(ex2)


cs1 = cp.parse(sent1)
cs2 = cp.parse(sent2)
print(cs1)
print(cs2)

iob_tagged1 = tree2conlltags(cs1)
pprint(iob_tagged1)

iob_tagged2 = tree2conlltags(cs2)
pprint(iob_tagged2)

ne_tree1 = nltk.ne_chunk(pos_tag(word_tokenize(ex1)))
print(ne_tree1)

ne_tree2 = nltk.ne_chunk(pos_tag(word_tokenize(ex2)))
print(ne_tree2)

doc1 = nlp(ex1)
print('Named Entities for scentence1:')
pprint([(X.text, X.label_) for X in doc1.ents])

doc1_set = set()
for X in doc1.ents:
    doc1_set.add(X.text)
length = len(doc1_set)

doc2 = nlp(ex2)
print('Named Entities for scentence2:')
pprint([(X.text, X.label_) for X in doc2.ents])

score1 =0
for X in doc2.ents:
    if X.text.strip() in doc1_set:
        score1 = score1 + 1

print('Similarity Count of ex1 and ex2 is ', score1)
print('Similarity Ratio of ex1 and ex2 is ', score1 / length)


doc3 = nlp(ex3)
print('Named Entities for scentence3:')
pprint([(X.text, X.label_) for X in doc3.ents])

doc3_set = set()
for X in doc3.ents:
    doc3_set.add(X.text)
length3 = len(doc1_set)

doc4 = nlp(ex4)
print('Named Entities for scentence4:')
pprint([(X.text, X.label_) for X in doc4.ents])

score4 =0
for X in doc4.ents:
    if X.text.strip() in doc3_set:
        score4 = score4 + 1


print('Similarity Count of ex3 and ex4 is ', score4)
print('Similarity Ratio of ex3 and ex4 is ', score4 / length3)
