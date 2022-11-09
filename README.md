# Inzynierka
Praca inżynierska w ramach studiów na Politechnice Wrocławskiej, wydziale Podstawowych Problemów Techniki (teraz: Informatyki i Telekomunikacji), kierunku Informatyka Algorytmiczna.

## Temat pracy
Implementacja programu **GRAPHPLAN** do
planowania akcji z wykorzystaniem
programowania ograniczeń
Promotorem pracy jest Pan **Doktor Przemysław Kobylański**, któremu serdecznie dziękuję za pomoc 
w doboru planu oraz realizacji pracy.

## Zawartośc repozytorium 

W repozytorium znajduje się sama praca, jak i wszystkie kody źródłowe wykreowane w trakcie jej tworzenia
W folderze ***pictures*** znajduja się wszystkie rysunki wykorzystane do obrazowego przedstawienia głównej problematyki pracy.
W folderze ***sources*** znajdują się pliki źródłowe aplikacji desktopowej, generatora grafów oraz implementacji algorytmu. Dodatkowo w skład tego folderu 
wchodzą wyniki algorytmu w postaci plików tekstowych oraz wygenerowane grafu w postaci plików z rozszerzeniem ***.pdf*** oraz ***.png***
W folderze ***tables*** znajdują się wszystkie tabele użyte w pracy do prezentowania otrzymanych programów w wcześniej spreparowanych środowiskach przez 
implementowany algorytm

## O pracy słów kilka
Praca zawiera w sobie kilka słów o historii planowania przy użyciu komputerów, przedstawia idee przewodnie oraz archetypy, na podstawie których tworzono coraz to bardziej wymyślne algorytmy. W następnych częściach w sposób precyzyjny oraz szczegółowy przedstawiono ideę stojącą za planowaniem akcji metodologią GRAPHPLAN. Dodatkowo wprowadzono formalnie pojęcie programowania ograniczeń, które wykorzystywane jest w celu usprawnienia osiągnieć algorytmu. Ostatni rozdział poświęcony jest testom algorytmu, w skład których wchodzą: Rozwiązywanie łamigłówki piętnastki oraz jej młodszej siostry- ósemki, CargoBot, polegający na przenoszeniu kartonów z odpowiednich półek, zarządzanie ruchem robotów w zdefiniowanej przestrzeni, rozwiązywanie problemu wieży Hanoi, czy N Hetmanów.
Z mniej istotnych rozdziałów- przedstawiono przykładowe sposoby użycia algorytmu, połączenia między komponentami oraz wykorzystane języki jak i technologie w samej implementacji algorytmu. Przedstawiono również implementacje najważniejszych części grafu planującego.

## Co doinstalować:
UWAGA: Poniższe sposoby instalacji poszczególnych komponentów zostały przedstawione dla systemu operacyjnego **UBUNTU**. Korzystając z innych
systemów operacyjnych w trakcie instalowania odpowiednich pakietów należy na własną rękę zapoznać się ze sposobami ich instalacji.
1. SWI-Prolog ()
2. Python3.9 (w **UBUNTU** python jest już domyslnie zainstalowany, można to sprawdzić wpisująć komendę: `python3 --version`)
3. Biblioteka ***graphviz*** dla języka python (`pip install graphviz`)
4. Biblioteka ***PIL*** dla języka python (`pip install Pillow`)
5. Biblioteka ***PySwip*** dla języka python (`pip install pyswip`)

## Jak uruchamiać?

Po przejściu do folderu ***sources*** i wprowadzeniu komendy `python3 gui.py` uruchomiona zostanie aplikacja desktopowa, w której dzieje się cała akcja programu

## Jak używać aplikacji? 
TO-DO

