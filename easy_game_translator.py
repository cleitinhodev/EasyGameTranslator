
'''
Easy Game Translator - A screen capture and real-time translation tool for games
Copyright (C) 2024 CleitinhoDEV

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.

---

Easy Game Translator - Ferramenta de captura de tela e tradução em tempo real para jogos
Copyright (C) 2024 CleitinhoDEV

Este programa é um software livre: você pode redistribuí-lo e/ou modificá-lo
sob os termos da Licença Pública Geral GNU, conforme publicada pela
Free Software Foundation, na versão 3 da Licença, ou (a seu critério) qualquer versão posterior.

Este programa é distribuído na esperança de que seja útil,
mas SEM QUALQUER GARANTIA; sem mesmo a garantia implícita de
COMERCIABILIDADE ou ADEQUAÇÃO A UM DETERMINADO PROPÓSITO. Consulte a
Licença Pública Geral GNU para mais detalhes.

Você deve ter recebido uma cópia da Licença Pública Geral GNU
junto com este programa. Caso contrário, veja <https://www.gnu.org/licenses/>.
'''

# Importação de Bibliotecas

from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QTimer
import sys
import customtkinter as ctk
import pygame
import tkinter as tk
import time
from PIL import ImageGrab
import pytesseract
from deep_translator import GoogleTranslator
from langdetect import detect
import threading
import webbrowser
from tkinter import filedialog, messagebox
import os

# r'C:\Program Files\Tesseract-OCR\tesseract.exe'

arquivo_txt = "caminho.txt"
endereco = open("caminho.txt", "r").read() if "caminho.txt" in os.listdir() else None
pytesseract.pytesseract.tesseract_cmd = endereco
# Variáveis importantes

variavel_de_atualizacao = 1
translation_active = False
primeiro_ponto = [0, 0]
segundo_ponto = [0, 0]
rect = None
idioma_principal = 'pt'
idioma_principal_manual = 'pt'
simbolo_principal = 'abc'
texto_box_mode = ''
box_ligado = None
edit_ligado = None
help_ligado = None
x_offset = None
y_offset = None
texto_finalizado = ''


