import re
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import webbrowser
from datetime import datetime
from tkinter import filedialog
import os

try:
    import docx

    docx_available = True
except ImportError:
    docx_available = False

try:
    from PyPDF2 import PdfReader

    pdf_available = True
except ImportError:
    pdf_available = False


class EmailExtractorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Extractor de Email-uri")
        self.root.geometry("800x700")
        self.root.minsize(600, 500)

        try:
            icon_image = tk.PhotoImage(file="inf.png")
            self.root.iconphoto(True, icon_image)
        except:
            pass

        # Setări de stil
        self.style = ttk.Style()
        self.style.theme_use("clam")  # Temă modernă
        self.style.configure("TButton", font=("Segoe UI", 10), padding=6)
        self.style.configure("TLabel", font=("Segoe UI", 10))
        self.style.configure("Header.TLabel", font=("Segoe UI", 12, "bold"))
        self.style.configure("SubHeader.TLabel", font=("Segoe UI", 11))

        # Culori
        self.bg_color = "#f0f0f0"
        self.accent_color = "#3498db"
        self.header_color = "#2c3e50"
        self.root.configure(bg=self.bg_color)

        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        # Creare taburi pentru funcționalități
        self.tab_control = ttk.Notebook(self.root)

        # Tab pentru Exercițiul 1
        self.tab1 = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab1, text="Extragere Nume & Companie")

        # Tab pentru Exercițiul 2
        self.tab2 = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab2, text="Extragere Toate Email-urile")

        # Tab pentru Funcționalități Avansate
        self.tab3 = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab3, text="Funcționalități Avansate")

        # Tab pentru Ajutor & Informații
        self.tab4 = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab4, text="Ajutor & Info")

        self.tab_control.pack(expand=1, fill="both", padx=10, pady=10)

        self.tab_control.pack(expand=1, fill="both", padx=5, pady=5)

        # Inițializare conținut taburi
        self.init_tab1()
        self.init_tab2()
        self.init_tab3()
        self.init_tab4()

        # Bara de stare
        self.status_bar = ttk.Label(self.root, text=f"© {datetime.now().year} - Program Extractor Email-uri",
                                    relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def create_scrollable_frame(self, parent):
        """Create a scrollable frame that adapts to window size"""
        # Create a canvas with scrollbar
        canvas = tk.Canvas(parent)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        # Configure the canvas
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Pack the canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        return scrollable_frame

    def import_file(self, text_widget):
        """Importă text dintr-un fișier extern"""
        filetypes = [
            ("Fișiere text", "*.txt"),
            ("Toate fișierele", "*.*")
        ]

        # Adaugă opțiuni pentru Word dacă biblioteca docx este disponibilă
        if docx_available:
            filetypes.insert(1, ("Documente Word", "*.docx"))

        # Adaugă opțiuni pentru PDF dacă biblioteca PyPDF2 este disponibilă
        if pdf_available:
            filetypes.insert(1, ("Fișiere PDF", "*.pdf"))

        file_path = filedialog.askopenfilename(
            title="Selectați un fișier pentru import",
            filetypes=filetypes
        )

        if not file_path:
            return  # Utilizatorul a anulat selecția

        try:
            # Obține extensia fișierului
            _, ext = os.path.splitext(file_path)
            ext = ext.lower()

            # Procesează în funcție de tipul fișierului
            if ext == '.txt':
                with open(file_path, 'r', encoding='utf-8') as file:
                    text = file.read()
                    text_widget.delete("1.0", tk.END)
                    text_widget.insert("1.0", text)

            elif ext == '.docx' and docx_available:
                doc = docx.Document(file_path)
                text = '\n'.join([paragraph.text for paragraph in doc.paragraphs])
                text_widget.delete("1.0", tk.END)
                text_widget.insert("1.0", text)

            elif ext == '.pdf' and pdf_available:
                reader = PdfReader(file_path)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() + "\n"
                text_widget.delete("1.0", tk.END)
                text_widget.insert("1.0", text)

            else:
                messagebox.showwarning("Format nesuportat",
                                       f"Formatul fișierului {ext} nu este suportat direct.\n\n"
                                       "Sugestie: Pentru documente Word (.docx), instalați biblioteca 'python-docx'.\n"
                                       "Pentru PDF, instalați biblioteca 'PyPDF2'.")
                return

            self.status_bar.config(text=f"Fișier importat cu succes: {os.path.basename(file_path)}")

        except Exception as e:
            messagebox.showerror("Eroare", f"A apărut o eroare la importul fișierului:\n{str(e)}")

    def init_tab1(self):
        """Inițializează conținutul pentru Exercițiul 1: Extragere nume utilizator și companie"""
        # Titlu
        header = ttk.Label(self.tab1, text="Extragere nume utilizator și companie din adresa de email",
                           style="Header.TLabel")
        header.pack(pady=10)

        # Descriere
        description = ttk.Label(self.tab1,
                                text="Introduceți un text care conține o adresă de email. Programul va extrage numele utilizatorului și numele companiei.",
                                wraplength=700)
        description.pack(pady=5)

        # Cadru pentru introducerea textului
        input_frame = ttk.LabelFrame(self.tab1, text="Text de analizat")
        input_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # self.text_input1 = scrolledtext.ScrolledText(input_frame, height=8)
        # self.text_input1.pack(fill="both", expand=True, padx=5, pady=5)

        # Adăugăm un cadru pentru butoanele de input
        input_buttons_frame = ttk.Frame(input_frame)
        input_buttons_frame.pack(fill="x", side=tk.TOP, padx=5, pady=2)

        # Buton pentru import
        import_button = ttk.Button(
            input_buttons_frame,
            text="Import din fișier",
            command=lambda: self.import_file(self.text_input1)
        )
        import_button.pack(side=tk.LEFT, padx=5, pady=2)

        self.text_input1 = scrolledtext.ScrolledText(input_frame, height=8)
        self.text_input1.pack(fill="both", expand=True, padx=5, pady=5)

        # Buton pentru analiză
        analyze_button = ttk.Button(self.tab1, text="Analizează", command=self.analyze_ex1)
        analyze_button.pack(pady=10)

        # Cadru pentru rezultate
        results_frame = ttk.LabelFrame(self.tab1, text="Rezultate")
        results_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Creăm un cadru pentru afișarea rezultatelor într-un mod mai plăcut
        result_display_frame = ttk.Frame(results_frame)
        result_display_frame.pack(fill="both", expand=True, padx=5, pady=5)

        # Etichetă pentru numele utilizatorului
        ttk.Label(result_display_frame, text="Nume utilizator:", style="SubHeader.TLabel").grid(row=0, column=0,
                                                                                                sticky="w", padx=5,
                                                                                                pady=5)
        self.username_result = ttk.Label(result_display_frame, text="-", width=30)
        self.username_result.grid(row=0, column=1, sticky="w", padx=5, pady=5)

        # Etichetă pentru numele companiei
        ttk.Label(result_display_frame, text="Nume companie:", style="SubHeader.TLabel").grid(row=1, column=0,
                                                                                              sticky="w", padx=5,
                                                                                              pady=5)
        self.company_result = ttk.Label(result_display_frame, text="-", width=30)
        self.company_result.grid(row=1, column=1, sticky="w", padx=5, pady=5)

        # Etichetă pentru domeniul complet
        ttk.Label(result_display_frame, text="Domeniu complet:", style="SubHeader.TLabel").grid(row=2, column=0,
                                                                                                sticky="w", padx=5,
                                                                                                pady=5)
        self.domain_result = ttk.Label(result_display_frame, text="-", width=30)
        self.domain_result.grid(row=2, column=1, sticky="w", padx=5, pady=5)

        # Adaugă un buton pentru ștergerea textului
        clear_button = ttk.Button(self.tab1, text="Șterge tot", command=lambda: self.clear_fields(self.text_input1,
                                                                                                  [self.username_result,
                                                                                                   self.company_result,
                                                                                                   self.domain_result]))
        clear_button.pack(pady=10)

    def init_tab2(self):
        """Inițializează conținutul pentru Exercițiul 2: Extragere toate email-urile"""
        # Titlu
        header = ttk.Label(self.tab2, text="Extragere toate adresele de email din text",
                           style="Header.TLabel")
        header.pack(pady=10)

        # Descriere
        description = ttk.Label(self.tab2,
                                text="Introduceți un text care conține una sau mai multe adrese de email. Programul va identifica și extrage toate adresele valide.",
                                wraplength=700)
        description.pack(pady=5)

        # Cadru pentru introducerea textului
        input_frame = ttk.LabelFrame(self.tab2, text="Text de analizat")
        input_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # self.text_input2 = scrolledtext.ScrolledText(input_frame, height=8)
        # self.text_input2.pack(fill="both", expand=True, padx=5, pady=5)

        # Adăugăm un cadru pentru butoanele de input
        input_buttons_frame = ttk.Frame(input_frame)
        input_buttons_frame.pack(fill="x", side=tk.TOP, padx=5, pady=2)

        # Buton pentru import
        import_button = ttk.Button(
            input_buttons_frame,
            text="Import din fișier",
            command=lambda: self.import_file(self.text_input2)
        )
        import_button.pack(side=tk.LEFT, padx=5, pady=2)

        self.text_input2 = scrolledtext.ScrolledText(input_frame, height=8)
        self.text_input2.pack(fill="both", expand=True, padx=5, pady=5)

        # Cadru pentru opțiuni
        options_frame = ttk.Frame(self.tab2)
        options_frame.pack(fill="x", padx=10, pady=5)

        # Opțiune pentru tipul de pattern
        ttk.Label(options_frame, text="Tip pattern:").pack(side=tk.LEFT, padx=5)
        self.pattern_type = tk.StringVar(value="standard")
        pattern_combo = ttk.Combobox(options_frame, textvariable=self.pattern_type,
                                     values=["standard", "strict", "relaxat"],
                                     width=10, state="readonly")
        pattern_combo.pack(side=tk.LEFT, padx=5)

        # Tooltip pentru tipurile de pattern - adăugăm funcționalitate
        tooltip_label = ttk.Label(options_frame, text="ℹ️", cursor="hand2")
        tooltip_label.pack(side=tk.LEFT)
        tooltip_label.bind("<Button-1>", lambda e: messagebox.showinfo("Informații Pattern",
                                                                       "standard: detectează majoritatea formatelor de email\n" +
                                                                       "strict: doar formate standard cu litere, cifre și câteva caractere speciale\n" +
                                                                       "relaxat: acceptă o gamă mai largă de caractere speciale"))

        # # Tooltip pentru tipurile de pattern
        # ttk.Label(options_frame, text="ℹ️", cursor="hand2").pack(side=tk.LEFT)

        # Buton pentru analiză
        analyze_button = ttk.Button(self.tab2, text="Analizează", command=self.analyze_ex2)
        analyze_button.pack(pady=10)

        # Cadru pentru rezultate
        results_frame = ttk.LabelFrame(self.tab2, text="Rezultate")
        results_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # List box pentru afișarea email-urilor
        self.email_listbox = tk.Listbox(results_frame, height=8, font=("Segoe UI", 10))
        self.email_listbox.pack(side=tk.LEFT, fill="both", expand=True, padx=5, pady=5)

        # Scrollbar pentru listbox
        scrollbar = ttk.Scrollbar(results_frame, orient="vertical", command=self.email_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill="y")
        self.email_listbox.config(yscrollcommand=scrollbar.set)

        # Cadru pentru butoane acțiuni pe email-uri
        actions_frame = ttk.Frame(self.tab2)
        actions_frame.pack(fill="x", padx=10, pady=5)

        # Buton de copiere
        copy_button = ttk.Button(actions_frame, text="Copiază", command=self.copy_selected_email)
        copy_button.pack(side=tk.LEFT, padx=5)

        # Buton de export
        export_button = ttk.Button(actions_frame, text="Export", command=self.export_emails)
        export_button.pack(side=tk.LEFT, padx=5)

        # Adaugă un buton pentru ștergerea textului
        clear_button = ttk.Button(actions_frame, text="Șterge tot",
                                  command=lambda: self.clear_fields(self.text_input2, None, self.email_listbox))
        clear_button.pack(side=tk.LEFT, padx=5)

    def init_tab3(self):
        """Inițializează conținutul pentru funcționalități avansate"""
        # Titlu
        header = ttk.Label(self.tab3, text="Funcționalități avansate de extragere și analiză",
                           style="Header.TLabel")
        header.pack(pady=10)

        # Cadru pentru introducerea textului
        input_frame = ttk.LabelFrame(self.tab3, text="Text de analizat")
        input_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # self.text_input3 = scrolledtext.ScrolledText(input_frame, height=6)
        # self.text_input3.pack(fill="both", expand=True, padx=5, pady=5)

        # Adăugăm un cadru pentru butoanele de input
        input_buttons_frame = ttk.Frame(input_frame)
        input_buttons_frame.pack(fill="x", side=tk.TOP, padx=5, pady=2)

        # Buton pentru import
        import_button = ttk.Button(
            input_buttons_frame,
            text="Import din fișier",
            command=lambda: self.import_file(self.text_input3)
        )
        import_button.pack(side=tk.LEFT, padx=5, pady=2)

        self.text_input3 = scrolledtext.ScrolledText(input_frame, height=6)
        self.text_input3.pack(fill="both", expand=True, padx=5, pady=5)

        # Cadru pentru opțiuni avansate
        options_frame = ttk.LabelFrame(self.tab3, text="Opțiuni de extragere")
        options_frame.pack(fill="x", padx=10, pady=5)

        # Creăm un notebook pentru diferite tipuri de extrageri
        extract_notebook = ttk.Notebook(options_frame)
        extract_notebook.pack(fill="both", expand=True, padx=5, pady=5)

        # Tab pentru extragere email
        email_tab = ttk.Frame(extract_notebook)
        extract_notebook.add(email_tab, text="Email-uri")

        # Opțiuni pentru email
        self.show_domain = tk.BooleanVar(value=True)
        ttk.Checkbutton(email_tab, text="Arată domeniul", variable=self.show_domain).grid(row=0, column=0, padx=5,
                                                                                          pady=5, sticky="w")

        self.show_top_domains = tk.BooleanVar(value=False)
        ttk.Checkbutton(email_tab, text="Arată statistici domenii", variable=self.show_top_domains).grid(row=0,
                                                                                                         column=1,
                                                                                                         padx=5, pady=5,
                                                                                                         sticky="w")

        # Tab pentru extragere telefon
        phone_tab = ttk.Frame(extract_notebook)
        extract_notebook.add(phone_tab, text="Telefoane")

        # Opțiuni pentru telefon
        self.phone_format = tk.StringVar(value="toate")
        ttk.Radiobutton(phone_tab, text="Toate formatele", variable=self.phone_format, value="toate").grid(row=0,
                                                                                                           column=0,
                                                                                                           padx=5,
                                                                                                           pady=5,
                                                                                                           sticky="w")
        ttk.Radiobutton(phone_tab, text="Format românesc", variable=self.phone_format, value="ro").grid(row=0, column=1,
                                                                                                        padx=5, pady=5,
                                                                                                        sticky="w")
        ttk.Radiobutton(phone_tab, text="Format internațional", variable=self.phone_format, value="int").grid(row=1,
                                                                                                              column=0,
                                                                                                              padx=5,
                                                                                                              pady=5,
                                                                                                              sticky="w")

        # Tab pentru extragere URL
        url_tab = ttk.Frame(extract_notebook)
        extract_notebook.add(url_tab, text="URL-uri")

        # Opțiuni pentru URL
        self.url_protocol = tk.BooleanVar(value=True)
        ttk.Checkbutton(url_tab, text="Include protocol (http/https)", variable=self.url_protocol).grid(row=0, column=0,
                                                                                                        padx=5, pady=5,
                                                                                                        sticky="w")

        # Buton pentru analiză
        analyze_button = ttk.Button(self.tab3, text="Analizează", command=self.analyze_advanced)
        analyze_button.pack(pady=10)

        # Cadru pentru rezultate
        results_frame = ttk.LabelFrame(self.tab3, text="Rezultate")
        results_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Notebook pentru diferite tipuri de rezultate
        results_notebook = ttk.Notebook(results_frame)
        results_notebook.pack(fill="both", expand=True, padx=5, pady=5)

        # Tab pentru rezultate email
        email_results_tab = ttk.Frame(results_notebook)
        results_notebook.add(email_results_tab, text="Email-uri")

        self.adv_email_listbox = tk.Listbox(email_results_tab, height=6, font=("Segoe UI", 10))
        self.adv_email_listbox.pack(side=tk.LEFT, fill="both", expand=True, padx=5, pady=5)

        # Scrollbar pentru email listbox
        email_scrollbar = ttk.Scrollbar(email_results_tab, orient="vertical", command=self.adv_email_listbox.yview)
        email_scrollbar.pack(side=tk.RIGHT, fill="y")
        self.adv_email_listbox.config(yscrollcommand=email_scrollbar.set)

        # Tab pentru rezultate telefon
        phone_results_tab = ttk.Frame(results_notebook)
        results_notebook.add(phone_results_tab, text="Telefoane")

        self.phone_listbox = tk.Listbox(phone_results_tab, height=6, font=("Segoe UI", 10))
        self.phone_listbox.pack(side=tk.LEFT, fill="both", expand=True, padx=5, pady=5)

        # Scrollbar pentru phone listbox
        phone_scrollbar = ttk.Scrollbar(phone_results_tab, orient="vertical", command=self.phone_listbox.yview)
        phone_scrollbar.pack(side=tk.RIGHT, fill="y")
        self.phone_listbox.config(yscrollcommand=phone_scrollbar.set)

        # Tab pentru rezultate URL
        url_results_tab = ttk.Frame(results_notebook)
        results_notebook.add(url_results_tab, text="URL-uri")

        self.url_listbox = tk.Listbox(url_results_tab, height=6, font=("Segoe UI", 10))
        self.url_listbox.pack(side=tk.LEFT, fill="both", expand=True, padx=5, pady=5)

        # Scrollbar pentru URL listbox
        url_scrollbar = ttk.Scrollbar(url_results_tab, orient="vertical", command=self.url_listbox.yview)
        url_scrollbar.pack(side=tk.RIGHT, fill="y")
        self.url_listbox.config(yscrollcommand=url_scrollbar.set)

        # Cadru pentru acțiuni
        action_frame = ttk.Frame(self.tab3)
        action_frame.pack(fill="x", padx=10, pady=5)

        # Buton pentru export toate
        export_all_button = ttk.Button(action_frame, text="Exportă toate", command=self.export_all_advanced)
        export_all_button.pack(side=tk.LEFT, padx=5)

        # Buton pentru ștergere
        clear_button = ttk.Button(action_frame, text="Șterge tot", command=self.clear_advanced)
        clear_button.pack(side=tk.LEFT, padx=5)

    def init_tab4(self):
        """Inițializează conținutul pentru tab-ul de ajutor și informații"""
        # Titlu
        header = ttk.Label(self.tab4, text="Ajutor și informații despre expresii regulate",
                           style="Header.TLabel")
        header.pack(pady=10)

        # Notebook pentru diferite secțiuni de ajutor
        help_notebook = ttk.Notebook(self.tab4)
        help_notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # Tab pentru ghid de utilizare
        usage_tab = ttk.Frame(help_notebook)
        help_notebook.add(usage_tab, text="Ghid utilizare")

        usage_text = scrolledtext.ScrolledText(usage_tab, wrap=tk.WORD, font=("Segoe UI", 10))
        usage_text.pack(fill="both", expand=True, padx=5, pady=5)

        # In tab4, update the usage_text.insert() by adding this information
        usage_text.insert(tk.END, """
Ghid de utilizare al programului Extractor de Email-uri:

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
""")
        usage_text.config(state=tk.DISABLED)  # Face textul read-only

        # Tab pentru informații despre regex
        regex_tab = ttk.Frame(help_notebook)
        help_notebook.add(regex_tab, text="Despre Regex")

        regex_text = scrolledtext.ScrolledText(regex_tab, wrap=tk.WORD, font=("Segoe UI", 10))
        regex_text.pack(fill="both", expand=True, padx=5, pady=5)
        regex_text.insert(tk.END, """
Expresii regulate (Regex) - noțiuni de bază:

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
- \\d : cifre [0-9]
- \\w : caractere de cuvânt [a-zA-Z0-9_]
- \\s : spații albe (spațiu, tab, newline)

Pattern pentru email:
Un pattern simplu pentru email este: [\\w.-]+@[\\w.-]+\\.[\\w]+
Acesta identifică:
- Nume utilizator: litere, cifre, puncte și cratime
- @ : simbolul standard
- Domeniu: litere, cifre, puncte și cratime
- .extension: punctul urmat de extensie (com, ro, org, etc.)

Pentru informații mai detaliate despre expresii regulate, accesați:
https://docs.python.org/3/library/re.html
        """)
        regex_text.config(state=tk.DISABLED)  # Face textul read-only

        # Tab pentru despre program
        about_tab = ttk.Frame(help_notebook)
        help_notebook.add(about_tab, text="Despre")

        # Logo sau imagine placeholder
        logo_frame = ttk.Frame(about_tab)
        logo_frame.pack(pady=20)

        logo_label = ttk.Label(logo_frame, text="EXTRACTOR EMAIL", font=("Segoe UI", 16, "bold"))
        logo_label.pack()

        # Informații despre program
        about_info = ttk.Label(about_tab, text=f"""
        Program pentru extragerea informațiilor din adrese de email

        Versiune: 1.0
        Creat pentru: Laborator HCI
        Data: {datetime.now().strftime('%d-%m-%Y')}

        Acest program demonstrează utilizarea expresiilor regulate
        pentru extragerea și analiza adreselor de email din text.

        Dependențe opționale pentru import din fișiere:
        - python-docx: pentru documente Word (.docx)
        - PyPDF2: pentru documente PDF (.pdf)
        """, justify=tk.CENTER)
        about_info.pack(pady=10)

        # Link către mai multe resurse
        link_label = ttk.Label(about_tab, text="Mai multe despre expresii regulate",
                               foreground="blue", cursor="hand2")
        link_label.pack(pady=10)
        link_label.bind("<Button-1>", lambda e: webbrowser.open_new("https://pycon2016.regex.training/regex-intro"))

    def analyze_ex1(self):
        """Analizează textul pentru Exercițiul 1"""
        text = self.text_input1.get("1.0", tk.END)

        if not text.strip():
            messagebox.showinfo("Informație", "Vă rugăm să introduceți un text pentru analiză.")
            return

        # Pattern regex îmbunătățit pentru a extrage numele utilizatorului și numele companiei
        pattern = r"([a-zA-Z0-9._-]+)@([a-zA-Z0-9.-]+)\.([a-zA-Z]{2,})"

        rezultat = re.search(pattern, text)

        if rezultat:
            nume_utilizator = rezultat.group(1)
            nume_companie = rezultat.group(2)
            extensie = rezultat.group(3)

            # Actualizează rezultatele în interfață
            self.username_result.config(text=nume_utilizator)
            self.company_result.config(text=nume_companie)
            self.domain_result.config(text=f"{nume_companie}.{extensie}")

            # Actualizează bara de stare
            self.status_bar.config(text=f"Analiză completă - Email găsit: {nume_utilizator}@{nume_companie}.{extensie}")
        else:
            # Resetează rezultatele
            self.username_result.config(text="-")
            self.company_result.config(text="-")
            self.domain_result.config(text="-")

            # Actualizează bara de stare
            self.status_bar.config(text="Nu a fost găsită nicio adresă de email validă.")
            messagebox.showinfo("Rezultat", "Nu a fost găsită nicio adresă de email validă în textul introdus.")

    def analyze_ex2(self):
        """Analizează textul pentru Exercițiul 2"""
        text = self.text_input2.get("1.0", tk.END)

        if not text.strip():
            messagebox.showinfo("Informație", "Vă rugăm să introduceți un text pentru analiză.")
            return

        # Alege pattern-ul în funcție de selecție
        if self.pattern_type.get() == "strict":
            pattern = r"([a-zA-Z0-9._-]+)@([a-zA-Z0-9.-]+)\.([a-zA-Z]{2,})"
        elif self.pattern_type.get() == "relaxat":
            pattern = r"([\w\.\-\+]+)@([\w\.\-]+)(\.[\w\-]{2,})"
        else:  # standard
            pattern = r"([\w\.-]+)@([\w\.-]+)(\.[\w]+)"

        # Găsește toate email-urile
        rezultate = re.findall(pattern, text)

        # Curăță lista anterioară
        self.email_listbox.delete(0, tk.END)

        if rezultate:
            # Adaugă fiecare email găsit în listbox
            for i, (utilizator, domeniu, extensie) in enumerate(rezultate, 1):
                adresa_completa = f"{utilizator}@{domeniu}{extensie}"
                self.email_listbox.insert(tk.END, adresa_completa)

            # Actualizează bara de stare
            self.status_bar.config(text=f"Analiză completă - {len(rezultate)} adrese de email găsite.")
        else:
            self.status_bar.config(text="Nu a fost găsită nicio adresă de email.")
            messagebox.showinfo("Rezultat", "Nu a fost găsită nicio adresă de email în textul introdus.")

    def analyze_advanced(self):
        """Analizează textul pentru funcționalitățile avansate"""
        text = self.text_input3.get("1.0", tk.END)

        if not text.strip():
            messagebox.showinfo("Informație", "Vă rugăm să introduceți un text pentru analiză.")
            return

        # Curăță listele anterioare
        self.adv_email_listbox.delete(0, tk.END)
        self.phone_listbox.delete(0, tk.END)
        self.url_listbox.delete(0, tk.END)

        # Extrage email-uri
        email_pattern = r"([\w\.-]+)@([\w\.-]+)(\.[\w]+)"
        email_rezultate = re.findall(email_pattern, text)

        # Extrage numere de telefon în funcție de format selectat
        if self.phone_format.get() == "ro":
            phone_pattern = r"(07\d{2}[. -]?\d{3}[. -]?\d{3})|(\+407\d{2}[. -]?\d{3}[. -]?\d{3})|((02|03)\d{1}[. -]?\d{3}[. -]?\d{3})"
        elif self.phone_format.get() == "int":
            phone_pattern = r"(\+\d{1,3}[. -]?)?\d{2,4}[. -]?\d{3,4}[. -]?\d{3,4}"
        else:  # toate
            phone_pattern = r"(\+\d{1,3}[. -]?)?\d{2,4}[. -]?\d{3,4}[. -]?\d{3,4}"

        phone_rezultate = re.findall(phone_pattern, text)

        # Extrage URL-uri - pattern îmbunătățit
        if self.url_protocol.get():
            url_pattern = r"(https?:\/\/)([\w.-]+)\.([a-zA-Z]{2,})(:[0-9]+)?(\/[\w\.-]*)*"
        else:
            url_pattern = r"()([\w.-]+)\.([a-zA-Z]{2,})(:[0-9]+)?(\/[\w\.-]*)*"

        url_rezultate = re.findall(url_pattern, text)

        # Adaugă email-uri în listbox
        for utilizator, domeniu, extensie in email_rezultate:
            adresa_completa = f"{utilizator}@{domeniu}{extensie}"
            self.adv_email_listbox.insert(tk.END, adresa_completa)

        # Adaugă numere de telefon în listbox
        for phone_tuple in phone_rezultate:
            # Pentru a trata diferite forme ale rezultatelor
            if isinstance(phone_tuple, tuple):
                # Ia prima variantă care nu este goală
                phone = next((p for p in phone_tuple if p), "")
                if phone:
                    self.phone_listbox.insert(tk.END, phone)
            else:
                # Pentru cazul când rezultatul e un string direct
                self.phone_listbox.insert(tk.END, phone_tuple)

        # Adaugă URL-uri în listbox - cod corectat
        for url_match in url_rezultate:
            # Reconstruiește URL-ul
            url = ""
            protocol, domain, tld, port, path = url_match[0], url_match[1], url_match[2], url_match[3], url_match[4]

            if protocol:  # Protocol
                url += protocol
            url += domain + "." + tld  # Domeniu complet

            if port:  # Port
                url += port
            if path:  # Path
                url += path

            if url:  # Adaugă doar dacă URL-ul nu este gol
                self.url_listbox.insert(tk.END, url)

        # Actualizează bara de stare - corectat indentarea
        total_rezultate = len(email_rezultate) + len(phone_rezultate) + len(url_rezultate)
        self.status_bar.config(
            text=f"Analiză completă - {total_rezultate} elemente găsite (Email: {len(email_rezultate)}, Telefon: {len(phone_rezultate)}, URL: {len(url_rezultate)})")

        if total_rezultate == 0:
            messagebox.showinfo("Rezultat", "Nu a fost găsit niciun element în textul introdus.")

    def copy_selected_email(self):
        """Copiază email-ul selectat în clipboard"""
        selection = self.email_listbox.curselection()
        if selection:
            email = self.email_listbox.get(selection[0])
            self.root.clipboard_clear()
            self.root.clipboard_append(email)
            self.status_bar.config(text=f"Email copiat în clipboard: {email}")
        else:
            messagebox.showinfo("Informație", "Vă rugăm să selectați un email din listă.")

    def export_emails(self):
        """Exportă toate email-urile găsite într-un fișier text"""
        emails = self.email_listbox.get(0, tk.END)
        if not emails:
            messagebox.showinfo("Informație", "Nu există email-uri de exportat.")
            return

        # Creează un fișier de salvare
        filename = f"email_list_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write("\n".join(emails))
            self.status_bar.config(text=f"Email-uri exportate cu succes în {filename}")
            messagebox.showinfo("Succes", f"Lista de email-uri a fost exportată în {filename}")
        except Exception as e:
            messagebox.showerror("Eroare", f"A apărut o eroare la export: {str(e)}")

    def export_all_advanced(self):
        """Exportă toate rezultatele din funcționalitățile avansate"""
        emails = self.adv_email_listbox.get(0, tk.END)
        phones = self.phone_listbox.get(0, tk.END)
        urls = self.url_listbox.get(0, tk.END)

        if not emails and not phones and not urls:
            messagebox.showinfo("Informație", "Nu există date de exportat.")
            return

        # Creează un fișier de salvare
        filename = f"extracted_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        try:
            with open(filename, "w", encoding="utf-8") as f:
                if emails:
                    f.write("=== EMAIL-URI ===\n")
                    f.write("\n".join(emails))
                    f.write("\n\n")

                if phones:
                    f.write("=== NUMERE TELEFON ===\n")
                    f.write("\n".join(phones))
                    f.write("\n\n")

                if urls:
                    f.write("=== URL-URI ===\n")
                    f.write("\n".join(urls))
                    f.write("\n")

            self.status_bar.config(text=f"Date exportate cu succes în {filename}")
            messagebox.showinfo("Succes", f"Toate datele au fost exportate în {filename}")
        except Exception as e:
            messagebox.showerror("Eroare", f"A apărut o eroare la export: {str(e)}")

    def clear_fields(self, text_widget, labels=None, listbox=None):
        """Șterge conținutul din widget-urile specificate"""
        text_widget.delete("1.0", tk.END)

        if labels:
            for label in labels:
                label.config(text="-")

        if listbox:
            listbox.delete(0, tk.END)

        self.status_bar.config(text="Câmpuri șterse.")

    def clear_advanced(self):
        """Șterge toate câmpurile din funcționalitățile avansate"""
        self.text_input3.delete("1.0", tk.END)
        self.adv_email_listbox.delete(0, tk.END)
        self.phone_listbox.delete(0, tk.END)
        self.url_listbox.delete(0, tk.END)
        self.status_bar.config(text="Toate câmpurile au fost șterse.")


def main():
    root = tk.Tk()
    app = EmailExtractorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
