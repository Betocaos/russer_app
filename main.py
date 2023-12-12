from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.properties import StringProperty, ObjectProperty
from kivymd.uix.textfield import MDTextField
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivymd.uix.button import MDRaisedButton, MDTextButton
from kivy.uix.recycleview import RecycleView
from kivymd.uix.label import MDLabel
from kivy.core.window import Window
from kivymd.uix.card import MDCard
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.graphics import Color, Rectangle
from datetime import datetime
from kivy.clock import Clock
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivy.uix.spinner import Spinner
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.camera import Camera
from kivy.core.camera import CameraBase
from kivymd.uix.selectioncontrol import MDCheckbox
from kivy.graphics.texture import Texture

from kivy.clock import Clock
from PIL import Image
from kivy.uix.image import Image
from io import BytesIO
import sqlite3
import datetime
import json
import pickle

Window.softinput_mode = "below_target"

# Defina uma variável global para armazenar o usuário atual
current_user = {"id": "dummy_user"}





Builder.load_string("""
<WhiteHintTextInput>:
    hint_text_color: 1, 1, 1, 1
    foreground_color: 1, 1, 1, 1
    background_color: 1, 1, 1, 0  # Configura a cor do fundo para transparente

<TelaProcedimentos>:
    BoxLayout:
        orientation: 'vertical'
        id: box_layout
""")


# Tela de Registro de Usuários
class TelaRegistro(Screen):
    def __init__(self, **kwargs):
        super(TelaRegistro, self).__init__(**kwargs)
        self.username_input = None
        self.password_input = None
        self.create_widgets()

    def create_widgets(self):
        layout = BoxLayout(
            orientation="vertical",
            spacing=10,
            padding=20,
            size_hint=(None, None),
            size=(400, 600),
            pos_hint={'center_x': 0.5, 'center_y': 0.7}
        )
        logo = Image(
            source='russer_logo.png',
            size_hint=(None, None),
            size=(300, 300),
            pos_hint={'center_x': 0.5, 'center_y': 0.9}
        )
        layout.add_widget(logo)

        input_fields = [
            ("", "username_input", "Usuário"),
            ("", "password_input", "Senha")
        ]

        for label_text, id_name, hint_text in input_fields:
            input_layout = BoxLayout(
                orientation="vertical",
                spacing=5,
                size_hint=(None, None),
                size=(400, 30),
                height=30,
                pos_hint={'center_x': 0.2, 'center_y': 0.5}
            )
            label = MDLabel(
                text=label_text,
                halign="center",
                theme_text_color="Secondary"
            )
            input_layout.add_widget(label)
            text_input = self.create_input("", id_name, hint_text)
            input_layout.add_widget(text_input)
            layout.add_widget(input_layout)

        cadastrar_button = MDRaisedButton(
            text="Registrar",
            on_press=self.register_user,
            size_hint=(None, None),
            size=(200, 40),
            pos_hint={'center_x': 0.5}
        )
        layout.add_widget(cadastrar_button)

        self.add_widget(layout)

    def create_input(self, label_text, id_name, hint_text):
        input_box = BoxLayout(
            orientation="horizontal",
            spacing=10,
            size_hint_y=None,
            height=30
        )
        label = MDLabel(
            text=label_text,
            halign="center",
            theme_text_color="Secondary"
        )
        input_box.add_widget(label)
        input_widget = MDTextField(
            id=id_name,
            hint_text=hint_text,
            size_hint_x=None,
            width=200,
            password=(id_name == "password_input")  # Ocultar a senha no campo de senha
        )
        setattr(self, id_name, input_widget)
        input_box.add_widget(input_widget)

        return input_box


    def register_user(self, instance):
        username = self.username_input.text
        password = self.password_input.text

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        cursor.execute('''
            INSERT INTO users (username, password)
            VALUES (?, ?)
        ''', (username, password))
        conn.commit()
        conn.close()

        self.mostrar_dialogo_sucesso()

        # Limpar os campos de input após o registro bem-sucedido
        self.username_input.text = ""
        self.password_input.text = ""

    def mostrar_dialogo_sucesso(self):
        dialog = MDDialog(
            title="Sucesso",
            text="Usuário registrado com sucesso!",
            buttons=[
                MDRaisedButton(
                    text="Fechar",
                    on_release=self.fechar_dialogo_sucesso
                )
            ],
        )
        dialog.open()

    def fechar_dialogo_sucesso(self, instance):
        self.manager.current = "tela_principal"  # Navega de volta para a tela principal


