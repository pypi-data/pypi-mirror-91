from pathlib import Path

def find_num(name_txt):
    home = Path.cwd()
    parent  = home.parent
    sou = Path(parent, "k_ege.egg-info", name_txt)
    read = sou.open().read()
    print(read)

find_num("ty.txt")