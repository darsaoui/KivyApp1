from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import OneLineListItem
import pandas as pd
import os

KV = '''
ScreenManager:
    MenuScreen:

<MenuScreen>:
    name: "menu"

    MDBoxLayout:
        orientation: "vertical"
        padding: 20
        spacing: 10

        MDTextField:
            id: nom_utilisateur
            hint_text: "Nom utilisateur"

        MDTextField:
            id: nom_pc
            hint_text: "Nom du PC"

        MDTextField:
            id: ip
            hint_text: "Adresse IP"

        MDTextField:
            id: num_bureau
            hint_text: "Numéro de Bureau"

        MDTextField:
            id: date_intervention
            hint_text: "Date d'intervention"

        MDRaisedButton:
            text: "Ajouter Intervention"
            on_release: app.ajouter_intervention()

        MDRaisedButton:
            text: "Télécharger CSV"
            on_release: app.download_data_file()

        ScrollView:
            MDList:
                id: list_interventions
'''

class MenuScreen(Screen):
    pass

class InterventionApp(MDApp):
    interventions = []

    def build(self):
        self.theme_cls.primary_palette = "Blue"
        return Builder.load_string(KV)

    def ajouter_intervention(self):
        nom_utilisateur = self.root.get_screen("menu").ids.nom_utilisateur.text
        nom_pc = self.root.get_screen("menu").ids.nom_pc.text
        ip = self.root.get_screen("menu").ids.ip.text
        num_bureau = self.root.get_screen("menu").ids.num_bureau.text
        date_intervention = self.root.get_screen("menu").ids.date_intervention.text

        if not all([nom_utilisateur, nom_pc, ip, num_bureau, date_intervention]):
            self.show_dialog("Erreur", "Veuillez remplir tous les champs")
            return

        intervention = {
            "Nom utilisateur": nom_utilisateur,
            "Nom du PC": nom_pc,
            "IP": ip,
            "Numéro de Bureau": num_bureau,
            "Date d'intervention": date_intervention
        }

        self.interventions.append(intervention)
        self.root.get_screen("menu").ids.list_interventions.add_widget(
            OneLineListItem(text=f"{nom_utilisateur} - {ip} - {date_intervention}")
        )

        self.show_dialog("Ajout réussi", "Intervention ajoutée avec succès")

    def download_data_file(self):
        if not self.interventions:
            self.show_dialog("Erreur", "Aucune intervention à enregistrer")
            return

        df = pd.DataFrame(self.interventions)
        df.to_csv("interventions.csv", index=False)

        self.show_dialog("Téléchargement réussi", "Fichier CSV enregistré")

    def show_dialog(self, title, text):
        dialog = MDDialog(title=title, text=text)
        dialog.open()

if __name__ == "__main__":
    InterventionApp().run()
