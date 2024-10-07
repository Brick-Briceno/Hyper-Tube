import json

class conf:
    #Configuración por defecto
    def __init__(self):
        self.name_conf = "conf.ini"
        self.config = {
            "video path": "%USERPROFILE%/Videos/YT",
            "resolution": "1080p",
            "overlay subs": True,
            "list count": True,
            "first time": True,
            "lang subs": "es",
            "video list": {
                "ID": ["pene lalala", "8", "por culo te lo esmorocho"],
                "Name": ["pene lalala jeje", "8", "Name"],
                "Data": [False, False, False],
                }
            }

    def __getitem__(self, dato): return self.config[dato]

    def __setitem__(self, consulta, respuesta): self.config[consulta] = respuesta

    def guardar(self):
        with open(self.name_conf, "w") as f:
            json.dump(self.config, f, indent=4)

    def cargar(self):
        try:
            with open(self.name_conf, "r") as f:
                self.config = json.load(f)
        except FileNotFoundError:
            conf.guardar(self)

cf = conf()
cf.cargar()
