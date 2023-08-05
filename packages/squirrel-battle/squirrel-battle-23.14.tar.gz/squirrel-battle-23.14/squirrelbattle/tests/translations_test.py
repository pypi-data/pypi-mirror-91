import unittest

from squirrelbattle.translations import gettext as _, Translator


class TestTranslations(unittest.TestCase):
    def setUp(self) -> None:
        Translator.compilemessages()
        Translator.refresh_translations()
        Translator.setlocale("fr")

    def test_main_menu_translation(self) -> None:
        """
        Ensures that the main menu is translated.
        """
        self.assertEqual(_("New game"), "Nouvelle partie")
        self.assertEqual(_("Resume"), "Continuer")
        self.assertEqual(_("Load"), "Charger")
        self.assertEqual(_("Save"), "Sauvegarder")
        self.assertEqual(_("Settings"), "Paramètres")
        self.assertEqual(_("Exit"), "Quitter")

    def test_settings_menu_translation(self) -> None:
        """
        Ensures that the settings menu is translated.
        """
        self.assertEqual(_("Main key to move up"),
                         "Touche principale pour aller vers le haut")
        self.assertEqual(_("Secondary key to move up"),
                         "Touche secondaire pour aller vers le haut")
        self.assertEqual(_("Main key to move down"),
                         "Touche principale pour aller vers le bas")
        self.assertEqual(_("Secondary key to move down"),
                         "Touche secondaire pour aller vers le bas")
        self.assertEqual(_("Main key to move left"),
                         "Touche principale pour aller vers la gauche")
        self.assertEqual(_("Secondary key to move left"),
                         "Touche secondaire pour aller vers la gauche")
        self.assertEqual(_("Main key to move right"),
                         "Touche principale pour aller vers la droite")
        self.assertEqual(_("Secondary key to move right"),
                         "Touche secondaire pour aller vers la droite")
        self.assertEqual(_("Key to validate a menu"),
                         "Touche pour valider un menu")
        self.assertEqual(_("Key used to open the inventory"),
                         "Touche utilisée pour ouvrir l'inventaire")
        self.assertEqual(_("Key used to use an item in the inventory"),
                         "Touche pour utiliser un objet de l'inventaire")
        self.assertEqual(_("Key used to equip an item in the inventory"),
                         "Touche pour équiper un objet de l'inventaire")
        self.assertEqual(_("Key used to drop an item in the inventory"),
                         "Touche pour jeter un objet de l'inventaire")
        self.assertEqual(_("Key used to talk to a friendly entity"),
                         "Touche pour parler à une entité pacifique")
        self.assertEqual(_("Key used to wait"), "Touche pour attendre")
        self.assertEqual(_("Key used to use ladders"),
                         "Touche pour utiliser les échelles")
        self.assertEqual(_("Key used to use a bow"),
                         "Touche pour utiliser un arc")
        self.assertEqual(_("Key used to dance"),
                         "Touche pour danser")
        self.assertEqual(_("Texture pack"), "Pack de textures")
        self.assertEqual(_("Language"), "Langue")

    def test_entities_translation(self) -> None:
        self.assertEqual(_("player"), "joueur")

        self.assertEqual(_("hedgehog"), "hérisson")
        self.assertEqual(_("merchant"), "marchand")
        self.assertEqual(_("rabbit"), "lapin")
        self.assertEqual(_("sunflower"), "tournesol")
        self.assertEqual(_("teddy bear"), "nounours")
        self.assertEqual(_("tiger"), "tigre")
        self.assertEqual(_("eagle"), "pygargue")

        self.assertEqual(_("body snatch potion"), "potion d'arrachage de corps")
        self.assertEqual(_("bomb"), "bombe")
        self.assertEqual(_("explosion"), "explosion")
        self.assertEqual(_("heart"), "cœur")
        self.assertEqual(_("sword"), "épée")
        self.assertEqual(_("helmet"), "casque")
        self.assertEqual(_("chestplate"), "plastron")
        self.assertEqual(_("shield"), "bouclier")
        self.assertEqual(_("ruler"), "règle")
        self.assertEqual(_("scroll of damage"), "parchemin de dégâts")
        self.assertEqual(_("scroll of weakness"), "parchemin de faiblesse")
        self.assertEqual(_("bow"), "arc")
        self.assertEqual(_("fire ball staff"), "baton de boule de feu")
        self.assertEqual(_("ring of critical damage"),
                         "anneau de coup critique")
        self.assertEqual(_("ring of more experience"),
                         "anneau de plus d'expérience")
        self.assertEqual(_("monocle"), "monocle")
