from sym.cli.helpers import updater


class SymUpdater(updater.SymUpdater):
    def __init__(self):
        super().__init__(cli="sym-flow-cli")
