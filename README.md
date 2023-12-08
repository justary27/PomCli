# PomCli
`A pom.xml CLI parser for your GitHub repos.`

A Command Line Interface application that uses [GitHub app](https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/differences-between-github-apps-and-oauth-apps) capabilities to search and parse the `pom.xml` files in the user's repositories. Parsed results show the dependencies in that pom file.

## Setup

1. Create a GitHub app with scopes from repository read access and user info.
2. Put the client id & secret as in the `.sample.env` file and rename it to `.env`
3. Install the required dependencies
```bash
pip install -r requirements.txt
```
4. _(Optional) If you want to use the program as an executable, run the `executable.sh` file, make sure to replace the path there!_
4. Run the CLI with the following command.
```bash
python ./run.py
```

## Commands

- `login`: The login command, logs the user via the github device code OAuth service.

![loginUsage](https://github.com/just-ary27/PomCli/assets/76696648/75a23dd2-dd84-4f4f-81e2-79896ba64992)

- `listRepos`: The listRepos command, lists all the repositories of the currently logged in user.

![listReposUsage](https://github.com/just-ary27/PomCli/assets/76696648/5bd2a03f-e289-477b-8969-69195577ddc4)

- `selectRepo`: The selectRepo command, selects one of the repositories to search for pom.xml files in it.

![selectRepoUsage](https://github.com/just-ary27/PomCli/assets/76696648/b3011c62-adf4-462c-a201-676ad8bdb597)

- `searchPom`: The searchPom command, searches and lists all the pom.xml files in the currently selected repository.

![searchPomUsage](https://github.com/just-ary27/PomCli/assets/76696648/fbf05534-dc51-4146-a960-51d379470014)

- `listPomDep`: The listPomDep command, lists all the dependencies of the currently selected pom.xml file in the currently selected repository.

![listDPomDep](https://github.com/just-ary27/PomCli/assets/76696648/6c9eb4ac-64f4-4b2f-8735-ae6bb660648a)

- `clear`: Clears the terminal
- `..`: Goes to previous level command.

![,,Usage](https://github.com/just-ary27/PomCli/assets/76696648/c4a2226b-6661-4c97-a11d-0092cb8fa68c)

- `logout`: Logs out the current user and exits from the CLI.

![logoutUsage](https://github.com/just-ary27/PomCli/assets/76696648/4544f335-aded-4ff8-9a3d-2d9d5825f333)

- `exit`: Exit from the PomCli.

![ExitUsage](https://github.com/just-ary27/PomCli/assets/76696648/03a701c4-55a8-4388-9187-0e3eb77827af)

## Future Ideas
- [Add refresh token logic to the login function.](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/refreshing-user-access-tokens)
- Fix the help function.
- Print the selected `pom.xml` file.