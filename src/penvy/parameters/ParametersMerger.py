class ParametersMerger:
    def merge(self, a, b, overwrite=True, path=None):
        """merges b into a"""
        if path is None:
            path = []

        for key in b:
            if key in a:
                if isinstance(a[key], dict) and isinstance(b[key], dict):
                    self.merge(a[key], b[key], overwrite, path + [str(key)])
                elif a[key] == b[key]:
                    pass  # same leaf value
                elif overwrite is True:
                    a[key] = b[key]
                else:
                    raise Exception(f"Conflict at {'.'.join(path + [str(key)])}")
            else:
                a[key] = b[key]
        return a
