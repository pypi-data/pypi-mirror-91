class UncalledArgumentError(Exception):
    def __init__(self, dependant_arg, needed_arg):
        if dependant_arg == "catch-rejected":
            self.message = "You can't catch rejected words without also being in debug mode!"

        self.message += f"\nTarget Arg: {dependant_arg} = True"
        self.message += f"\nNeeded Arg: {needed_arg} = True"
        print(self.message)
