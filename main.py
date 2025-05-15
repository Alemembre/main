from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.button import Button
from kivy.uix.popup import Popup
import pandas as pd
from datetime import datetime
import os
import re

class RequisaApp(App):
    def build(self):
        self.df = self.cargar_datos()
        self.mesas_preparacion = {
            "carne": "Mesa caliente", "res": "Mesa caliente", "pollo": "Mesa caliente", "cerdo": "Mesa caliente",
            "pescado": "Mesa caliente", "churrasco": "Mesa caliente", "tacos": "Mesa caliente", "bistec": "Mesa caliente",
            "milanesa": "Mesa caliente", "sopa": "Mesa caliente", "huevos": "Mesa caliente", "omelette": "Mesa caliente",
            "salsa": "Mesa caliente", "huevo": "Mesa caliente", "canelones": "Mesa caliente", "lasaña": "Mesa caliente",

            "vegetales": "Guarnicion", "queso": "Guarnicion", "pasta": "Guarnicion", "tajadas": "Guarnicion",
            "totopos": "Guarnicion", "tostones": "Guarnicion", "maduro": "Guarnicion", "platano": "Guarnicion",
            "pipian": "Guarnicion", "guiso": "Guarnicion", "papas": "Guarnicion", "papa": "Guarnicion", "elote": "Guarnicion",
            "ayote": "Guarnicion", "chayote": "Guarnicion", "pancake": "Guarnicion", "wafles": "Guarnicion", "vigoron": "Guarnicion",
            "baho": "Guarnicion", "quequisque": "Guarnicion", "frijoles": "Guarnicion",

            "ensalada": "Mesa fria", "sandia": "Mesa fria", "aderezo": "Mesa fria", "sandwich": "Mesa fria",
            "fruta": "Mesa fria", "pico de gallo": "Mesa fria", "parfait": "Mesa fria", "yogurt": "Mesa fria", "granola": "Mesa fria",

            "rollo": "Panaderia", "rol": "Panaderia", "pico": "Panaderia", "pan": "Panaderia", "croissant": "Panaderia",
            "bruschetta": "Panaderia", "panuelos": "Panaderia", "prisionero": "Panaderia", "strudel": "Panaderia", "canapè": "Panaderia",
            "tostadas": "Panaderia", "rosquillas": "Panaderia",

            "pastel": "Reposteria", "red velvet": "Reposteria", "flan": "Reposteria", "torta": "Reposteria",
            "tres leches": "Reposteria", "tiramisú": "Reposteria", "cupcake": "Reposteria", "brownie": "Reposteria",
            "budín": "Reposteria", "galleta": "Reposteria", "donas": "Reposteria", "tartaleta": "Reposteria"
        }

        self.root = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.root.add_widget(Label(text='📋 Ingreso de Requisas para Eventos', font_size=24, size_hint=(1, 0.1)))

        self.fecha_input = TextInput(hint_text='Fecha (YYYY-MM-DD)', multiline=False, size_hint=(1, 0.07))
        self.root.add_widget(self.fecha_input)

        hora_box = BoxLayout(size_hint=(1, 0.07))
        self.hora_input = TextInput(hint_text='Hora (HH:MM)', multiline=False)
        self.ampm_spinner = Spinner(
            text='AM',
            values=('AM', 'PM'),
            size_hint=(0.3, 1)
        )
        hora_box.add_widget(self.hora_input)
        hora_box.add_widget(self.ampm_spinner)
        self.root.add_widget(hora_box)

        self.evento_input = TextInput(hint_text='Nombre del Evento', multiline=False, size_hint=(1, 0.07))
        self.root.add_widget(self.evento_input)

        self.producto_input = TextInput(hint_text='Producto', multiline=False, size_hint=(1, 0.07))
        self.root.add_widget(self.producto_input)

        self.unidad_spinner = Spinner(
            text='Ltrs',
            values=['Ltrs', 'Galón', 'Pax', 'Porción/?', 'Libra', 'Oz'],
            size_hint=(1, 0.07)
        )
        self.root.add_widget(self.unidad_spinner)

        self.cantidad_input = TextInput(hint_text='Cantidad', multiline=False, input_filter='int', size_hint=(1, 0.07))
        self.root.add_widget(self.cantidad_input)

        self.destino_input = TextInput(hint_text='Área de Destino', multiline=False, size_hint=(1, 0.07))
        self.root.add_widget(self.destino_input)

        self.observaciones_input = TextInput(hint_text='Observaciones', multiline=False, size_hint=(1, 0.07))
        self.root.add_widget(self.observaciones_input)

        self.guardar_btn = Button(text='Guardar', background_color=(0, 1, 0, 1), size_hint=(1, 0.1))
        self.guardar_btn.bind(on_press=self.guardar_requisa)
        self.root.add_widget(self.guardar_btn)

        self.mensaje_label = Label(text='', size_hint=(1, 0.15))
        self.root.add_widget(self.mensaje_label)

        return self.root

    def cargar_datos(self):
        if os.path.exists("requisas_eventos.xlsx"):
            try:
                return pd.read_excel("requisas_eventos.xlsx")
            except Exception as e:
                print("Error al leer Excel:", e)
                return pd.DataFrame(columns=[
                    "ID Evento", "Fecha del Evento", "Hora de Entrega", "Nombre del Evento", "Producto", "Unidad",
                    "Cantidad Requerida", "Área de Destino", "Mesa de Preparación", "Observaciones"
                ])
        else:
            return pd.DataFrame(columns=[
                "ID Evento", "Fecha del Evento", "Hora de Entrega", "Nombre del Evento", "Producto", "Unidad",
                "Cantidad Requerida", "Área de Destino", "Mesa de Preparación", "Observaciones"
            ])

    def asignar_mesa(self, producto):
        producto = producto.lower()
        for clave, valor in self.mesas_preparacion.items():
            if clave in producto:
                return valor
        return "Mesa no asignada"

    def generar_id_evento(self):
        return datetime.now().strftime('%Y%m%d%H%M%S')

    def mostrar_popup(self, mensaje):
        popup = Popup(title='Mensaje',
                      content=Label(text=mensaje),
                      size_hint=(0.6, 0.4))
        popup.open()

    def validar_hora(self, hora_text):
        # Validar formato HH:MM 12h
        pattern = r'^(0?[1-9]|1[0-2]):([0-5][0-9])$'
        return bool(re.match(pattern, hora_text))

    def convertir_a_24h(self, hora_text, ampm):
        hora, minutos = map(int, hora_text.split(":"))
        if ampm == 'PM' and hora != 12:
            hora += 12
        if ampm == 'AM' and hora == 12:
            hora = 0
        return f"{hora:02d}:{minutos:02d}"

    def guardar_requisa(self, instance):
        fecha_text = self.fecha_input.text.strip()
        if fecha_text:
            try:
                fecha = datetime.strptime(fecha_text, '%Y-%m-%d').date()
            except ValueError:
                self.mostrar_popup("❌ Formato de fecha incorrecto. Use YYYY-MM-DD.")
                return
        else:
            fecha = datetime.today().date()

        hora_text = self.hora_input.text.strip()
        if not self.validar_hora(hora_text):
            self.mostrar_popup("❌ Formato de hora inválido. Use HH:MM en formato 12 horas (ej: 01:30).")
            return

        hora_24 = self.convertir_a_24h(hora_text, self.ampm_spinner.text)

        evento = self.evento_input.text.strip()
        producto = self.producto_input.text.strip()
        unidad = self.unidad_spinner.text
        cantidad_text = self.cantidad_input.text.strip()
        destino = self.destino_input.text.strip()
        observaciones = self.observaciones_input.text.strip()

        if not evento or not producto or not cantidad_text or not destino:
            self.mostrar_popup("❌ Por favor complete todos los campos obligatorios.")
            return

        try:
            cantidad = int(cantidad_text)
        except ValueError:
            self.mostrar_popup("❌ Cantidad debe ser un número entero.")
            return

        mesa = self.asignar_mesa(producto)
        id_evento = self.generar_id_evento()

        nueva_fila = {
            "ID Evento": id_evento,
            "Fecha del Evento": fecha,
            "Hora de Entrega": hora_24,
            "Nombre del Evento": evento,
            "Producto": producto,
            "Unidad": unidad,
            "Cantidad Requerida": cantidad,
            "Área de Destino": destino,
            "Mesa de Preparación": mesa,
            "Observaciones": observaciones
        }

        self.df = pd.concat([self.df, pd.DataFrame([nueva_fila])], ignore_index=True)
        self.df.to_excel("requisas_eventos.xlsx", index=False)

        self.mensaje_label.text = "✅ Requisa guardada correctamente."
        self.limpiar_campos()

    def limpiar_campos(self):
        self.fecha_input.text = ""
        self.hora_input.text = ""
        self.ampm_spinner.text = "AM"
        self.evento_input.text = ""
        self.producto_input.text = ""
        self.unidad_spinner.text = "Ltrs"
        self.cantidad_input.text = ""
        self.destino_input.text = ""
        self.observaciones_input.text = ""

if __name__ == '__main__':
    RequisaApp().run()
