#!/usr/bin/python3

import re
import sys
import subprocess

from mendeleev import element


def create_card(atomno, template, size="poker"):
    el = element(atomno)
    mass = str(el.mass)
    atomic_number = str(el.atomic_number)

    econf = re.sub(r"(\d) ", r"^{\g<1>} ", el.econf)
    econf = re.sub(r"(\d)$", r"^{\g<1>}", econf)

    footer_items = [mass, el.name]
    header_items = ["\ce{" + econf + "}"]

    footer = "\n\n".join(map(str, footer_items))
    header = "\hfill{}".join(map(str, header_items))
    if len(header_items) < 2:
        header = "\hfill{}" + header

    texcode = (template
               .replace("$ATOMIC_NUMBER", atomic_number)
               .replace("$SYMBOL", el.symbol)
               .replace("$HEADER", header)
               .replace("$FOOTER", footer))

    texcode = texcode.replace("$HEIGHT", "3.5in")
    texcode = texcode.replace("$WIDTH", "2.5in")
    if size == "poker":
        texcode = texcode.replace("$WIDTH", "2.5in")
    elif size == "bridge":
        texcode = texcode.replace("$WIDTH", "2.25in")

    path = "{}_{}.tex".format(atomic_number, mass)
    with open(path, "w") as stream:
        stream.write(texcode)
    subprocess.run(["latexmk", "-f", "-pdf", path])


def main():
    with open("template.tex") as stream:
        template = stream.read()

        if len(sys.argv) < 1 or sys.argv[1] == "all":
            for atomno in range(1, 119):
                create_card(atomno, template)
        else:
            create_card(int(sys.argv[1]), template)


if __name__ == "__main__":
    main()
