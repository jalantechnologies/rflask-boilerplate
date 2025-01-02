from pathlib import Path

class ConfigUtils:
    
    @staticmethod
    def get_parent_directory(directory: str, levels: int) -> Path:
        parent_dir = Path(directory)
        for _ in range(levels):
            parent_dir = parent_dir.parent
        return parent_dir
