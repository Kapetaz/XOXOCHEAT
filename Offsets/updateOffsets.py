import sys

def update_offsets(fonte):

    print("updating offsets...")

    fonte = fonte.replace('[signatures]','#signatures\n').replace('[netvars]','#netvars\n')
    
    try:
        open("../Hacks/offsets.py",'w').write(fonte)
        print("update sucessfull!")
    except:
        print('"offsets.py" not found')

def init():

    FAILED = False

    try:
        import requests
    except:
        print("Instalando a biblioteca requests...")
        try:
            os.system('python -m pip install requests')
        except:
            print("ERRO na instalação da biblioteca.")
            FAILED = True

    if not FAILED:
        try:
            offsets = requests.get("https://raw.githubusercontent.com/frk1/hazedumper/master/csgo.toml").text
            del requests
            update_offsets(offsets)
        except:
            print("ERROR: Failed to connect")