# Tela de Login
class TelaLogin(Screen):
    def __init__(self, **kwargs):
        super(TelaLogin, self).__init__(**kwargs)
        self.username_input = None
        self.password_input = None
        self.logged_in_user = None  # Adicione esta linha
        self.create_widgets()
        username_input = ObjectProperty(None)

    def create_widgets(self):
        layout = BoxLayout(
            orientation="vertical",
            spacing=10,
            padding=20,
            size_hint=(None, None),
            size=(400, 600),
            pos_hint={'center_x': 0.5, 'center_y': 0.6}
        )
        # Adiciona uma linha vazia (Widget Spacer)
        layout.add_widget(Widget(size_hint_y=None, height=50))

        image = Image(
            source='russer_logo.png',
            size_hint=(None, None),
            size=(300, 300),
            pos_hint={'center_x': 0.5, 'top': 0.6}
        )
        layout.add_widget(image)

        input_fields = [
            ("", "username_input", "Usuário"),
            ("", "password_input", "Senha")
        ]

        for label_text, id_name, hint_text in input_fields:
            input_layout = BoxLayout(
                orientation="vertical",
                spacing=5,
                size_hint=(None, None),
                size=(400, 30),
                # height=30,
                pos_hint={'center_x': 0.2, 'center_y': 0.5}
            )
            label = MDLabel(
                text=label_text,
                halign="center",
                theme_text_color="Secondary"
            )
            input_layout.add_widget(label)
            text_input = self.create_input("", id_name, hint_text)
            input_layout.add_widget(text_input)
            layout.add_widget(input_layout)

            # Adiciona uma linha vazia (Widget Spacer)
            layout.add_widget(Widget(size_hint_y=None, height=10))

        login_btn = MDRaisedButton(
            text="   Login   ",
            on_press=self.login,
            size_hint=(None, None),
            size=(300, 40),
            pos_hint={'center_x': 0.5}
        )

        register_btn = MDTextButton(
            text="[u][color=00008b]Registrar[/color][/u]",
            markup=True,
            on_press=self.navigate_to_registro,
            size_hint=(None, None),
            size=(200, 20),
            pos_hint={'center_x': 0.5, 'center_y': 0.4},
            padding=20,
        )

        layout.add_widget(login_btn)
        layout.add_widget(register_btn)

        # Adiciona uma linha vazia (Widget Spacer)
        layout.add_widget(Widget(size_hint_y=None, height=50))

        # Adicionar sua assinatura no rodapé da tela
        signature_label = Label(
            text="[color=808080][i]Created by BetoCaos[/i][/color]",
            markup=True,
            size_hint=(None, None),
            size=(400, 30),
            pos_hint={"center_x": 0.5}
        )
        layout.add_widget(signature_label)

        # Adicionar a versão no rodapé da tela
        version_label = Label(
            text="[color=808080][i]Versão 0.0.1[/i][/color]",
            markup=True,
            size_hint=(None, None),
            size=(400, 30),
            pos_hint={"center_x": 0.5}
        )
        layout.add_widget(version_label)

        self.add_widget(layout)

        # Adicione um evento de foco aos campos de entrada
        self.username_input.bind(on_focus=self.on_textfield_focus)
        self.password_input.bind(on_focus=self.on_textfield_focus)

    def on_textfield_focus(self, instance, value):
        if value:
            # Adia o foco no MDTextField para garantir que o teclado esteja pronto
            Clock.schedule_once(self.focus_on_input, 0.1)

    def focus_on_input(self, dt):
        # Foca no MDTextField para abrir o teclado
        self.username_input.focus = True
        # Abre o teclado virtual explicitamente
        Window.show_virtual_keyboard()



    def create_input(self, label_text, id_name, hint_text):
        input_box = BoxLayout(
            orientation="horizontal",
            spacing=10,
            size_hint_y=None,
            height=30
        )
        label = MDLabel(
            text=label_text,
            halign="center",
            theme_text_color="Secondary"
        )
        input_box.add_widget(label)

        input_widget = MDTextField(
            id=id_name,
            hint_text=hint_text,
            size_hint_x=None,
            width=200,
            password=(id_name == "password_input")  # Ocultar a senha no campo de senha
        )
        setattr(self, id_name, input_widget)
        input_box.add_widget(input_widget)

        return input_box



    def login(self, instance):
        username = self.username_input.text
        password = self.password_input.text
        print(f"Nome do Usuário: {username}")

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM users WHERE username=? AND password=?
        ''', (username, password))

        if cursor.fetchone():
            # Define o nome do usuário logado no momento
            global current_user
            current_user = username
            self.manager.current = "tela_principal"

        else:
            self.mostrar_dialogo_erro()

            conn.close()

    def save_user_name(self, user_name):
        try:
            conn = sqlite3.connect("procedimentos.db")
            cursor = conn.cursor()

            # Verifica se a tabela 'usuarios' existe
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT
                )
            ''')

            # Insere ou atualiza o nome do usuário
            cursor.execute('''
                INSERT OR REPLACE INTO usuarios (id, nome) VALUES (1, ?)
            ''', (user_name,))

            conn.commit()
            conn.close()

        except sqlite3.Error as e:
            print("Erro ao salvar o nome do usuário no banco de dados:", e)

        finally:
            # Garante que a conexão seja fechada, mesmo em caso de erro
            conn.close()



    def mostrar_dialogo_erro(self):
        dialog = MDDialog(
            title="Erro",
            text="Usuário ou senha incorretos.",
            buttons=[
                MDRaisedButton(
                    text="Fechar", on_release=lambda x: dialog.dismiss()
                )
            ],
        )
        dialog.open()

        # Limpar os campos de input após o registro bem-sucedido
        self.username_input.text = ""
        self.password_input.text = ""

    def navigate_to_registro(self, instance):
        self.manager.current = "tela_registro"


class WhiteHintTextInput(TextInput):
    pass





