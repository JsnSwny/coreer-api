import os
from accounts.models import Language


def load_languages():
	languages = [
    "Python",
    "JavaScript",
    "Java",
    "C",
    "C++",
    "C#",
    "Ruby",
    "Go",
    "Swift",
    "Kotlin",
    "TypeScript",
    "Rust",
    "PHP",
    "Perl",
    "Objective-C",
    "Scala",
    "Haskell",
    "Lua",
    "Shell",
    "HTML",
    "CSS",
    "SQL",
    "R",
    "MATLAB",
    "Groovy",
    "Assembly",
    "VB.NET",
    "Dart",
    "Julia",
    "F#",
    "Elixir",
    "Clojure",
    "Erlang",
    "PowerShell",
    "PL/SQL",
    "Visual Basic",
    "Delphi",
    "Fortran",
    "Ada",
    "Prolog",
    "Lisp",
    "Scheme",
    "COBOL",
    "Pascal",
    "Racket",
    "Rexx",
    "Awk",
    "Tcl",
    "Bash",
    "D",
    "Smalltalk",
    "Logo"
]

	for language in languages:
			print(language)
			language = Language(name=language, icon_name="")
			language.save()