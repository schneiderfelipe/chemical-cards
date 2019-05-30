#!/usr/bin/python3

import re
import argparse
import subprocess

from mendeleev import element


def create_card(atomno, template, size="bridge"):
    el = element(atomno)
    mass = str(el.mass)
    atomic_number = str(el.atomic_number)

    econf = re.sub(r"(\d+) ", r"^{\g<1>} ", el.econf)
    econf = re.sub(r"(\d+)$", r"^{\g<1>}", econf)

    footer_items = [mass, el.name]
    # header_items = [el.abundance_crust, "\ce{" + econf + "}"]
    # header_items = [el.block, "\ce{" + econf + "}"]
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

    # Other sizes: http://copag.com.br/servicos/cartas-personalizadas/
    if size == "poker":
        height, width = "3.5in", "2.5in"
    else:
        # defaults to "bridge"
        height, width = "3.5in", "2.25in"
    texcode = texcode.replace("$HEIGHT", height)
    texcode = texcode.replace("$WIDTH", width)

    path = "{}_{}_{}.tex".format(el.symbol, atomic_number, mass)
    with open(path, "w") as stream:
        stream.write(texcode)
    subprocess.run(["latexmk", "-f", "-pdf", path])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("element")
    parser.add_argument("--size", default="bridge", choices=["bridge", "poker"])
    args = parser.parse_args()

    with open("template.tex") as stream:
        template = stream.read()

        if args.element == "all":
            for atomno in range(1, 119):
                create_card(atomno, template, size=args.size)
        else:
            try:
                create_card(int(args.element), template, size=args.size)
            except ValueError:
                create_card(args.element, template, size=args.size)


if __name__ == "__main__":
    main()
