class Console:
    @staticmethod
    def Log(*args):
        print("[Log]", *args)

    @staticmethod
    def Error(*args):
        print("\033[91m[Error] {}\033[00m".format(*args))