# Tela Principal
class TelaPrincipal(Screen, FocusBehavior):
    logged_in_user = StringProperty()
    procedimento_em_execucao = StringProperty()

    def __init__(self, **kwargs):
        super(TelaPrincipal, self).__init__(**kwargs)
        self.create_widgets()
        self.procedure_cards = {}
        self.load_data()
        self.load_saved_cards()
        self.initialize_status_file()
        # self.manager.current_user = None


    def initialize_status_file(self):
        try:
            with open("status.json", "r") as file:
                status_data = json.load(file)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            # Cria o arquivo "status.json" com um objeto vazio, se não existir ou estiver vazio
            with open("status.json", "w") as file:
                json.dump({}, file)

    def update_logged_in_user(self, user_name):
        self.logged_in_user = user_name

    def on_pre_enter(self, *args):
        # Este método é chamado sempre que a tela é exibida
        self.load_data()  # Carrega os dados do banco de dados


    def create_widgets(self):
        layout = BoxLayout(
            orientation="vertical",
            spacing=10,
            padding=20,
            size_hint=(None, None),
            size=(400, 700),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )


        logo = Image(
            source='russer_a.png',
            size_hint=(None, None),
            size=(300, 200),
            pos_hint={'center_x': 0.5, 'center_y': 1}
        )
        layout.add_widget(logo)

        # Adiciona um layout horizontal para o logo e os MDTextButtons
        header_layout = BoxLayout(orientation='horizontal', spacing=10)

        # Adiciona os MDTextButtons
        pesquisa_btn = MDTextButton(
            text="Pesquisar",
            theme_text_color="Custom",
            text_color=(0, 0, 1, 1),  # Cor azul
            on_press=self.ir_para_tela_pesquisa,
            size_hint=(None, None),
            size=(150, 40),
            pos_hint={'center_x': 0.3}

        )
        separador_label = Label(text="|", color=(0, 0, 1, 1))  # Caractere "|"

        procedimentos_btn = MDTextButton(
            text="Procedimentos",
            theme_text_color="Custom",
            text_color=(0, 0, 1, 1),  # Cor azul
            on_press=self.ir_para_tela_procedimentos,
            size_hint=(None, None),
            size=(150, 40),
            pos_hint={'center_x': 0.8}

        )

        # Adiciona os MDTextButtons ao layout horizontal
        header_layout.add_widget(pesquisa_btn)
        header_layout.add_widget(separador_label)
        header_layout.add_widget(procedimentos_btn)

        # Adiciona o layout horizontal ao layout vertical
        layout.add_widget(header_layout)
        self.add_widget(layout)

        # Crie um RecycleView para exibir os procedimentos
        self.rv = RecycleView(
            size_hint=(1, None),
            size=(Window.width, Window.height - 150)  # Ajuste a altura conforme necessário
        )
        self.data_layout = BoxLayout(orientation='vertical', spacing=10)
        self.rv.add_widget(self.data_layout)
        layout.add_widget(self.rv)

        # Adiciona uma linha vazia (Widget Spacer)
        layout.add_widget(Widget())

        cadastrar_procedimentos_btn = MDRaisedButton(
            text="Cadastrar Procedimentos",
            on_press=self.navigate_to_cadastro_procedimentos,
            size_hint=(None, None),
            size=(200, 40),
            pos_hint={'center_x': 0.5}
        )

        layout.add_widget(cadastrar_procedimentos_btn)

    def ir_para_tela_pesquisa(self, instance):
        self.manager.current = "tela_pesquisa"

    def ir_para_tela_procedimentos(self, instance):
        self.manager.current = "tela_procedimentos"



    def update_data(self, instance):
        # Lógica para atualizar os dados na tela principal
        self.load_data()  # Recarrega os dados do banco de dados

    def navigate_to_cadastro_procedimentos(self, instance):
        self.manager.current = "tela_cadastro_procedimentos"

    def create_popup(self, procedimento, procedimento_id):
        if procedimento in ["Uret. Rígida", "Uret. Rigida", "Rigida"]:
            hint_texts = [
                ("Fio Guia", ""), ("Pinça Extratora", ""), ("Fibra Laser", ""),
                ("Duplo J", ""), ("", ""), ("", "")
            ]
        elif procedimento in ["Uret. Flexível", "Uret. Flexivel", "Flexivel", "flexivel"]:
            hint_texts = [
                ("Fio Guia", ""), ("Bainha", ""), ("Pinça Extratora", ""),
                ("Fibra Laser", ""), ("Duplo J", ""), ("", "")
            ]
        elif procedimento in ["RTU - P", "RTU - V", "RTU"]:
            hint_texts = [
                ("Alça de Ressecção", ""), ("Evacuador Ellick", ""), ("", ""),
                ("", ""), ("", ""), ("", "")
            ]
        elif procedimento in ["Percutanea", "Percutânea"]:
            hint_texts = [
                ("Fio Guia", ""), ("Cateter Ureteral", ""), ("Agulha de Punção", ""),
                ("Kit dilatadores", ""), ("Duplo J", ""), ("", "")
            ]
        else:
            hint_texts = [
                ("Consignado", " "), ("Consignado", " "), ("Consignado", " "),
                ("Consignado", " "), ("Consignado", " ")
            ]

        content = BoxLayout(orientation='vertical', spacing=10)

        # Adicione o botão de fechar no canto superior direito
        close_button = MDTextButton(
            text="X",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),  # Branco
            pos_hint={'right': 1, 'top': 1},
            size_hint=(None, None),
            size=(30, 30)
        )
        close_button.bind(on_press=lambda instance: self.popup.dismiss())

        title_layout = BoxLayout(size_hint_y=None, height=40)
        title_label = Label(text="  ", size_hint_x=0.2)
        title_layout.add_widget(title_label)
        title_layout.add_widget(close_button)

        content.add_widget(title_layout)

        input_fields = []

        for campo, quantidade_inicial in hint_texts:
            input_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint_x=1)
            input_layout.padding_x = 50  # Ajusta o espaçamento à esquerda para centralizar os widgets

            hint_text = campo.strip()
            quantidade_input = TextInput(
                hint_text="1" if hint_text else " ",
                text=str(quantidade_inicial),
                halign="center",
                size_hint=(None, None),  # Removendo size_hint_x e size_hint_y
                height=30,  # Definindo a altura desejada
                width=50  # Definindo a largura fixa do campo de entrada de quantidade
            )

            input_field = TextInput(
                hint_text=campo,
                size_hint=(None, None),  # Removendo size_hint_x e size_hint_y
                height=30,  # Definindo a altura desejada
                width=210  # Definindo a largura fixa do campo de entrada de texto
            )
            # Adiciona um evento de foco nos campos de entrada para adiar o foco
            quantidade_input.bind(focus=self.on_textfield_focus)
            input_field.bind(focus=self.on_textfield_focus)

            input_layout.add_widget(quantidade_input)
            input_layout.add_widget(input_field)
            content.add_widget(input_layout)
            input_fields.extend([quantidade_input, input_field])

        consignados_button_visible = self.check_consignados_exist(procedimento_id)

        # Verifica se há dados salvos e ajusta o texto do botão "Seguir"
        follow_button_text = "Seguir"
        if consignados_button_visible:
            follow_button_text = "Alterar"

        follow_button = MDRaisedButton(
            # text="Seguir",
            text=follow_button_text,
            # on_release=lambda instance: self.save_consignados_data(procedimento_id, input_fields, procedimento),
            size_hint=(None, None),
            size=(250, 30),
            pos_hint={'center_x': 0.5}
        )
        follow_button.bind(
            on_release=lambda instance: self.save_consignados_data(procedimento_id, input_fields, procedimento))

        if consignados_button_visible:
            show_consignados_button = MDRaisedButton(
                text="Mostrar Consignados",
                on_release=lambda instance: self.show_consignados(procedimento_id),
                size_hint=(None, None),
                size=(250, 30),
                pos_hint={'center_x': 0.5}
            )

            content.add_widget(show_consignados_button)

        content.add_widget(follow_button)

        self.popup = Popup(title="", content=content, size_hint=(None, None), size=(300, 400))
        self.popup.title = "Consignados"
        self.popup.open()

    def on_textfield_focus(self, instance, value):
        if value:
            # Adia o foco no TextInput para garantir que o teclado esteja pronto
            Clock.schedule_once(lambda dt: self.focus_on_input(instance), 0.1)

    def focus_on_input(self, text_input):
        # Use o método `focus` do `FocusBehavior` para forçar o foco e abrir o teclado
        self.focus = True
        text_input.focus = True
        # Abre o teclado virtual explicitamente
        # Window.show_virtual_keyboard()

    # Adicione esta nova função para verificar se existem consignados salvos
    def check_consignados_exist(self, procedimento_id):
        conn = sqlite3.connect('procedimentos.db')
        cursor = conn.cursor()

        try:
            # Utilize COUNT(*) para obter o número de linhas
            cursor.execute(f'''
                SELECT COUNT(*) FROM consignados_{procedimento_id}
            ''')

            count = cursor.fetchone()[0]  # Obtenha o valor do COUNT
        except sqlite3.OperationalError:
            # Se ocorrer um erro, a tabela não existe
            count = 0

        conn.close()

        return count > 0  # Retorna True se houver pelo menos uma linha, indicando que a tabela existe

    def show_consignados(self, procedimento_id):
        # Lógica para mostrar consignados salvos
        conn = sqlite3.connect('procedimentos.db')
        cursor = conn.cursor()

        # Verifica se a tabela de consignados para o procedimento_id existe
        cursor.execute(f'SELECT * FROM consignados_{procedimento_id}')


        consignados_data = cursor.fetchall()

        conn.close()

        # Cria um popup para mostrar os consignados salvos
        consignados_content = BoxLayout(orientation='vertical', spacing=10)
        for consignado in consignados_data:
            consignado_label = Label(
                text=f" {consignado[1]} |  {consignado[2]} |  {consignado[3]}",
                size_hint_y=None,
                height=30,
                halign="left",
            )
            consignados_content.add_widget(consignado_label)

        consignados_popup = Popup(title="Consignados Salvos", content=consignados_content, size_hint=(None, None),
                                  size=(400, 300))
        consignados_popup.open()

    def save_consignados_data(self, procedimento_id, input_fields, procedimento):
        # Recupere os dados dos campos de consignados
        consignados_data = []

        for i in range(6):
            quantidade = input_fields[i * 2].text
            hint_text = input_fields[i * 2 + 1].hint_text
            dados_input = input_fields[i * 2 + 1].text

            consignados_data.append((quantidade, hint_text, dados_input))

        # Salve os dados no banco de dados vinculado ao procedimento_id
        conn = sqlite3.connect('procedimentos.db')
        cursor = conn.cursor()

        # Exemplo de criação de uma tabela para os consignados vinculada ao procedimento
        create_table_query = f'''
            CREATE TABLE IF NOT EXISTS consignados_{procedimento_id} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                quantidade TEXT,
                hint_text TEXT,
                dados_input TEXT
            )
        '''
        insert_data_query = f'''
            INSERT INTO consignados_{procedimento_id} (quantidade, hint_text, dados_input)
            VALUES (?, ?, ?)
        '''

        try:
            cursor.execute(create_table_query)

            # Insira os dados dos consignados na tabela
            for consignado in consignados_data:
                cursor.execute(insert_data_query, consignado)

            conn.commit()
        except sqlite3.Error as e:
            print("SQLite error:", e)
        finally:
            conn.close()




        # Limpe os campos de entrada
        for input_field in input_fields:
            input_field.text = ""

        # Feche o popup atual
        self.popup.dismiss()

        # Abra o segundo popup
        self.create_popup2(procedimento_id)




    def create_popup2(self, procedimento_id):
        popup2 = Popup(
            title="Equipamentos Utilizados",
            size_hint=(0.6, 0.4)
        )

        equipamentos_input = WhiteHintTextInput(
            hint_text="Equipamentos",
            size_hint=(0.5, None),
            pos_hint={'center_x': 0.5},
            height=30

        )
        obs_input = WhiteHintTextInput(
            hint_text="Obs.",
            size_hint=(0.5, None),
            pos_hint={'center_x': 0.5},
            height=30


        )

        confirm_button = MDRaisedButton(
            text="Confirmar",
            size_hint=(None, None),
            size=(400, 40),
            pos_hint={'center_x': 0.5},
            md_bg_color=(0, 0.5, 0, 1),  # Cor verde (RGBA)
            on_release=lambda x: self.confirm_procedure(procedimento_id, equipamentos_input.text, obs_input.text)
        )

        cancel_button = MDRaisedButton(
            text="Cancelar",
            size_hint=(None, None),
            size=(400, 40),
            pos_hint={'center_x': 0.5},
            height=40,
            md_bg_color=(1, 0, 0, 1),  # Cor vermelha (RGBA)
            on_release=lambda x: self.cancel_procedure(procedimento_id, equipamentos_input.text, obs_input.text)
        )

        popup2.content = BoxLayout(
            orientation="vertical",
            spacing=10,
            padding=10
        )

        popup2.content.add_widget(equipamentos_input)
        popup2.content.add_widget(obs_input)
        popup2.content.add_widget(confirm_button)
        popup2.content.add_widget(cancel_button)

        self.popup2 = popup2  # Armazene a referência ao popup para usá-la no método confirm_procedure
        popup2.open()

        content = BoxLayout(orientation='vertical', spacing=10, size_hint=(None, None), size=(400, 400))

        # Exemplo de uso do procedimento_id no segundo popup
        label = MDLabel(
            text=f"ID do Procedimento: {procedimento_id}",
            halign="center",
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
        )

        content.add_widget(label)





    def clear_input_fields(self):
        self.equipamentos_utilizados = []  # Limpa a lista de equipamentos utilizados
        self.obs = ""  # Limpa o campo de observações

    def save_procedure_status(self, procedimento_id, status, color):
        status_data = self.load_procedure_status()
        status_data[procedimento_id] = {"status": status, "color": color}
        with open("status.json", "w") as file:
            json.dump(status_data, file)

    def load_procedure_status(self):
        try:
            with open("status.json", "r") as file:
                status_data = json.load(file)
        except FileNotFoundError:
            status_data = {}
        return status_data

    def tirar_foto_e_salvar(self, procedimento_id):
        try:
            # Inicializa a câmera
            camera = Camera(resolution=(640, 480), play=True)

            # Aguarda o início da câmera
            Clock.schedule_once(lambda dt: self.tirar_foto(camera, procedimento_id), 1)

        except Exception as e:
            print("Erro ao inicializar a câmera:", e)

    def tirar_foto(self, camera, procedimento_id):
        try:
            # Aguarda o usuário tirar a foto
            while not camera.play:
                Clock.tick()

            # Certifica-se de que a câmera está pronta
            while not camera.texture:
                Clock.tick()

            # Verifica se a coluna 'imagens' existe e, se não, a cria
            self.adicionar_coluna_imagems()

            # Captura a imagem da câmera
            image_texture = camera.texture

            # Obtém os pixels da textura da câmera
            pixels = image_texture.pixels
            image_width = image_texture.width
            image_height = image_texture.height

            # Salva os pixels como uma imagem PNG
            image_data = BytesIO(pixels)
            image_data.name = f"{procedimento_id}.png"

            # Salva a imagem no campo "imagens" do banco de dados
            conn = sqlite3.connect("procedimentos.db")
            cursor = conn.cursor()

            cursor.execute('''
                UPDATE procedimentos SET imagens = ? WHERE id = ?
            ''', (image_data.getvalue(), procedimento_id))

            conn.commit()
            conn.close()

            # Adiciona feedback ao usuário, como desativar a câmera ou mostrar uma mensagem de sucesso
            camera.play = False

        except Exception as e:
            print("Erro ao tirar foto e salvar no banco de dados:", e)

    def adicionar_coluna_imagems(self):
        try:
            conn = sqlite3.connect("procedimentos.db")
            cursor = conn.cursor()

            # Adiciona a coluna 'imagens' se ela não existir
            cursor.execute('''
                PRAGMA table_info(procedimentos)
            ''')
            columns = [column[1] for column in cursor.fetchall()]
            if 'imagens' not in columns:
                cursor.execute('''
                    ALTER TABLE procedimentos ADD COLUMN imagens BLOB
                ''')

            conn.commit()

        except sqlite3.Error as e:
            print("Erro ao adicionar coluna 'imagens':", e)

        finally:
            conn.close()


    def confirm_procedure(self, procedimento_id, equipamentos_utilizados, obs):
        # Lógica para salvar os dados no banco de dados
        self.save_procedure_data(procedimento_id, equipamentos_utilizados, obs, "Confirmado")

        # Lógica para atualizar a cor do texto do procedimento na interface
        self.update_procedure_color(procedimento_id, (0, 0.5, 0, 1))  # Altere para a cor verde

        # Tirar foto e salvar no campo "imagens"
        self.tirar_foto_e_salvar(procedimento_id)

        # Limpar os campos de input
        self.clear_input_fields()

        # Fechar o pop-up
        self.popup2.dismiss()

        # Salvar a cor no arquivo "status.json"
        self.save_procedure_status(procedimento_id, "Confirmado", (0, 0.5, 0, 1))

        # Obtém o nome do usuário logado no momento
        global current_user
        user_name = current_user

        try:
            conn = sqlite3.connect("procedimentos.db")
            cursor = conn.cursor()

            # Adiciona a coluna 'usuario' se ela não existir
            cursor.execute('''
                PRAGMA table_info(procedimentos)
            ''')
            columns = [column[1] for column in cursor.fetchall()]
            if 'usuario' not in columns:
                cursor.execute('''
                    ALTER TABLE procedimentos ADD COLUMN usuario TEXT
                ''')

            # Salva o nome do usuário na tabela procedimentos
            cursor.execute('''
                 UPDATE procedimentos SET usuario = ? WHERE id = ?
            ''', (user_name, procedimento_id))

            conn.commit()

        except sqlite3.Error as e:
            print("Erro ao confirmar procedimento e salvar o nome do usuário:", e)

        finally:
            conn.close()



    def get_procedimento_em_execucao(self):
        return self.procedimento_em_execucao


    def cancel_procedure(self, procedimento_id, equipamentos_utilizados, obs):
        if not equipamentos_utilizados:
            equipamentos_utilizados = ""

        # Lógica para salvar os dados no banco de dados, incluindo equipamentos_utilizados e obs
        self.save_procedure_data(procedimento_id, equipamentos_utilizados, obs, "Cancelado")

        # Lógica para atualizar a cor do texto do procedimento na interface
        self.update_procedure_color(procedimento_id, (1, 0, 0, 1))  # Vermelho

        # Limpar os campos de input
        self.clear_input_fields()

        # Fechar o pop-up
        self.popup2.dismiss()

        # Salvar a cor e o status no arquivo "status.json"
        self.save_procedure_status(procedimento_id, "Cancelado", (1, 0, 0, 1))

        # # Carregue os cartões salvos
        # self.load_saved_cards()

    def update_procedure_color(self, procedimento_id, cor):
        card = self.procedure_cards.get(procedimento_id)
        if card:
            label = card.children[0]  # Assumindo que o MDLabel está no topo do cartão
            label.color = cor

    def save_procedure_data(self, procedimento_id, equipamentos_utilizados, obs, status):
        try:
            conn = sqlite3.connect("procedimentos.db")
            cursor = conn.cursor()

            cursor.execute(
                "UPDATE procedimentos SET equipamentos_utilizados = ?, obs = ?, status = ? WHERE id = ?",
                (equipamentos_utilizados, obs, status, procedimento_id))

            conn.commit()
            conn.close()

        except sqlite3.Error as e:
            print("Erro ao salvar os dados do procedimento no banco de dados:", e)

    def clear_input_fields(self):
        self.equipamentos_utilizados = []
        self.obs = ""

    def load_saved_cards(self):
        # Carregue os cartões salvos de um arquivo
        try:
            with open('card_state.pkl', 'rb') as file:
                self.procedure_cards = pickle.load(file)
        except FileNotFoundError:
            self.procedure_cards = []

    def get_data_from_database(self):
        # Conecta ao banco de dados
        conn = sqlite3.connect("procedimentos.db")
        cursor = conn.cursor()

        # Executa a consulta
        cursor.execute("SELECT * FROM procedimentos")

        # Obtém todos os dados
        data_from_db = cursor.fetchall()

        # Fecha a conexão
        conn.close()

        return data_from_db

    def load_data(self):
        # Lógica para carregar os dados do banco de dados
        data_from_db = self.get_data_from_database()

        # Ordena os dados pela data e hora
        data_from_db.sort(key=lambda x: (x[1], x[2]))



        # Limpa os widgets de dados anteriores
        self.data_layout.clear_widgets()

        # Limpa o dicionário de cartões ao recarregar os dados
        self.procedure_cards = {}

        try:
            # Utiliza o cursor da instância
            for row in data_from_db:
                # print(row)  # Adicione esta linha para imprimir os valores de row
                data_dict = {
                    "id": row[0],
                    "data": row[1],
                    "hora": row[2],
                    "hospital": row[3],
                    "paciente": row[4],
                    "medico": row[5],
                    "convenio": row[6],
                    "procedimento": row[7]
                }

                # Formatando a string antes de atribuí-la ao MDLabel
                formatted_data = (
                    f"Data: {data_dict['data']}  |  {data_dict['hora']}  |  Hosp.: {data_dict['hospital']} \n"
                    f"Pac.: {data_dict['paciente']}  |   Med.: {data_dict['medico']}\n"
                    f"Proc.: {data_dict['procedimento']}  |  Conv.: {data_dict['convenio']}"
                )

                card = MDCard(
                    orientation="vertical",
                    size_hint=(None, None),
                    size=(400, 80)
                )
                card.procedimento_id = data_dict['id']  # Atribui o ID do procedimento ao card
                self.procedure_cards[data_dict['id']] = card  # Adiciona o card ao dicionário
                card.add_widget(
                    MDLabel(
                        text=formatted_data,
                        size_hint=(None, None),
                        width=400,
                        height=90,
                        font_size=9,
                        halign="left",
                        theme_text_color="Secondary"
                    )
                )
                card.bind(on_release=lambda instance, procedimento=data_dict['procedimento'],
                                            procedimento_id=data_dict['id']: self.create_popup(procedimento,
                                                                                               procedimento_id))
                self.data_layout.add_widget(card)

        except sqlite3.Error as e:
            print("Erro ao consultar o banco de dados:", e)


        finally:
            # conn.close()
            pass



