import tkinter as tk
from tkinter import scrolledtext, ttk
from tkinter import messagebox
import ply.lex as lex

class MyLexer(object):
    reserved = {
        'static': 'STATIC',
        'public': 'PUBLIC',
        'void': 'VOID',
        'int': 'INT',
        'float': 'FLOAT',
        'if': 'IF',
        'else': 'ELSE',
        'while': 'WHILE',
        'return': 'RETURN',
        'print': 'PRINT',
    }

    tokens = [
        'IDENTIFICADOR', 'ENTERO', 'DECIMAL', 'OPERADOR_LE',
        'DELIMITADOR_LE', 'CADENA',
    ] + list(reserved.values())

    t_OPERADOR_LE = r'[\+\-\*/=]'
    t_DELIMITADOR_LE = r'[;,\(\)\{\}]'
    t_ignore = ' \t'
    t_ignore_COMMENT = r'\/\/.*'

    def t_CADENA(self, t):
        r'\".*?\"'
        t.value = t.value[1:-1]
        return t

    def t_DECIMAL(self, t):
        r'\d+\.\d+'
        t.value = float(t.value)
        return t

    def t_ENTERO(self, t):
        r'\d+'
        t.value = int(t.value)
        return t

    def t_IDENTIFICADOR(self, t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        if t.value[0].isdigit():
            messagebox.showerror("Error", f"Identificador no puede comenzar con un número en la línea {t.lexer.lineno}")
            t.lexer.skip(1)
        else:
            t.type = self.reserved.get(t.value, 'IDENTIFICADOR')
            return t

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    def t_error(self, t):
        messagebox.showerror("Error", f"Carácter ilegal '{t.value[0]}' en la línea {t.lexer.lineno}")
        t.lexer.skip(1)

    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

lexer = MyLexer()
lexer.build()

def analyze():
    lexer.lexer.input(input_text.get("1.0", tk.END))
    result_text.delete("1.0", tk.END)
    for tok in lexer.lexer:
        result_text.insert(tk.END, f"Token: {tok.type}\tLexema: {tok.value}\tLínea: {tok.lineno}\n")

def clear_texts():
    input_text.delete("1.0", tk.END)
    result_text.delete("1.0", tk.END)

window = tk.Tk()
window.title("Analizador Léxico")
window.geometry("800x600")  # Ajusta el tamaño de la ventana según tus necesidades

frame = tk.Frame(window, bg="#ecf0f1")
frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

input_label = tk.Label(frame, text="Ingresa el código:", bg="#ecf0f1", font=("Arial", 12))
input_label.pack(side=tk.TOP, anchor="w", pady=(10, 0))  # Agrega espacio superior

input_text = scrolledtext.ScrolledText(frame, width=80, height=15, bg="#d5dbdb", font=("Arial", 10))
input_text.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)

result_label = tk.Label(frame, text="Resultados del análisis:", bg="#ecf0f1", font=("Arial", 12))
result_label.pack(side=tk.TOP, anchor="w", pady=(10, 0))  # Agrega espacio superior

result_text = scrolledtext.ScrolledText(frame, width=80, height=15, bg="#d5dbdb", fg="#333", font=("Arial", 10))
result_text.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)

analyze_button = tk.Button(frame, text="Analizar", command=analyze, bg="#3498db", fg="#fff", font=("Arial", 12), relief=tk.GROOVE)
analyze_button.pack(side=tk.LEFT, padx=(10, 5))  # Ajusta el espacio izquierdo y derecho

clear_button = tk.Button(frame, text="Limpiar", command=clear_texts, bg="#e74c3c", fg="#fff", font=("Arial", 12), relief=tk.GROOVE)
clear_button.pack(side=tk.RIGHT, padx=(5, 10))  # Ajusta el espacio izquierdo y derecho

style = ttk.Style()
style.configure("Treeview", background="#d5dbdb", fieldbackground="#d5dbdb", font=("Arial", 10))
style.map("Treeview", background=[("selected", "#3498db")])

window.mainloop()
S