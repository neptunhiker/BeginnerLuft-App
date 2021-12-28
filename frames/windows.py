def set_dpi_awareness() -> None:
    """Gives better quality of tk fonts etc."""
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    except:
        pass