class TelaCadastroProcedimentos(Screen):
    def __init__(self, **kwargs):
        super(TelaCadastroProcedimentos, self).__init__(**kwargs)
        self.data_input = None
        self.hora_input = None
        self.hospital_input = None
        self.paciente_input = None
        self.medico_input = None
        self.convenio_input = None
        self.procedimento_input = None
        self.create_widgets()

    def create_widgets(self):
        layout = BoxLayout(
            orientation="vertical",
            spacing=20,
            padding=20,
            size_hint=(None, None),
            size=(400, 600),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )

        logo = Image(
            source='russer_c.png',
            size_hint=(None, None),
            size=(300, 200),
            pos_hint={'center_x': 0.5}
        )
        layout.add_widget(logo)



        input_fields = [
            ("data_input", "Data"),
            ("hora_input", "Hora"),
            ("hospital_input", "Hospital"),
            ("paciente_input", "Paciente"),
            ("medico_input", "Médico"),
            ("convenio_input", "Convênio"),
            ("procedimento_input", "Procedimento"),

        ]

        for id_name, hint_text in input_fields:
            text_input = self.create_input(id_name, hint_text)
            layout.add_widget(text_input)

        # Adiciona uma linha vazia (Widget Spacer)
        layout.add_widget(Widget())

        cadastrar_procedimento_btn = MDRaisedButton(
            text="Cadastrar Procedimento",
            on_press=self.cadastrar_procedimento,
            size_hint=(None, None),
            size=(200, 40),
            pos_hint={'center_x': 0.5}
        )

        layout.add_widget(cadastrar_procedimento_btn)

        # Adiciona uma linha vazia (Widget Spacer)
        layout.add_widget(Widget())

        # ao clicar volta pa tela principal
        voltar_tela_principal_btn = MDTextButton(
            text="Voltar",
            theme_text_color="Custom",
            text_color=(0, 0, 1, 1),  # Cor azul
            on_press=self.voltar_tela_principal,
            size_hint=(None, None),
            size=(200, 200),
            pos_hint={'x': 0, 'y': 0}
        )

        layout.add_widget(voltar_tela_principal_btn)
        self.add_widget(layout)

    def create_input(self, id_name, hint_text):
        input_box = BoxLayout(
            orientation="horizontal",
            spacing=10,
            size_hint_y=None,
            height=30,
            pos_hint={'center_x': 0.5}
        )

        input_widget = MDTextField(
            id=id_name,
            hint_text=hint_text,  # Usa hint_text no lugar do texto
        )
        setattr(self, id_name, input_widget)
        input_box.add_widget(input_widget)

        input_widget.bind(on_touch_down=self.on_input_touch_down)

        return input_box

    def on_input_touch_down(self, instance, touch):
        if instance.collide_point(*touch.pos):
            instance.focus = True

    def voltar_tela_principal(self, instance):
        self.manager.current = "tela_principal"

    def cadastrar_procedimento(self, instance):
        data = self.data_input.text
        hora = self.hora_input.text
        hospital = self.hospital_input.text
        paciente = self.paciente_input.text
        medico = self.medico_input.text
        convenio = self.convenio_input.text
        procedimento = self.procedimento_input.text

        # Salvar os dados no banco de dados
        self.save_procedimento(data, hora, hospital, paciente, medico, convenio, procedimento)

        # Limpar os campos
        self.clear_input_fields()




    def save_procedimento(self, data, hora, hospital, paciente, medico, convenio, procedimento):
        try:
            conn = sqlite3.connect("procedimentos.db")
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS procedimentos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    data DATE,
                    hora TIME,  -- Use TIME for the time field
                    hospital TEXT,
                    paciente TEXT,
                    medico TEXT,
                    convenio TEXT,
                    procedimento TEXT,
                    equipamentos_utilizados TEXT DEFAULT "Equip. Utilizado ",
                    obs TEXT DEFAULT "Obs. ",
                    status TEXT DEFAULT "Pendente"
                )
            ''')

            cursor.execute('''
                        INSERT INTO procedimentos (data, hora, hospital, paciente, medico, convenio, procedimento)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (data, hora, hospital, paciente, medico, convenio, procedimento))

            conn.commit()
            conn.close()
            self.mostrar_dialogo_sucesso()
        except sqlite3.Error as e:
            print(f"Erro ao salvar procedimento: {e}")

        finally:
            conn.close()



    def clear_input_fields(self):
        for id_name in ["data_input", "hora_input", "hospital_input", "paciente_input", "medico_input",
                        "convenio_input", "procedimento_input"]:
            getattr(self, id_name).text = ""


    def mostrar_dialogo_sucesso(self):
        dialog = MDDialog(
            title="Sucesso",
            text="Procedimento cadastrado com sucesso!",
            buttons=[
                MDRaisedButton(
                    text="Fechar", on_release=self.fechar_dialogo_sucesso

                )
            ],
        )
        dialog.open()

    def fechar_dialogo_sucesso(self, instance):
        self.manager.current = "tela_principal"  # Navega de volta para a tela principal



