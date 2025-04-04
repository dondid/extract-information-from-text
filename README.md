# extract-information-from-text
https://github.com/user-attachments/assets/96cd6423-8d5d-429b-9083-2b6646f5fceb

# Ghid de utilizare al programului Extractor de Email-uri:
1. Extragere nume utilizator și companie:
   - Introduceți un text care conține o adresă de email sau folosiți butonul "Import din fișier"
   - Apăsați butonul "Analizează"
   - Rezultatele vor afișa numele utilizatorului și numele companiei

2. Extragere toate email-urile:
   - Introduceți un text care conține una sau mai multe adrese de email sau folosiți butonul "Import din fișier"
   - Selectați tipul de pattern dorit:
     * standard - detectează majoritatea formatelor de email
     * strict - doar formate standard cu litere, cifre și câteva caractere speciale
     * relaxat - acceptă o gamă mai largă de caractere speciale
   - Apăsați butonul "Analizează"
   - Toate adresele de email găsite vor fi afișate în lista de rezultate
   - Puteți copia sau exporta adresele găsite

3. Funcționalități avansate:
   - Introduceți text care conține email-uri, numere de telefon și/sau URL-uri sau folosiți butonul "Import din fișier"
   - Selectați opțiunile dorite pentru fiecare tip de extragere
   - Apăsați butonul "Analizează"
   - Verificați rezultatele în tab-urile corespunzătoare

4. Import din fișier:
   - Fiecare secțiune permite importul textului din fișiere externe
   - Formate suportate: .txt (întotdeauna)
   - Format opțional: .docx (necesită biblioteca python-docx)
   - Format opțional: .pdf (necesită biblioteca PyPDF2)

# Expresii regulate (Regex) - noțiuni de bază:

Metacaractere importante:
- . : orice caracter cu excepția newline
- ^ : începutul șirului
- $ : sfârșitul șirului
- * : zero sau mai multe repetiții
- + : una sau mai multe repetiții
- ? : zero sau o repetiție
- [] : clasă de caractere (ex: [a-z] = orice literă mică)
- | : alternativă (sau)

Secvențe speciale:
- \d : cifre [0-9]
- \w : caractere de cuvânt [a-zA-Z0-9_]
- \s : spații albe (spațiu, tab, newline)

Pattern pentru email:
Un pattern simplu pentru email este: [\w.-]+@[\w.-]+\.[\w]+
Acesta identifică:
- Nume utilizator: litere, cifre, puncte și cratime
- @ : simbolul standard
- Domeniu: litere, cifre, puncte și cratime
- .extension: punctul urmat de extensie (com, ro, org, etc.)

Pentru informații mai detaliate despre expresii regulate, accesați:

https://docs.python.org/3/library/re.html

https://pycon2016.regex.training/regex-intro
