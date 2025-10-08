class ScriptContext:
    """
    Jednostavna helper klasa koja pomaže prilikom dijeljenja informacija između
    main metode skripte i wrappera (error handlera).

    Primarno se koristi za dijeljenje informacija o objektu za konekciju na bazu podataka jer
    se informacije o logovima koji su potrebni prilikom slanja mailova
    dohvaćaju kroz taj isti objekt.
    """

    def __init__(self):
        self.db = None
