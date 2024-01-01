from interface.basefile import BaseFile


class PomFile(BaseFile):
    """
    Model class for a pom.xml file obtained from a GitHub repository.
    """

    def __init__(self, name:str, path:str, url:str) -> None:
        self.name = name
        self.url = url
        self.path = path
        self.FILE_EXTENSION = '.xml'

    def get_dependencies(self, data:str) -> list:
        """
        Print dependencies list in the instance of pom.xml file
        """

        self.set_data(data)

        dependencies = []

        dependencies_start = self.decoded_data.find("<dependencies>")
        dependencies_end = self.decoded_data.find("</dependencies>", dependencies_start)

        if dependencies_start != -1 and dependencies_end != -1:
            dependencies_content = self.decoded_data[dependencies_start + len("<dependencies>"):dependencies_end]

            dependency_tags = dependencies_content.split("<dependency>")[1:]

            for dependency_tag in dependency_tags:
                group_id_start = dependency_tag.find("<groupId>") + len("<groupId>")
                group_id_end = dependency_tag.find("</groupId>")
                group_id = dependency_tag[group_id_start:group_id_end].strip()

                artifact_id_start = dependency_tag.find("<artifactId>") + len("<artifactId>")
                artifact_id_end = dependency_tag.find("</artifactId>")
                artifact_id = dependency_tag[artifact_id_start:artifact_id_end].strip()

                version_start = dependency_tag.find("<version>") + len("<version>")
                version_end = dependency_tag.find("</version>")
                version = dependency_tag[version_start:version_end].strip() if version_start != 8 else "-"

                dependencies.append({
                    'group_id': group_id,
                    'artifact_id': artifact_id,
                    'version': version
                })

        return dependencies
