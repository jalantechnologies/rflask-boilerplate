class FileManager:
  def __init__(self, filename, mode) -> None:
    self.filename = filename
    self.mode = mode
    self.file = None

  def __enter__(self):
    self.file = open(self.filename, self.mode)
    return self.file

  def __exit__(self, exc_type, exc_value, exc_traceback) -> None:
    self.file.close()
