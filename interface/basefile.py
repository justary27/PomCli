import base64
import subprocess
from abc import ABC

class BaseFile(ABC):
    """
    BaseFile abstract class for all types of files.
    """

    name:str
    url:str
    path:str
    raw_data:str
    decoded_data:str
    FILE_EXTENSION:str
    

    def set_data(self, data:str) -> None:
        """
        Decodes the base64 encoded data string of 
        pom.xml file from GitHub to a normal utf-8 
        encoded one.
        """

        self.raw_data = data
        self.decoded_data = base64.b64decode(
            self.raw_data
        ).decode("utf-8")

    def print_file(self) -> None:
        """
        Outputs the file in vim.
        """

        script_path = '/scripts/vi.sh'

        # Suffix for the temporary file
        suffix = BaseFile.file_extension

        # Run the Bash script with the Base64 string 
        # and suffix arguments using subprocess
        subprocess.run(
            [
                script_path, '-b', BaseFile.decoded_data, 
                '-s', suffix
            ], 
            check=True
        )