class TelaPesquisa(Screen):
    def __init__(self, **kwargs):
        super(TelaPesquisa, self).__init__(**kwargs)
        self.create_widgets()

    def create_widgets(self):
        layout = BoxLayout(
            orientation="vertical",
            spacing=20,
            padding=20,
            size_hint=(None, None),
            size=(400, 600),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )

        logo = Image(
            source='russer_p.png',
            size_hint=(None, None),
            size=(300, 200),
            pos_hint={'center_x': 0.5}
        )
        layout.add_widget(logo)

        pesquisa_label = Label(text="Opções de Pesquisa", font_size=20)

        # Adiciona um layout horizontal para o spinner e o input de pesquisa
        pesquisa_layout = BoxLayout(orientation='horizontal', spacing=10)

        # Adiciona um Spinner para escolher a opção de pesquisa
        opcoes_pesquisa = ["Data", "Hospital", "Paciente", "Médico", "Procedimento", "Convênio", "Status", "Usuário"]
        spinner = Spinner(
            text="Selecione uma opção",
            values=opcoes_pesquisa,
            size_hint=(None, None),
            size=(150, 30),
            background_color=(0, 0, 1, 1)  # Cor azul (R, G, B, A)
        )
        pesquisa_layout.add_widget(spinner)

        # Adiciona um MDTextField para inserir os dados de pesquisa
        pesquisa_input = MDTextField(
            hint_text="Digite os dados de pesquisa",
            size_hint=(None, None),
            size=(200, 40)
        )
        pesquisa_layout.add_widget(pesquisa_input)

        confirmar_pesquisa_btn = MDRaisedButton(
            text="Confirmar Pesquisa",
            on_press=self.realizar_pesquisa,
            size_hint=(None, None),
            size=(200, 40),
            pos_hint={'center_x': 0.5}
        )

        self.resultados_label = MDLabel(
            text="Resultados da Pesquisa:",
            theme_text_color="Secondary",
            valign='middle',
            markup=True,
        )

        scroll_view = ScrollView(size_hint=(None, None), size=(400, 300), do_scroll_y=True)
        scroll_view.add_widget(self.resultados_label)

        layout.add_widget(pesquisa_label)
        layout.add_widget(pesquisa_layout)
        layout.add_widget(confirmar_pesquisa_btn)
        layout.add_widget(scroll_view)

        self.add_widget(layout)

        self.spinner = spinner
        self.pesquisa_input = pesquisa_input

        # ao clicar volta pa tela principal
        voltar_tela_principal_btn = MDTextButton(
            text="Voltar",
            theme_text_color="Custom",
            text_color=(0, 0, 1, 1),  # Cor azul
            on_press=self.voltar_tela_principal,
            size_hint=(None, None),
            size=(200, 200),
            pos_hint={'x': 0, 'y': 0}
        )

        layout.add_widget(voltar_tela_principal_btn)
        # Adicione o evento de foco ao MDTextField
        self.pesquisa_input.bind(on_focus=self.on_textfield_focus)

    def on_textfield_focus(self, instance, value):
        if value:
            # Foca no MDTextField para abrir o teclado quando ele recebe o foco
            Window.bind(on_key_down=self.on_key_down)

    def on_key_down(self, window, key, *args):
        # Fecha o teclado quando a tecla 'Enter' é pressionada
        if key == 13:  # 13 é o código da tecla 'Enter'
            self.pesquisa_input.focus = False
            Window.unbind(on_key_down=self.on_key_down)
            return True  # Indica que a tecla foi tratada
        return False  # A tecla não foi tratada, permitindo que outros eventos de teclado ocorram

    def voltar_tela_principal(self, instance):
        self.manager.current = "tela_principal"

    def realizar_pesquisa(self, instance):
        opcao_pesquisa = self.spinner.text
        dado_pesquisa = self.pesquisa_input.text

        resultado_pesquisa = self.pesquisar_no_banco(opcao_pesquisa, dado_pesquisa)

        if resultado_pesquisa:
            linhas_formatadas = []


            # resultados_text = "\n\n".join(linhas_formatadas)
            for resultado in resultado_pesquisa:
                # Ignora o campo "Id" na formatação
                linha1 = ", ".join(str(resultado[i]) for i in range(0, 4))  # (Data, Hora, Hospital)
                linha2 = ", ".join(str(resultado[i]) for i in range(4, 6))  # (Paciente, Médico)
                linha3 = ", ".join(str(resultado[i]) for i in range(6, 11))  # (Procedimento, Convênio, Status)
                linha4 = ", ".join(str(resultado[i]) for i in range(11, 13))  # ("usuario", imagens)

                # Adiciona espaços entre as linhas
                linhas_formatadas.append(f"{linha1}\n{linha2}\n{linha3}\n{linha4}")

            resultados_text = "\n\n".join(linhas_formatadas)
            self.resultados_label.text = f"[size=16]{resultados_text}[/size]"
        else:
            self.resultados_label.text = "[size=16]Nenhum resultado encontrado.[/size]"

    def pesquisar_no_banco(self, opcao_pesquisa, dado_pesquisa):
        try:
            conn = sqlite3.connect("procedimentos.db")
            cursor = conn.cursor()


            # Use o operador LIKE de forma mais aberta e converta para minúsculas
            query = f'SELECT * FROM procedimentos WHERE LOWER("{opcao_pesquisa}") LIKE LOWER(?)'

            print("Consulta SQL:", query)  # Adicione esta linha para imprimir a consulta SQL
            print("Opção de Pesquisa:", opcao_pesquisa)
            print("Dado de Pesquisa:", dado_pesquisa)

            cursor.execute(query, (f'%{dado_pesquisa}%',))


            resultado_pesquisa = cursor.fetchall()

            conn.close()
            return resultado_pesquisa
        except sqlite3.Error as e:
            print(f"Erro na pesquisa: {e}")
            return None
        finally:
            # Garante que a conexão seja fechada, mesmo em caso de erro
            conn.close()




