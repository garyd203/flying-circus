"""Various tools to configure the behaviour of Flying Circus on-the-fly [sic]."""


class ExportContext(object):
    """Controls the way objects export themselves."""

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


class ExportYamlContext(ExportContext):
    """Export data as YAML."""
    pass
