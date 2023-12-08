# PomCli
`A pom.xml CLI parser for your GitHub repos.`

A Command Line Interface application that uses GitHub app capabilities to search and parse the `pom.xml` files in user's repositories. Parsed results show the dependencies in that pom file.

## Setup

1. Create a GitHub app with scopes from repository read access and user info.
2. Put the client id & secret as in the `.sample.env` file and rename it to `.env`
3. Install the required dependencies
```bash
pip install -r requirements.txt
```
4. _(Optional) If you want to use the program as an executable run the `executable.sh` file, make sure to replace the path there!_
4. Run the cli with the following command
```bash
python ./run.py
```

## Commands

- `login`: The login command, logs the user via the github device code OAuth sevice.
- `listRepos`: The listRepos command, lists all the repositories of the currently logged in user.
- `selectRepo`: The selectRepo command, selects one of the repositories to search for pom.xml files in it.
- `searchPom`: The searchPom command, searches and lists all the pom.xml files in the currently selected the repository.
- `listPomDep`: The listPomDep command, lists all the dependencies of the currently selected pom.xml file in the currently selected repository.
- `clear`: Clears the terminal
- `..`: Goes to previous level command.
- `logout`: Logs out the current user.
- `exit`: Exit from the PomCli.
