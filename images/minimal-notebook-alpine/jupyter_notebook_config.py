c = get_config()  # noqa: F821
# Listen on all interfaces (ipv4 and ipv6)
c.NotebookApp.ip = ""
c.NotebookApp.password = ""
c.NotebookApp.token = ""
c.NotebookApp.open_browser = False
c.NotebookApp.show_banner = False

# to output both image/svg+xml and application/pdf plot formats in the notebook file
c.InlineBackend.figure_formats = {"png", "jpeg", "svg", "pdf"}

c.FilesystemManager.trash_enabled = False