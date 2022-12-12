class WrongPigeonGenderExcetion(Exception):
    def __init__(self, role, gender):
        self.message = f"Pohlaví {role} nemůže být {gender}"
        super().__init__(self.message)