class TabelaProcedimentos(RecycleView):
    def __init__(self, **kwargs):
        super(TabelaProcedimentos, self).__init__(**kwargs)
        self.data = self.obter_dados_do_banco()

    def obter_dados_do_banco(self):
        # Conectar ao banco de dados
        conn = sqlite3.connect('procedimentos.db')
        cursor = conn.cursor()

        # Executar a consulta para obter dados
        cursor.execute(
            'SELECT strftime("%m/%Y", datetime(data, '
            '"unixepoch", "localtime")) AS mes_ano, COUNT(*) FROM procedimentos WHERE data IS NOT NULL GROUP BY mes_ano'
        )

        # Obter resultados
        dados = cursor.fetchall()

        # Imprimir todos os resultados
        for row in dados:
            print(row)

        # Fechar a conexão com o banco de dados
        conn.close()

        # Transformar resultados em um formato mais adequado
        dados_formatados = [{'text': f'{row[0]} = {row[1]} procedimentos'} for row in dados]

        return dados_formatados




class TelaProcedimentos(Screen):
    def __init__(self, **kwargs):
        super(TelaProcedimentos, self).__init__(**kwargs)

    def on_enter(self, *args):
        # Chamado quando a tela é exibida
        self.carregar_tabela()

    def carregar_tabela(self):
        # Conecta ao banco de dados
        conn = sqlite3.connect("procedimentos.db")
        cursor = conn.cursor()

        # Consulta SQL para obter o total de procedimentos por mês, ano e usuário
        query = """
            SELECT strftime('%m/%Y', Data) as MesAno, Usuario, COUNT(*) as TotalProcedimentos
            FROM procedimentos
            GROUP BY MesAno, Usuario
        """
        cursor.execute(query)
        resultados = cursor.fetchall()

        # Cria um layout vertical para organizar a tabela e o botão "Voltar"
        layout_principal = BoxLayout(orientation='vertical')

        # Adiciona o logo no topo
        logo_layout = FloatLayout(size=(600, 200))
        logo = Image(source='russer_logo.png', size_hint=(None, None), size=(300, 150), pos_hint={'center_x': 0.5, 'top': 1})
        logo_layout.add_widget(logo)
        layout_principal.add_widget(logo_layout)

        # Adiciona os resultados ao layout
        for resultado in resultados:
            mes_ano, usuario, total_procedimentos = resultado
            label_text = f"{mes_ano} - {usuario} = {total_procedimentos} procedimentos"
            label = Label(
                text=label_text,
                color=(0, 0, 1, 1),
                size_hint=(None, None),
                size=(600, 50),
            )
            layout_principal.add_widget(label)

        # Adiciona o botão "Voltar" ao rodapé
        voltar_tela_principal_btn = MDTextButton(
            text="Voltar",
            theme_text_color="Custom",
            text_color=(0, 0, 1, 1),  # Cor azul
            on_press=self.voltar_tela_principal,
            size_hint=(None, None),
            size=(200, 50),
        )
        layout_principal.add_widget(voltar_tela_principal_btn)

        # Fecha a conexão com o banco de dados
        conn.close()

        # Adiciona o layout principal à tela
        self.add_widget(layout_principal)

    def voltar_tela_principal(self, instance):
         self.manager.current = "tela_principal"





class RusserApp(MDApp):
    def build(self):


        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.primary_hue = "900"
        self.theme_cls.accent_hue = "900"
        self.theme_cls.theme_style = "Light"
        self.screen_manager = ScreenManager()
        self.screen_manager.add_widget(TelaLogin(name="tela_login"))
        self.screen_manager.add_widget(TelaRegistro(name="tela_registro"))
        self.screen_manager.add_widget(TelaPrincipal(name="tela_principal"))
        self.screen_manager.add_widget(TelaCadastroProcedimentos(name="tela_cadastro_procedimentos"))
        self.screen_manager.add_widget(TelaPesquisa(name="tela_pesquisa"))
        self.screen_manager.add_widget(TelaProcedimentos(name="tela_procedimentos"))

        # Defina a tela inicial
        # self.screen_manager.current = "tela_principal"
        return self.screen_manager



if __name__ == "__main__":
    RusserApp().run()