def abrir_janela_ctk():

    # Cria a janela====================================================================================================
    janela = ctk.CTk()
    janela.title('Easy Game Translator')  # Ou Easy Game Translator
    janela.iconbitmap('Design/icone.ico')

    # Calcula a posição da janela para centralizá-la
    largura_janela = 700
    altura_janela = 430

    # Obtém as dimensões da tela
    largura_tela = janela.winfo_screenwidth()
    altura_tela = janela.winfo_screenheight()

    # Calcula a posição no centro
    pos_x = (largura_tela - largura_janela) // 2
    pos_y = (altura_tela - altura_janela) // 2

    # Define a geometria incluindo a posição calculada
    janela.geometry(f'{largura_janela}x{altura_janela}+{pos_x}+{pos_y}')
    janela.resizable(False, False)  # (largura, altura)
    janela.configure(fg_color="#1c1f44")  # Cor de fundo para a janela

    # Elementos ======================================================================================================
    # Funções

    # Abre Caixa Box Mode
    def box_mode():
        global box_ligado, texto_box_mode, texto_finalizado

        if box_ligado is not None:

            # Se a janela já estiver aberta, não abra outra
            box_ligado.destroy()
            box_ligado = None

        else:

            def on_closing():
                global box_ligado
                box_ligado.destroy()
                box_ligado = None

            def update_text_size(event):
                """Atualiza o tamanho do texto conforme o redimensionamento da janela."""
                largura = box_ligado.winfo_width()
                altura = box_ligado.winfo_height()

                # Define o novo tamanho da fonte proporcional ao tamanho da janela
                dimensionamento = int((largura + altura) / 50) + 4
                label.configure(font=("Comic Sans MS", dimensionamento),
                                width=int(largura - 15), height=(altura - 30))

            def atualiza_label():
                global texto_finalizado
                label.configure(text=texto_finalizado)
                box_ligado.after(1000, atualiza_label)

            # Inicializar o CustomTkinter_____________________________________________________________________________
            box_ligado = ctk.CTk()

            # Remover bordas, título, ícone e botões
            # Calcula a posição da janela para centralizá-la
            largura_janela_box = 600
            altura_janela_box = 250

            # Obtém as dimensões da tela
            largura_tela_box = box_ligado.winfo_screenwidth()
            altura_tela_box = box_ligado.winfo_screenheight()

            # Calcula a posição no centro
            pos_x_box = (largura_tela_box - largura_janela_box) // 2
            pos_y_box = (altura_tela_box - altura_janela_box) // 2

            # Define a geometria incluindo a posição calculada
            box_ligado.geometry(f'{largura_janela_box}x{altura_janela_box}+{pos_x_box}+{pos_y_box}')
            box_ligado.resizable(True, True)  # (largura, altura)

            box_ligado.overrideredirect(False)
            box_ligado.title('Box Mode')
            box_ligado.configure(fg_color="#1c1f44")  # Cor de fundo para a janela
            box_ligado.iconbitmap('Design/icone.ico')

            box_ligado.attributes("-topmost", True)  # Garantir que janela fique no topo ao abrir

            # Objetos da janela Box Mode

            label = ctk.CTkLabel(box_ligado, text="",
                                 font=("Comic Sans MS", 15),
                                 text_color='#D3D3D3',
                                 fg_color='#1C1C1C',
                                 corner_radius=10,
                                 anchor='center',
                                 bg_color='#1c1f44'
                                 )
            label.pack(expand=True)  # Para que o label ocupe o espaço disponível na janela

            # Associar o evento de redimensionamento da janela para ajustar o tamanho do texto
            box_ligado.bind("<Configure>", update_text_size)

            # Configurar o protocolo para o evento de fechamento
            box_ligado.protocol("WM_DELETE_WINDOW", lambda: (on_closing()))

            # Atualiza o texto da Label
            box_ligado.after(1000, atualiza_label)

            # Exibir a janela
            box_ligado.mainloop()

    # Abre Caixa Edit mode
    def edit_mode():
        global edit_ligado, texto_box_mode

        if edit_ligado is not None:
            # Se a janela já estiver aberta, não abra outra
            edit_ligado.destroy()
            edit_ligado = None
        else:
            if edit_ligado is not None:
                # Se a janela já estiver aberta, não abra outra
                edit_ligado.destroy()
                edit_ligado = None
            else:
                # Selecionar idioma manual
                def selecionar_lingua_manual(lingua):
                    global idioma_principal_manual

                    idiomas = [
                        # 'United States',
                        'English', 'en',
                        # 'China',
                        '中文', 'zh',
                        # 'India',
                        'हिन्दी', 'hi',
                        # 'Spain',
                        'Español', 'es',
                        # 'France',
                        'Français', 'fr',
                        # 'Saudi Arabia',
                        'العربية', 'ar',
                        # 'Brazil',
                        'Português', 'pt',
                        # 'Bangladesh',
                        'বাংলা', 'bn',
                        # 'Russia',
                        'Русский', 'ru',
                        # 'Japan',
                        '日本語', 'ja',
                        # 'Germany',
                        'Deutsch', 'de',
                        # 'Indonesia',
                        'Bahasa Indonesia', 'id',
                        # 'Pakistan',
                        'اردو', 'ur',
                        # 'Turkey',
                        'Türkçe', 'tr',
                        # 'South Korea',
                        '한국어', 'ko'
                    ]

                    for pos, idioma in enumerate(idiomas):
                        if lingua == idioma:
                            idioma_principal_manual = idiomas[pos + 1]

                def traduzir_manual():
                    global idioma_principal_manual

                    try:
                        # Pega texto da Tex Box
                        original_text_manual = text_manual.get("1.0", "end-1c")

                        # Detecta o Idioma com o Deep
                        idioma_de_origem = detect(original_text_manual)

                        # Usar o Deep Translator para traduzir o texto
                        translated_text = GoogleTranslator(source=idioma_de_origem,
                                                           target=f'{idioma_principal_manual}').\
                            translate(original_text_manual)

                        # Exibir o texto traduzido em outra label
                        traducao.configure(text=translated_text)

                    except Exception as e:
                        # Não sei porque isso funciona mas FUNCIONA!!! Então deixa assim!!!
                        traduzido_label.configure(text='texto não encontrado'
                                                       '\n(text not found)')

                # Função para adicionar o placeholder
                def add_placeholder(event=None):
                    if text_manual.get("1.0", "end-1c") == "":
                        text_manual.insert("1.0", "Digite aqui (Type here)")
                        text_manual.tag_add("placeholder", "1.0", "end")
                        text_manual.configure("placeholder", text_color="gray")

                # Função para remover o placeholder quando o usuário clicar ou digitar
                def remove_placeholder(event=None):
                    if text_manual.get("1.0", "end-1c") == "Digite aqui (Type here)":
                        text_manual.delete("1.0", "end")
                    text_manual.tag_remove("placeholder", "1.0", "end")
                    text_manual.configure("placeholder", text_color='white')

                def on_closing():
                    global edit_ligado
                    edit_ligado.destroy()
                    edit_ligado = None

                # Inicializar o CustomTkinter________________________________________________________________________
                edit_ligado = ctk.CTk()

                # Calcula a posição da janela para centralizá-la
                largura_janela_edit = 530
                altura_janela_edit = 310

                # Obtém as dimensões da tela
                largura_tela_edit = edit_ligado.winfo_screenwidth()
                altura_tela_edit = edit_ligado.winfo_screenheight()

                # Calcula a posição no centro
                pos_x_edit = (largura_tela_edit - largura_janela_edit) // 2
                pos_y_edit = (altura_tela_edit - altura_janela_edit) // 2

                # Define a geometria incluindo a posição calculada
                edit_ligado.geometry(f'{largura_janela_edit}x{altura_janela_edit}+{pos_x_edit}+{pos_y_edit}')
                edit_ligado.resizable(True, True)  # (largura, altura)

                edit_ligado.overrideredirect(False)
                edit_ligado.title('Manual Mode')
                edit_ligado.attributes("-topmost", True)
                edit_ligado.configure(fg_color="#1c1f44")  # Cor de fundo para a janela
                edit_ligado.resizable(False, True)
                edit_ligado.iconbitmap('Design/icone.ico')

                # Objetos da Janela Manual Mode

                text_manual = ctk.CTkTextbox(edit_ligado,
                                             width=240,
                                             height=210,
                                             wrap="word",
                                             bg_color="#1c1f44",
                                             border_width=2)
                text_manual.place(x=15, y=45)

                traducao = ctk.CTkLabel(edit_ligado,
                                        text='',
                                        font=('Comic Sans Ms', 20),
                                        width=240,
                                        height=210,
                                        corner_radius=10,
                                        fg_color='#1C1C1C',
                                        bg_color='#1c1f44',
                                        wraplength=200
                                        )
                traducao.place(x=270, y=45)

                traduzir_manual = ctk.CTkButton(edit_ligado, text='Translate',
                                                height=28, width=120,
                                                fg_color='#483D8B',
                                                font=('Arial', 14),
                                                hover_color='#6959CD',
                                                bg_color='#1c1f44',
                                                anchor='center',
                                                command=traduzir_manual
                                                )
                traduzir_manual.place(x=75, y=270)

                lista_de_idiomas_manual = ['Português', 'English', 'Español', 'Français', 'Deutsch',
                                           'বাংলা', '日本語', '中文', '한국어', 'हिन्दी', 'Русский', 'Bahasa Indonesia',
                                           'Türkçe', 'العربية', 'اردو']

                # Rolagem Idiomas
                menu_idiomas_rolagem_manual = ctk.CTkOptionMenu(edit_ligado,
                                                                values=lista_de_idiomas_manual,
                                                                command=lambda lin: selecionar_lingua_manual(lin),
                                                                bg_color='#1c1f44',
                                                                fg_color='#483D8B',
                                                                dropdown_fg_color='#6959CD',
                                                                button_color='#483D8B',
                                                                button_hover_color='#6959CD',
                                                                width=140)
                menu_idiomas_rolagem_manual.place(x=65, y=10)

                add_placeholder()

                # Vincular os eventos para adicionar/remover o placeholder
                text_manual.bind("<FocusIn>", remove_placeholder)  # Quando a caixa ganha foco, remove o placeholder
                text_manual.bind("<FocusOut>",
                                 add_placeholder)  # Quando a caixa perde foco, adiciona o placeholder se estiver vazio

                # Configurar o protocolo para o evento de fechamento
                edit_ligado.protocol("WM_DELETE_WINDOW", lambda: (on_closing()))

                # Exibir a janela
                edit_ligado.mainloop()

    # Abre Caixa de Ajuda(Help)
    def help_mode():
        global help_ligado

        if help_ligado is not None:
            # Se a janela já estiver aberta, não abra outra
            help_ligado.destroy()
            help_ligado = None
        else:

            def on_closing():
                global help_ligado
                help_ligado.destroy()
                help_ligado = None

            # Inicializar o CustomTkinter
            help_ligado = ctk.CTk()

            # Remover bordas, título, ícone e botões
            # Calcula a posição da janela para centralizá-la
            largura_janela_help = 300
            altura_janela_help = 350

            # Obtém as dimensões da tela
            largura_tela_help = help_ligado.winfo_screenwidth()
            altura_tela_help = help_ligado.winfo_screenheight()

            # Calcula a posição no centro
            pos_x_help = (largura_tela_help - largura_janela_help) // 2
            pos_y_help = (altura_tela_help - altura_janela_help) // 2

            # Define a geometria incluindo a posição calculada
            help_ligado.geometry(f'{largura_janela_help}x{altura_janela_help}+{pos_x_help}+{pos_y_help}')
            help_ligado.resizable(True, True)  # (largura, altura)

            help_ligado.overrideredirect(False)
            help_ligado.title('Help')
            help_ligado.attributes("-topmost", True)
            help_ligado.resizable(False, False)
            help_ligado.configure(fg_color="#1c1f44")  # Cor de fundo para a janela
            help_ligado.iconbitmap('Design/icone.ico')

            # Funções______________________________________________________________________________________________

            def open_link1():
                webbrowser.open("bugzinho.com/easygametranslator")

            def open_link2():
                webbrowser.open("github.com/cleitinhodev/EasyGameTranslator")

            def open_link3():
                webbrowser.open("patreon.com/CleitinhoDEV")

            # Objetos da Janela Help

            borda_help = ctk.CTkFrame(
                help_ligado,
                corner_radius=10,
                border_width=2,
                border_color="black",
                width=280,
                height=330)
            borda_help.place(x=10, y=10)

            titulo_help = ctk.CTkLabel(help_ligado, text='Easy '
                                       '\nGame Translator',
                                       font=("Comic Sans MS", 20, "bold"),
                                       text_color='#D3D3D3',
                                       corner_radius=10,
                                       width=20, height=20,
                                       anchor='center',
                                       wraplength=325,
                                       bg_color='#2a2a2b')
            titulo_help.place(x=60, y=30)

            developer_help = ctk.CTkLabel(help_ligado, text='Developed by CleitinhoDev.',
                                          font=("Comic Sans MS", 15),
                                          text_color='#D3D3D3',
                                          fg_color='#483D8B',
                                          corner_radius=10,
                                          width=20, height=20,
                                          anchor='center',
                                          wraplength=325,
                                          bg_color='#2a2a2b')
            developer_help.place(x=45, y=100)

            site_help = ctk.CTkLabel(help_ligado, text='Tutorial or Donate:',
                                     font=("Comic Sans MS", 15, "bold"),
                                     text_color='#D3D3D3',
                                     fg_color='#483D8B',
                                     corner_radius=10,
                                     width=20, height=20,
                                     anchor='center',
                                     wraplength=325,
                                     bg_color='#2a2a2b')
            site_help.place(x=25, y=150)

            link1_label = ctk.CTkLabel(help_ligado, text='bugzinho.com/easygametranslator',
                                       font=("Arial", 14),
                                       text_color='#00FFFF',
                                       corner_radius=10,
                                       width=20, height=20,
                                       anchor='center',
                                       wraplength=325,
                                       bg_color='#2a2a2b',
                                       cursor="hand2")
            link1_label.place(x=15, y=175)

            link1_label.bind("<Button-1>", lambda e: open_link1())

            tutorials_help = ctk.CTkLabel(help_ligado, text='GitHub:',
                                          font=("Comic Sans MS", 15, "bold"),
                                          text_color='#D3D3D3',
                                          fg_color='#483D8B',
                                          corner_radius=10,
                                          width=20, height=20,
                                          anchor='center',
                                          wraplength=325,
                                          bg_color='#2a2a2b')
            tutorials_help.place(x=25, y=200)

            link2_label = ctk.CTkLabel(help_ligado, text='github.com/cleitinhodev',
                                       font=("Arial", 15),
                                       text_color='#00FFFF',
                                       corner_radius=10,
                                       width=20, height=20,
                                       anchor='center',
                                       wraplength=325,
                                       bg_color='#2a2a2b',
                                       cursor="hand2")
            link2_label.place(x=15, y=225)

            link2_label.bind("<Button-1>", lambda e: open_link2())

            contribuir_help = ctk.CTkLabel(help_ligado, text='Patreon:',
                                           font=("Comic Sans MS", 15, "bold"),
                                           text_color='#D3D3D3',
                                           fg_color='#483D8B',
                                           corner_radius=10,
                                           width=20, height=20,
                                           anchor='center',
                                           wraplength=325,
                                           bg_color='#2a2a2b')
            contribuir_help.place(x=25, y=250)

            link3_label = ctk.CTkLabel(help_ligado, text='patreon.com/CleitinhoDEV',
                                       font=("Arial", 15),
                                       text_color='#00FFFF',
                                       corner_radius=10,
                                       width=20, height=20,
                                       anchor='center',
                                       wraplength=325,
                                       bg_color='#2a2a2b',
                                       cursor="hand2")
            link3_label.place(x=15, y=275)

            link3_label.bind("<Button-1>", lambda e: open_link3())

            agradece_help = ctk.CTkLabel(help_ligado, text='Thanks for the support! :)',
                                         font=("Comic Sans MS", 15,),
                                         text_color='#D3D3D3',
                                         corner_radius=10,
                                         width=20, height=20,
                                         anchor='center',
                                         wraplength=325,
                                         bg_color='#2a2a2b')
            agradece_help.place(x=55, y=300)

            # Configurar o protocolo para o evento de fechamento
            help_ligado.protocol("WM_DELETE_WINDOW", lambda: (on_closing()))

            # Exibir a janela
            help_ligado.mainloop()

    # Fecha Janelas Extras Abertas
    def close_custom_windows():
        global box_ligado, edit_ligado, help_ligado
        if box_ligado is not None:
            try:
                box_ligado.destroy()
            except tk.TclError:
                pass
            box_ligado = None
        if edit_ligado is not None:
            try:
                edit_ligado.destroy()
            except tk.TclError:
                pass
            edit_ligado = None
        if help_ligado is not None:
            try:
                help_ligado.destroy()
            except tk.TclError:
                pass
            help_ligado = None

    # Seleciona Símbolo de Alfabeto para Reconhecimento
    def selecionar_alpha(simbolo):
        global simbolo_principal
        # alpha = ['abc', '你', 'अ', 'ب', 'অ', 'абв', 'あ', '가']

        simbolos = [
            # English/Portuguese/Spanish/French/German
            # 'Latino',
            'abc',
            # Chinese
            # 'Hanzi',
            '你',
            # Hindi
            # 'Devanágari',
            'अ',
            # Arabic           
            # 'Alfabeto Árabe',
            'ب',
            # Bengali
            # 'Alfabeto Bengali',
            'অ',
            # Russian
            # 'Cirílico',
            'абв',
            # Japanese
            # 'Hiragana/Katakana',
            'あ',
            # Korean
            # 'Hangul',
            '가'
            ]

        for pos, simb in enumerate(simbolos):
            if simbolo == simb:
                simbolo_principal = simbolos[pos]
                print(simbolo_principal)

    # Seleciona Idioma a ser Traduzido
    def selecionar_lingua(lingua):
        global idioma_principal

        idiomas = [
            # 'United States',
            'English', 'en',
            # 'China',
            '中文', 'zh',
            # 'India',
            'हिन्दी', 'hi',
            # 'Spain',
            'Español', 'es',
            # 'France',
            'Français', 'fr',
            # 'Saudi Arabia',
            'العربية', 'ar',
            # 'Brazil',
            'Português', 'pt',
            # 'Bangladesh',
            'বাংলা', 'bn',
            # 'Russia',
            'Русский', 'ru',
            # 'Japan',
            '日本語', 'ja',
            # 'Germany',
            'Deutsch', 'de',
            # 'Indonesia',
            'Bahasa Indonesia', 'id',
            # 'Pakistan',
            'اردو', 'ur',
            # 'Turkey',
            'Türkçe', 'tr',
            # 'South Korea',
            '한국어', 'ko'
        ]

        for pos, idioma in enumerate(idiomas):
            if lingua == idioma:
                idioma_principal = idiomas[pos + 1]

    # Função que limita quantidade de carcteres nas caixas X,Y,X,Y
    def limitar_caracteres_input(*args):
        texto = caixa_01.get()
        if len(texto) > limite_maximo:
            caixa_01.delete(limite_maximo, tk.END)
        texto = caixa_02.get()
        if len(texto) > limite_maximo:
            caixa_02.delete(limite_maximo, tk.END)
        texto = caixa_03.get()
        if len(texto) > limite_maximo:
            caixa_03.delete(limite_maximo, tk.END)
        texto = caixa_04.get()
        if len(texto) > limite_maximo:
            caixa_04.delete(limite_maximo, tk.END)

        x1 = caixa_01.get()
        y1 = caixa_02.get()
        x2 = caixa_03.get()
        y2 = caixa_04.get()

        # Deleta caracteres das caixas deixando somente números
        filtro_x1 = ''
        for item in x1:
            if item.isnumeric():
                filtro_x1 = filtro_x1 + item
        caixa_01.delete(0, tk.END)  # Remove o texto existente
        caixa_01.insert(0, filtro_x1)  # Insere o novo texto

        filtro_y1 = ''
        for item in y1:
            if item.isnumeric():
                filtro_y1 = filtro_y1 + item
        caixa_02.delete(0, tk.END)  # Remove o texto existente
        caixa_02.insert(0, filtro_y1)  # Insere o novo texto

        filtro_x2 = ''
        for item in x2:
            if item.isnumeric():
                filtro_x2 = filtro_x2 + item
        caixa_03.delete(0, tk.END)  # Remove o texto existente
        caixa_03.insert(0, filtro_x2)  # Insere o novo texto

        filtro_y2 = ''
        for item in y2:
            if item.isnumeric():
                filtro_y2 = filtro_y2 + item
        caixa_04.delete(0, tk.END)  # Remove o texto existente
        caixa_04.insert(0, filtro_y2)  # Insere o novo texto

    # Função de atualização das traduções
    def update_seg(velodidade):
        global variavel_de_atualizacao
        valor = str(velodidade).replace(' s', '')
        valor = int(valor)
        variavel_de_atualizacao = valor

    # Altera Tamanho do Texto
    def alterar_tamanho_fonte(novo_tamanho):
        traduzir_label.configure(font=("Comic Sans MS", int(novo_tamanho)))
        traduzido_label.configure(font=("Comic Sans MS", int(novo_tamanho)))

    # Função para pegar valores originais da tela
    def buscar_arquivos():
        global endereco

        # Oculta a janela principal do Tkinter
        root = tk.Tk()
        root.withdraw()

        # Abre a janela de seleção de arquivo
        caminho_arquivo = filedialog.askopenfilename(
            title="Selecione o arquivo tesseract.exe",
            filetypes=[("Executável", "*.exe")],  # Filtros para mostrar apenas arquivos .exe
        )

        # Verifica se o arquivo foi encontrado e é o tesseract.exe
        if not caminho_arquivo or not os.path.basename(caminho_arquivo).lower() == "tesseract.exe":
            # Exibe mensagem de aviso
            messagebox.showwarning("Aviso", "O arquivo tesseract.exe não foi encontrado.")
            return None  # Retorna None caso não seja o arquivo correto

        # Salva o caminho do arquivo selecionado no arquivo texto
        with open("caminho.txt", "w") as arquivo:
            arquivo.write(caminho_arquivo)  # Salva o caminho sem o prefixo r e sem as aspas

        endereco = open("caminho.txt", "r").read() if "caminho.txt" in os.listdir() else None
        pytesseract.pytesseract.tesseract_cmd = endereco

        '''largura = str(janela.winfo_screenwidth())
        altura = str(janela.winfo_screenheight())

        caixa_01.delete(0, tk.END)  # Remove o texto existente
        caixa_01.insert(0, '0')  # Insere o novo texto
        caixa_02.delete(0, tk.END)  # Remove o texto existente
        caixa_02.insert(0, '0')  # Insere o novo texto
        caixa_03.delete(0, tk.END)  # Remove o texto existente
        caixa_03.insert(0, largura)  # Insere o novo texto
        caixa_04.delete(0, tk.END)  # Remove o texto existente
        caixa_04.insert(0, altura)  # Insere o novo texto'''

    # Função para capturar e traduzir
    def capture_and_translate():
        global idioma_principal, simbolo_principal, texto_box_mode, texto_finalizado
        try:
            x1 = int(caixa_01.get())
            x2 = int(caixa_03.get())
            y1 = int(caixa_02.get())
            y2 = int(caixa_04.get())

            if x1 > x2:
                x1, x2 = x2, x1
            if y1 > y2:
                y1, y2 = y2, y1

            # Capturar a área da tela com base nas coordenadas
            screenshot = ImageGrab.grab(bbox=(x1, y1, x2, y2))

            # Usar o Tesseract para reconhecer o texto na imagem
            # Pulo do gato na detecção (Não remover isso!!!):
            '''simbolos = [
                # English/Portuguese/Spanish/French/German
                # 'Latino',
                'abc',
                # Chinese
                # 'Hanzi',
                '你',
                # Hindi
                # 'Devanágari',
                'अ',
                # Arabic           
                # 'Alfabeto Árabe',
                'ب',
                # Bengali
                # 'Alfabeto Bengali',
                'অ',
                # Russian
                # 'Cirílico',
                'абв',
                # Japanese
                # 'Hiragana/Katakana',
                'あ',
                # Korean
                # 'Hangul',
                '가'
            ]'''
            original_text = None

            if simbolo_principal == 'abc':
                original_text = pytesseract.image_to_string(screenshot)  # Pode trocar o 'eng' pela linguagem desejada
            elif simbolo_principal == '你':
                original_text = pytesseract.image_to_string(screenshot, lang='chi_sim')
            elif simbolo_principal == 'अ':
                original_text = pytesseract.image_to_string(screenshot, lang='hin')
            elif simbolo_principal == 'ب':
                original_text = pytesseract.image_to_string(screenshot, lang='ara')
            elif simbolo_principal == 'অ':
                original_text = pytesseract.image_to_string(screenshot, lang='ben')
            elif simbolo_principal == 'абв':
                original_text = pytesseract.image_to_string(screenshot, lang='rus')
            elif simbolo_principal == 'あ':
                original_text = pytesseract.image_to_string(screenshot, lang='jpn')
            elif simbolo_principal == '가':
                original_text = pytesseract.image_to_string(screenshot, lang='kor')

            frase = str(original_text)
            idioma_de_origem = detect(frase)

            # Exibir o texto original em uma label
            traduzir_label.configure(text=frase)

            # Usar o Deep Translator para traduzir o texto
            translated_text = GoogleTranslator(source=idioma_de_origem,
                                               target=f'{idioma_principal}').translate(original_text)

            # Exibir o texto traduzido em outra label
            traduzido_label.configure(text=translated_text)
            texto_box_mode = str(translated_text)
            texto_finalizado = translated_text

        except Exception as e:
            # messagebox.showerror("Erro", f"Ocorreu um erro: {e}")
            traduzido_label.configure(text='texto não encontrado'
                                           '\n(text not found)')

    # Função para iniciar ou parar a captura e tradução
    def start_capture():
        try:
            x1 = int(caixa_01.get())
            x2 = int(caixa_03.get())
            y1 = int(caixa_02.get())
            y2 = int(caixa_04.get())

            if (0 <= y1 <= int(janela.winfo_screenheight()) and 0 <= y2 <= int(janela.winfo_screenheight())
                    and 0 <= x1 <= int(janela.winfo_screenwidth()) and 0 <= x2 <= int(janela.winfo_screenwidth())):
                # Mudar o botão para indicar que a tradução começou
                start_botao_opcao.configure(text="n", font=('Wingdings', 50))  # Alterar para o símbolo de pausa
                capture_menu_label.configure(text='Stop')

                def capture_loop():
                    global translation_active, variavel_de_atualizacao
                    translation_active = True
                    while translation_active:
                        capture_and_translate()
                        time.sleep(variavel_de_atualizacao)  # Intervalo de 5 segundos entre as capturas

                # Executar a captura em uma nova thread para não bloquear a interface
                threading.Thread(target=capture_loop).start()

            else:
                messagebox.showerror("Erro", f"Os valores devem estar "
                                             f"entre 0 e {int(janela.winfo_screenheight())} "
                                             f"para Y, e 0 e {int(janela.winfo_screenwidth())} para X.")
        except ValueError:
            messagebox.showerror("Erro", "Preencha todas as caixas com valores numéricos.")

    # Função para parar a tradução
    def stop_capture():
        global translation_active
        translation_active = False
        start_botao_opcao.configure(text="u", font=('Wingdings 3', 50))  # Voltar para o símbolo de play
        capture_menu_label.configure(text='Start')

    # Função que alterna entre iniciar e parar a captura
    def toggle_capture():
        if start_botao_opcao.cget("text") == "u":
            start_capture()
        else:
            stop_capture()

    # Captura de região
    def captura_regional():
        global primeiro_ponto, segundo_ponto
        rect = None

        # Configurações da janela
        root = tk.Tk()
        root.attributes('-fullscreen', True)  # Tela cheia
        root.configure(bg='black')

        # Definir a transparência da janela (0.0 é completamente transparente, 1.0 é completamente opaco)
        root.attributes('-alpha', 0.2)  # Ajuste o valor para o nível de transparência desejado

        canvas = tk.Canvas(root, bg='gray', cursor='cross', highlightthickness=0)
        canvas.pack(fill='both', expand=True)

        start_x = start_y = 0

        # Função para capturar a área da tela
        def capturar_area(x1, y1, x2, y2):
            # Certifique-se de que as coordenadas são inteiros e que x1 < x2 e y1 < y2
            x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])
            if x1 > x2:
                x1, x2 = x2, x1
            if y1 > y2:
                y1, y2 = y2, y1

            # Salva valores nas listas:
            primeiro_ponto[0] = x1
            primeiro_ponto[1] = y1
            segundo_ponto[0] = x2
            segundo_ponto[1] = y2

            caixa_01.delete(0, tk.END)  # Remove o texto existente
            caixa_01.insert(0, f'{str(primeiro_ponto[0])}')  # Insere o novo texto
            caixa_02.delete(0, tk.END)  # Remove o texto existente
            caixa_02.insert(0, f'{str(primeiro_ponto[1])}')  # Insere o novo texto
            caixa_03.delete(0, tk.END)  # Remove o texto existente
            caixa_03.insert(0, f'{str(segundo_ponto[0])}')  # Insere o novo texto
            caixa_04.delete(0, tk.END)  # Remove o texto existente
            caixa_04.insert(0, f'{str(segundo_ponto[1])}')  # Insere o novo texto

        # Funções de evento para o canvas
        def on_button_press(event):
            nonlocal start_x, start_y, rect
            start_x = canvas.canvasx(event.x)
            start_y = canvas.canvasy(event.y)
            if rect:
                canvas.delete(rect)
            rect = canvas.create_rectangle(start_x, start_y, start_x, start_y, outline='#6959CD', fill='#483D8B',
                                           stipple='gray75')

        def on_mouse_drag(event):
            cur_x = canvas.canvasx(event.x)
            cur_y = canvas.canvasy(event.y)
            canvas.coords(rect, start_x, start_y, cur_x, cur_y)

        def on_button_release(event):
            end_x = canvas.canvasx(event.x)
            end_y = canvas.canvasy(event.y)
            if abs(end_x - start_x) > 0 and abs(end_y - start_y) > 0:
                root.destroy()
                capturar_area(start_x, start_y, end_x, end_y)
            else:
                messagebox.showwarning("Seleção inválida",
                                       "A área selecionada é muito pequena. Tente novamente.")

        # Configura os eventos do canvas
        canvas.bind("<ButtonPress-1>", on_button_press)
        canvas.bind("<B1-Motion>", on_mouse_drag)
        canvas.bind("<ButtonRelease-1>", on_button_release)

        # Inicia a interface
        root.mainloop()

    # FRAMES__________________________________________________________________________________________________________

    borda_botoes = ctk.CTkFrame(
        janela,
        corner_radius=10,
        border_width=2,
        border_color="black",
        width=690,
        height=120)
    borda_botoes.place(x=5, y=5)

    borda_textos = ctk.CTkFrame(
        janela,
        corner_radius=10,
        border_width=2,
        border_color="black",
        width=690,
        height=285)
    borda_textos.place(x=5, y=140)

    # Labels__________________________________________________________________________________________________________
    # Label que exibe texto capturado
    traduzir_label = ctk.CTkLabel(janela, text='',
                                  font=("Comic Sans MS", 15),
                                  text_color='#D3D3D3',
                                  fg_color='#1C1C1C',
                                  corner_radius=10,
                                  width=325, height=265,
                                  anchor='center',
                                  wraplength=325,
                                  bg_color='#2a2a2b')
    traduzir_label.place(x=15, y=150)

    # Label que exibe texto Traduzido
    traduzido_label = ctk.CTkLabel(janela,
                                   text='',
                                   font=("Comic Sans MS", 15),
                                   text_color='#D3D3D3',
                                   fg_color='#1C1C1C',
                                   corner_radius=10,
                                   width=330, height=265,
                                   anchor='center',
                                   wraplength=325,
                                   bg_color='#2a2a2b')
    traduzido_label.place(x=350, y=150)

    # Label "Capture"
    capture_menu_label = ctk.CTkLabel(janela, text='Capture',
                                      font=("Arial", 12),
                                      fg_color='#2a2a2b',
                                      bg_color='#2a2a2b')
    capture_menu_label.place(x=32, y=95)

    # Label "x:" (1)
    capture_x1_label = ctk.CTkLabel(janela, text='x:',
                                    font=("Arial", 16, "bold"),
                                    fg_color='#2a2a2b',
                                    bg_color='#2a2a2b')
    capture_x1_label.place(x=112, y=17)

    # Label "y:" (1)
    capture_y1_label = ctk.CTkLabel(janela, text='y:',
                                    font=("Arial", 16, "bold"),
                                    fg_color='#2a2a2b',
                                    bg_color='#2a2a2b')
    capture_y1_label.place(x=192, y=17)

    # Label "x:" (2)
    capture_x2_label = ctk.CTkLabel(janela, text='x:',
                                    font=("Arial", 16, "bold"),
                                    fg_color='#2a2a2b',
                                    bg_color='#2a2a2b')
    capture_x2_label.place(x=112, y=52)

    # Label "y:" (2)
    capture_y2_label = ctk.CTkLabel(janela, text='y:',
                                    font=("Arial", 16, "bold"),
                                    fg_color='#2a2a2b',
                                    bg_color='#2a2a2b')
    capture_y2_label.place(x=192, y=52)

    # Tamanho_Fonte
    start_label = ctk.CTkLabel(janela, text='size:',
                               font=("Arial", 16),
                               fg_color='#2a2a2b',
                               bg_color='#2a2a2b')
    start_label.place(x=280, y=16)

    # Label "Start"
    capture_menu_label = ctk.CTkLabel(janela, text='Start',
                                      font=("Arial", 12),
                                      fg_color='#2a2a2b',
                                      bg_color='#2a2a2b')
    capture_menu_label.place(x=407, y=95)

    # Label "Update"
    update_label = ctk.CTkLabel(janela, text='Update:',
                                font=("Arial", 16),
                                fg_color='#2a2a2b',
                                bg_color='#2a2a2b')
    update_label.place(x=470, y=86)

    # Label "Cod:"
    cod_label = ctk.CTkLabel(janela, text='Alphabet:',
                             font=("Arial", 16),
                             fg_color='#2a2a2b',
                             bg_color='#2a2a2b')
    cod_label.place(x=470, y=15)

    # Box Mode label
    box_mode_menu_label = ctk.CTkLabel(janela, text='Box Mode',
                                       font=("Arial", 12),
                                       fg_color='#2a2a2b',
                                       bg_color='#2a2a2b')
    box_mode_menu_label.place(x=625, y=95)

    # Text label
    text_menu_label = ctk.CTkLabel(janela, text='Text',
                                   font=("Arial", 12),
                                   fg_color='#2a2a2b',
                                   bg_color='#2a2a2b')
    text_menu_label.place(x=310, y=95)

    # Caixas__________________________________________________________________________________________________________

    limite_maximo = 4

    # X1
    caixa_01 = ctk.CTkEntry(janela, width=50,
                            bg_color='#2a2a2b',
                            placeholder_text="X1")
    caixa_01.place(x=130, y=15)
    caixa_01.bind("<KeyRelease>", limitar_caracteres_input)

    # Y1
    caixa_02 = ctk.CTkEntry(janela, width=50,
                            bg_color='#2a2a2b',
                            placeholder_text="Y1")
    caixa_02.place(x=210, y=15)
    caixa_02.bind("<KeyRelease>", limitar_caracteres_input)

    # X2
    caixa_03 = ctk.CTkEntry(janela, width=50,
                            bg_color='#2a2a2b',
                            placeholder_text="X2")
    caixa_03.place(x=130, y=50)
    caixa_03.bind("<KeyRelease>", limitar_caracteres_input)

    # Y2
    caixa_04 = ctk.CTkEntry(janela, width=50,
                            bg_color='#2a2a2b',
                            placeholder_text="Y2")
    caixa_04.place(x=210, y=50)
    caixa_04.bind("<KeyRelease>", limitar_caracteres_input)

    # Rolagens________________________________________________________________________________________________________
    lista_tamanho_fonte = [str(i) for i in range(15, 31, 5)]

    lista_update_atualizacao = ['1 s', '2 s', '3 s', '4 s', '5 s',
                                '6 s', '7 s', '8 s', '9 s', '10 s',
                                '11 s', '12 s', '13 s', '14 s', '15 s']

    menu_tamanho = ctk.CTkOptionMenu(janela,
                                     values=lista_tamanho_fonte,
                                     command=lambda escolha: alterar_tamanho_fonte(escolha),
                                     bg_color='#2a2a2b',
                                     fg_color='#483D8B',
                                     dropdown_fg_color='#6959CD',
                                     button_color='#483D8B',
                                     button_hover_color='#6959CD',
                                     width=20)
    menu_tamanho.place(x=315, y=15)

    lista_de_idiomas = [
                        'Português',
                        'English',
                        'Español',
                        'Français',
                        'Deutsch',
                        'বাংলা',
                        '日本語',
                        '中文',
                        '한국어',
                        'हिन्दी',
                        'Русский',
                        'Bahasa Indonesia',
                        'Türkçe',
                        'العربية',
                        'اردو'
                        ]
    # Listas para referência (Não remover)
    '''idiomas = [
        'United States - English (en)',
        'China - 中文 (zh)',
        'India - हिन्दी (hi)',
        'Spain - Español (es)',
        'France - Français (fr)',
        'Saudi Arabia - العربية (ar)',
        'Brazil - Português (pt)',
        'Bangladesh - বাংলা (bn)',
        'Russia - Русский (ru)',
        'Japan - 日本語 (ja)',
        'Germany - Deutsch (de)',
        'Indonesia - Bahasa Indonesia (id)',
        'Pakistan - اردو (ur)',
        'Turkey - Türkçe (tr)',
        'South Korea - 한국어 (ko)'
    ]'''

    '''alfabetos = [
        ('English/Portuguese/Spanish/French/German', 'Latino', 'abc'),  # Alfabeto Latino
        ('Chinese', 'Hanzi', '你'),  # Exemplo de sílaba em Hanzi
        ('Hindi', 'Devanágari', 'अ'),  # Exemplo de sílaba em Devanágari
        ('Arabic', 'Alfabeto Árabe', 'ب'),  # Exemplo de sílaba em Árabe
        ('Bengali', 'Alfabeto Bengali', 'অ'),  # Exemplo de sílaba em Bengali
        ('Russian', 'Cirílico', 'абв'),  # Exemplo de sílaba em Cirílico
        ('Japanese', 'Hiragana/Katakana', 'あ'),  # Exemplo de sílaba em Hiragana
        ('Korean', 'Hangul', '가'),  # Exemplo de sílaba em Hangul
    ]'''

    alpha = ['abc', '你', 'अ', 'ب', 'অ', 'абв', 'あ', '가']

    # Alfabeto
    alfabeto_rolagem = ctk.CTkOptionMenu(janela,
                                         values=alpha,
                                         command=lambda sim: selecionar_alpha(sim),
                                         bg_color='#2a2a2b',
                                         fg_color='#483D8B',
                                         dropdown_fg_color='#6959CD',
                                         button_color='#483D8B',
                                         button_hover_color='#6959CD',
                                         width=70)
    alfabeto_rolagem.place(x=540, y=15)

    # Rolagem Idiomas
    menu_idiomas_rolagem = ctk.CTkOptionMenu(janela,
                                             values=lista_de_idiomas,
                                             command=lambda lin: selecionar_lingua(lin),
                                             bg_color='#2a2a2b',
                                             fg_color='#483D8B',
                                             dropdown_fg_color='#6959CD',
                                             button_color='#483D8B',
                                             button_hover_color='#6959CD',
                                             width=140)
    menu_idiomas_rolagem.place(x=470, y=50)

    # Rolagem Update
    menu_update_rolagem = ctk.CTkOptionMenu(janela,
                                            values=lista_update_atualizacao,
                                            command=lambda seg: update_seg(seg),
                                            bg_color='#2a2a2b',
                                            fg_color='#483D8B',
                                            dropdown_fg_color='#6959CD',
                                            button_color='#483D8B',
                                            button_hover_color='#6959CD',
                                            width=80)
    menu_update_rolagem.place(x=530, y=86)

    # Botões__________________________________________________________________________________________________________

    # Captura
    captura_botao_opcao = ctk.CTkButton(janela, text='x',
                                        height=80, width=80,
                                        fg_color='#483D8B',
                                        font=('Wingdings', 50),
                                        hover_color='#6959CD',
                                        bg_color='#2a2a2b',
                                        command=captura_regional)
    captura_botao_opcao.place(x=15, y=15)

    # Tela Inteira
    ajustar_botao_opcao = ctk.CTkButton(janela, text='search',
                                        height=28, width=80,
                                        fg_color='#483D8B',
                                        font=('Arial', 14),
                                        hover_color='#6959CD',
                                        bg_color='#2a2a2b',
                                        command=buscar_arquivos)
    ajustar_botao_opcao.place(x=153, y=88)

    # Start
    start_botao_opcao = ctk.CTkButton(janela, text='u',
                                      height=80, width=80,
                                      fg_color='#483D8B',
                                      font=('Wingdings 3', 50),
                                      hover_color='#6959CD',
                                      bg_color='#2a2a2b',
                                      command=toggle_capture)
    start_botao_opcao.place(x=380, y=15)

    # Botão Help
    help_botao_opcao = ctk.CTkButton(janela, text='Help!',
                                     height=28, width=28,
                                     fg_color='#483D8B',
                                     font=('Arial', 14),
                                     hover_color='#6959CD',
                                     bg_color='#2a2a2b',
                                     corner_radius=360,
                                     command=help_mode)
    help_botao_opcao.place(x=620, y=15)

    # Botao Modo Caixa
    box_botao_opcao = ctk.CTkButton(janela, text='4',
                                    height=40, width=65,
                                    fg_color='#483D8B',
                                    font=('Wingdings 2', 40),
                                    hover_color='#6959CD',
                                    bg_color='#2a2a2b',
                                    command=box_mode)
    box_botao_opcao.place(x=620, y=50)

    # Edit Mode

    # Botao Modo Caixa
    edit_botao_opcao = ctk.CTkButton(janela, text='Manual',
                                     height=28, width=87,
                                     fg_color='#483D8B',
                                     font=('Arial', 15),
                                     hover_color='#6959CD',
                                     bg_color='#2a2a2b',
                                     command=edit_mode)
    edit_botao_opcao.place(x=280, y=50)

    # Encerra todas as janelas abertas
    janela.protocol("WM_DELETE_WINDOW", lambda: (stop_capture(),
                                                 close_custom_windows(),
                                                 janela.destroy(),
                                                 sys.exit()))



    # Inicia o loop principal ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    janela.mainloop()

    sys.exit()


