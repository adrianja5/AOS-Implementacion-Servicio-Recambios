class HTTP404Exception(Exception):
  def __init__(self) -> None:
    pass


class HTTP400Exception(Exception):
  def __init__(self, detail: str) -> None:
    self.detail = detail


class HTTP409Exception(Exception):
  def __init__(self, detail: str) -> None:
    self.detail = detail


class HTTP412Exception(Exception):
  def __init__(self) -> None:
    pass