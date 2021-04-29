# BibliographicErrorFinder
Python-Skript zum Finden von Fehlern in der Bibliographie. Insbesondere werden fehlerhafte Autoren und fehlende Titel erkannt.

Mit diesem Skript können alle XML-Dateien eines Ordners überprüft werden. Dieser Ordner (*directory*) wird im Skript angegeben. Mögliche Ordner:
* entry
* det
* res
* au
* ae
* ae_se

#### Valide XML-Dateien
Das Skript geht davon aus, dass alle XML-Dateien valide sind. Gibt es Probleme beim Lesen einer Datei, wird der Dateiname in der Konsole ausgegeben.

## Ausgabe
Nach der Überprüfung werden drei TSV-Dateien erstellt, die über mögliche Fehler informieren.
* _{entry|det|...}_\_Entries.tsv
  * Vollständige Liste der Entries.
  * _Spalten_: ID, Autor, Titel
* _{entry|det|...}_\_Fehlende\_Titel.tsv
  * Entries, die keinen Titel besitzen.
  * _Spalten_: ID, Autor
* _{entry|det|...}_\_Falscher\_Autor.tsv
  * Entries, bei denen der Autor vermutlich falsch ist. Dies ist zum Einen der Fall, wenn es in einem vorherigen Eintrag einen Autor gibt, aber nicht in diesem. Zum Anderen, wenn der Autor dieses Eintrags in alphabetischer Reihenfolger vor dem Autor des vorherigen Eintrags steht.
  * _Spalten_: ID, Autor, Vorheriger Autor ID, Vorheriger Autor
