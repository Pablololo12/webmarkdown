from typing import Any
from pathlib import Path
from .checkpointer import Checkpointer
import re
import os
import shutil

def parse(line: str) -> str:
    def modify_link(match):
        t = match.group(1)
        u = match.group(2)
        if ".md" in u:
            u = u.replace(".md", ".html")
        return "<a href={}>{}</a>".format(u,t)
    def modify_image(match):
        t = match.group(1)
        u = match.group(2)
        return "<img src=\"{}\" alt=\"{}\">".format(u,t)
    line = re.sub(r"(?<!\!)\[([^\]]+)\]\(([^)]+)\)", modify_link, line)
    line = re.sub(r"!\[([^\]]+)\]\(([^)]+)\)", modify_image, line)
    if line == "":
        return ""
    elif line.startswith('#'):
        count = sum([1 for x in line if x=='#'])
        return "<h{}>{}</h{}>".format(count, line.replace("#",""), count)
    else:
        return "<p>{}</p>".format(line)

def get_block(start: bool, line: str) -> str:
    if start:
        line = line.replace("---","")
        sp = line.split(" ")
        if sp[-1].startswith("{"):
            lang = sp[-1].replace("{","").replace("}","")
            line = " ".join(sp[0:-1])
            return "<div class=\"box box-{} language-{}\">".format(line, lang)
        return "<div class=\"box box-{}\">".format(line)
    else:
        return "</div>"

def get_list_block(start: bool) -> str:
    if start:
        return "<ul>"
    else:
        return "</ul>"

def generate_page(lines: list[str], conf: dict[str, Any], level: int) -> str:
    title = "No title"
    if lines[0].startswith('#'):
        title = lines[0].replace("#","")
        lines = lines[1:]
    prevpath = ""
    if level > 0:
        for _ in range(level):
            prevpath += '../'
    out = """
        <!DOCTYPE html> <html> <head>
        <meta charset="utf-8" />
        <link rel="stylesheet" href="{}" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
        <link
            href="https://fonts.googleapis.com/css2?family=Advent+Pro:ital,wght@0,100..900;1,100..900&family=JetBrains+Mono:ital,wght@0,100..800;1,100..800&display=swap"
            rel="stylesheet"
        />
        <title>{}</title>
        <base target="_blank" />
        </head>
        <body>
    """.format(prevpath+conf["style"], title)
    block = False
    listblock = False
    for line in lines:
        if line == "{{language-selector}}":
            out += """<div class=\"box \"box-language\" id=\"lang-switch\">"""
            for lang in conf["langs"]:
                out += "<button onclick=\"setLang('{}')\">{}</button>".format(lang,conf["langs"][lang])
            out += """</div>"""
            continue
        elif line.startswith("---"):
            if block:
                block = False
            else:
                block = True
            out += get_block(block, line)
            continue
        elif line.startswith("- "):
            if not listblock:
                out += get_list_block(True)
                listblock = True
        elif listblock:
            out += get_list_block(False)
            listblock = False
        out += parse(line)
    out += """<script>
    function disable_all() {"""
    for lang in conf["langs"]:
        out += """
        document.querySelectorAll('.language-{}')
            .forEach(div => div.style.display = 'none');
        """.format(lang)
    out += """
    } function setLang(lang) {
    disable_all();
    document.cookie = `lang=${lang}; path=/; max-age=31536000`;
    document.querySelectorAll('.language-'+lang).forEach(div => div.style.display = 'block');
    }
    function getLang() {
    const match = document.cookie.match(/(?:^|; )lang=([^;]*)/);
      return match ? match[1] : "en";
    }
    setLang(getLang());
        </script>
        </body>
        </html>
    """
    return out

def create_html_file(filename: str, outfilename: str, conf: dict[str, Any]):
    with open(filename, 'r') as file:
        lines = [f.strip() for f in file.readlines()]
        level = sum([1 for x in outfilename if x=='/'])
        out = generate_page(lines, conf, level)
        outf = Path(outfilename)
        folder = outf.parent
        chk = Checkpointer()
        if not folder.exists():
            folder.mkdir(parents=True, exist_ok=True)
            chk.folder_created(folder)
        with open(outfilename, 'w') as ooo:
            ooo.write(out)
            chk.file_created(outfilename)

def generate_html(conf: dict[str, Any]):
    for root, dirs, files in os.walk(conf["directory"]):
        direc = root.removeprefix(conf["directory"])
        if direc.startswith("/"):
            direc = direc.removeprefix("/")
        for f in files:
            if not f.endswith(".md"):
                continue
            html = f.replace(".md", ".html")
            newF = os.path.join(direc, html)
            orig = os.path.join(root,f)
            create_html_file(orig, newF, conf)

def copy_assets(conf: dict[str, Any]):
    if "assets" not in conf:
        return
    chk = Checkpointer()
    for asset in conf["assets"]:
        shutil.copytree(os.path.join(conf["directory"], asset), asset, dirs_exist_ok=True)
        chk.folder_created(asset)