def apresentar_e_abrir_ctk():
    app = QApplication(sys.argv)

    # Configura a janela
    main_window = QMainWindow()
    main_window.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
    main_window.setAttribute(Qt.WA_TranslucentBackground)
    main_window.setGeometry(100, 100, 450, 450)

    # Carregar e exibir a imagem
    imagem = QPixmap('Design/icone.png')  # Substitua pelo caminho para sua imagem
    label = QLabel()
    label.setPixmap(imagem)
    label.setAlignment(Qt.AlignCenter)  # Alinha a imagem ao centro do QLabel

    central_widget = QWidget()
    layout = QVBoxLayout()
    layout.addWidget(label)
    layout.setAlignment(Qt.AlignCenter)  # Alinha o QLabel ao centro do layout
    central_widget.setLayout(layout)
    main_window.setCentralWidget(central_widget)

    # Função para centralizar a janela no monitor
    def centralizar_janela():
        screen = QApplication.primaryScreen().geometry()
        size = main_window.geometry()
        x = (screen.width() - size.width()) // 2
        y = (screen.height() - size.height()) // 2
        main_window.move(x, y)

    # Função para aumentar o tamanho da imagem
    def aumentar_imagem():

        def fechar_e_sair():
            main_window.close()
            app.quit()

        nonlocal image_size
        if image_size < 515:  # Ajuste o tamanho máximo conforme necessário
            image_size += 1
            label.setPixmap(imagem.scaled(image_size, image_size, Qt.KeepAspectRatio))
            # Atualiza o layout para centralizar a imagem
            central_widget.adjustSize()
            centralizar_janela()
        else:
            # Remove a imagem e fecha a janela após 1 segundo
            QTimer.singleShot(50, fechar_e_sair)

    pygame.mixer.init()
    pygame.mixer.music.load('Music/fundo.mp3')  # Substitua pelo caminho para sua música
    pygame.mixer.music.play()

    # Timer para aumentar o tamanho da imagem a cada 0.1 segundo
    image_size = 450
    timer = QTimer()
    timer.timeout.connect(aumentar_imagem)
    timer.start(100)

    # Timer para iniciar a janela CTk após 7 segundos
    QTimer.singleShot(7000, abrir_janela_ctk)

    # Exibe a janela
    main_window.show()
    centralizar_janela()
    sys.exit(app.exec_())


if __name__ == "__main__":
    apresentar_e_abrir_ctk()

sys.exit()
