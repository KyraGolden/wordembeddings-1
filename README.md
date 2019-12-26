# wordembeddings

Bemerkungen / Anweisungen:
Verzeichnisstruktur beibehalten.
def application: Pfad, für den Aufruf der Funktion get_synonyms muss angepasst werden. 
Je nach Eingabe des Benutzers liest das Programm ein anderes Vektorfile. Diese müssen separat erstellt werden auf dem Server, in diesem Repo befindet sich nur ein Exemplar, short.cc.de.300.vec, welches die ersten 1000 Vektoren des Originals cc.de.300.vec beinhaltet.
Für den quickSearch wird ein File mit dem Namen 10000.cc.de.300.vec eingelesen. Es ist vorgesehen, dass es die ersten 10'000 Vektoren des Originals enthält.
Für den longSearch wird eni File mit dem Namen 50000.cc.de.300.vec eingelesen. Es ist vorgesehen, dass es die ersten 50'000 Vektoren des Originals enthält.
Die Wörter in den Vektorfiles sind nach häufigstem Vorkommen sortiert.
