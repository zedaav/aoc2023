from typing import List

from nmk.model.resolver import NmkListConfigResolver


class PythonVersion(NmkListConfigResolver):
    def get_value(self, name: str) -> List[str]:
        return ["python3.9"]
