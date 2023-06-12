# Projekt-PJF
**Aplikacja web wspierająca rejestrację czasu programisty**

1. Aplikacja posiada interfejs graficzny obsługiwany przez przeglądarkę
2. Korzystanie z aplikacji wymaga od użytkownika zalogowania się
3. Zakończenie pracy wiąże się z wylogowaniem użytkownika
4. Wszystkie dane przechowywane są w bazie danych
5. Aplikacja posiada dwa profile użytkowników
  1. Kierownik
  2. Programista

**Funkcjonalności dla profilu Kierownik:**
1. definiowanie dla całego zespołu Programistów stałych zadań
2. definiowanie stałych zadań dla wybranego Programisty
3. wgląd w wykonane przez Programistę zadania w dowolnie wybranym okresie (wraz z
podsumowaniem łącznego czasu pracy)
4. eksport raportów z realizacji zadań przez poszczególnych programistów w dowolnie
wybranym okresie (wraz z podsumowaniem łącznego czasu pracy)

**Funkcjonalności dla profilu Programista:**
1. rejestracja rzeczywistego (na podstawie zegara systemowego serwera) czasu rozpoczęcia
wykonywania wybranego zadania stałego
2. rejestracja rzeczywistego (na podstawie zegara systemowego serwera) czasu zakończenia
wykonywania wybranego zadania stałego
3. rejestracja rzeczywistego (na podstawie zegara systemowego serwera) czasu rozpoczęcia
wykonywania jednorazowego zadania, którego nie ma w bazie zadań stałych (Programista
samodzielnie formułuje opis zadania)
4. rejestracja rzeczywistego (na podstawie zegara systemowego serwera) czasu zakończenia
wykonywania jednorazowego zadania, którego nie ma w bazie zadań stałych
5. funkcjonalność modyfikowania wszystkich zarejestrowanych czasów - informacja o każdej
takiej modyfikacji jest dostępna wyłącznie dla profilu Kierownik wraz z informacją o
oryginalnej wartości, która została zmodyfikowana.
6. funkcjonalność bieżącego podglądu w wybranym okresie wszystkich zarejestrowanych
zdarzeń związanych z realizacją zadań (wraz z podsumowaniem łącznego czasu pracy)
7. funkcjonalność generowania raportów z wykonanych zadań za okres wybranego
kalendarzowego tygodnia oraz wybranego kalendarzowego miesiąca w formacie .csv, .pdf
oraz .html (wraz z podsumowaniem łącznego czasu pracy)
