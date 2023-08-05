# Copyright (C) 2020-2021 by ÿnérant, eichhornchen, nicomarg, charlse
# SPDX-License-Identifier: GPL-3.0-or-later

import gettext as gt
import os
from pathlib import Path
import re
import subprocess
from typing import Any, List


class Translator:
    """
    This module uses gettext to translate strings.
    Translator.setlocale defines the language of the strings,
    then gettext() translates the messages.
    """
    SUPPORTED_LOCALES: List[str] = ["de", "en", "es", "fr"]
    locale: str = "en"
    translators: dict = {}

    @classmethod
    def refresh_translations(cls) -> None:
        """
        Loads compiled translations.
        """
        for language in cls.SUPPORTED_LOCALES:
            rep = Path(__file__).parent / "locale" / language / "LC_MESSAGES"
            rep.mkdir(parents=True) if not rep.is_dir() else None
            if os.path.isfile(rep / "squirrelbattle.mo"):
                cls.translators[language] = gt.translation(
                    "squirrelbattle",
                    localedir=Path(__file__).parent / "locale",
                    languages=[language],
                )

    @classmethod
    def setlocale(cls, lang: str) -> None:
        """
        Defines the language used to translate the game.
        The language must be supported, otherwise nothing is done.
        """
        lang = lang[:2]
        if lang in cls.SUPPORTED_LOCALES:
            cls.locale = lang

    @classmethod
    def get_translator(cls) -> Any:
        return cls.translators.get(cls.locale, gt.NullTranslations())

    @classmethod
    def makemessages(cls) -> None:  # pragma: no cover
        """
        Analyses all strings in the project and extracts them.
        """
        for language in cls.SUPPORTED_LOCALES:
            if language == "en":
                # Don't translate the main language
                continue
            file_name = Path(__file__).parent / "locale" / language \
                / "LC_MESSAGES" / "squirrelbattle.po"
            args = ["find", "squirrelbattle", "-iname", "*.py"]
            find = subprocess.Popen(args, cwd=Path(__file__).parent.parent,
                                    stdout=subprocess.PIPE)
            args = ["xargs", "xgettext", "--from-code", "utf-8",
                    "--add-comments",
                    "--package-name=squirrelbattle",
                    "--package-version=23.14",
                    "--copyright-holder=ÿnérant, eichhornchen, "
                    "nicomarg, charlse, ifugao",
                    "--msgid-bugs-address=squirrel-battle@crans.org",
                    "--sort-by-file",
                    "-o", file_name]
            if file_name.is_file():
                args.append("--join-existing")
                with open(file_name, "r") as f:
                    content = f.read()
                with open(file_name, "w") as f:
                    f.write(re.sub("#:.*\n", "", content))
            print(f"Make {language} messages...")
            subprocess.Popen(args, stdin=find.stdout).wait()

    @classmethod
    def compilemessages(cls) -> None:
        """
        Compiles translation messages from source files.
        """
        for language in cls.SUPPORTED_LOCALES:
            if language == "en":
                continue
            args = ["msgfmt", "--check-format",
                    "-o", Path(__file__).parent / "locale" / language
                    / "LC_MESSAGES" / "squirrelbattle.mo",
                    Path(__file__).parent / "locale" / language
                    / "LC_MESSAGES" / "squirrelbattle.po"]
            print(f"Compiling {language} messages...")
            subprocess.Popen(args).wait()


def gettext(message: str) -> str:
    """
    Translates a message.
    """
    return Translator.get_translator().gettext(message)


Translator.refresh_translations()
