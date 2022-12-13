class PigeonAppException(Exception):
    def __init__(self):
        self.message = f"Něco se pokazilo"
        super().__init__(self.message)


class WrongPigeonGenderExcetion(PigeonAppException):
    def __init__(self, role, gender):
        self.message = f"Pohlaví {role} nemůže být {gender}"
        super().__init__(self.message)

class WrongPigeonIdFormat(PigeonAppException):
    def __init__(self, WrongPigeonId):
        self.message = f"Nesprávný formát id holuba: {WrongPigeonId}"
        super().__init__(self.message)