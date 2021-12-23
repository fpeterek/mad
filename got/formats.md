## CSV

Pouze názvy uzlů a ke každému uzlu ceny hran vedoucích do všech dalších uzlů
(0 pokud hrana neexistuje), ale nic ke grafické reprezentaci grafu.

## GDF

Obsahuje data o uzlech (stupeň, komunitu), hrany mezi uzly, ale také data umožňující
rekonstrukci grafické reprezentace grafu (původní barvy, původní pozice, apod.)

## GEXF

Podobně jako GDF, ale data jsou zapsána ve formátu XML, což mimochodem umožňuje lepší
rozdělení dat o uzlech a metadat sloužících pouze k vizualizaci.

## GML

Podobně jako GEXF, obsahuje data o uzlech i metadata využitelná k vykreslení původní
grafické reprezentace. Definuje ale vlastní stromový formát, méně elokventní než je XML.

