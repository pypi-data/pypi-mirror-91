import re
import os
import tmdbsimple as tmdb
import click


class ApiKeyParamType(click.ParamType):
    name = "api-key"

    def convert(self, value, param, ctx):
        found = re.match(r"[0-9a-f]{32}", value)

        if not found:
            self.fail(
                f"{value} is not a 32-character hexadecimal string",
                param,
                ctx,
            )

        return value


class ExtParamType(click.ParamType):
    name = "extension"

    def convert(self, value, param, ctx):
        found = re.match(r"^$|^.[A-Za-z]", value)

        if not found:
            self.fail(
                f"{value} isn't a string that starts with '.' and consist only letters"
            )

        return value


def replace_illegal(s):
    illegal = ["\\", "/", ":", "*", '"', "<", ">", "|", "?"]
    for c in illegal:
        s = s.replace(c, "")
    return s


@click.group(chain=True)
@click.pass_context
def cli(ctx):
    ctx.obj = {}


@cli.command("tmdb-api")
@click.option(
    "--api-key",
    "-a",
    envvar="API_KEY",
    type=ApiKeyParamType(),
    prompt="Enter your API key from TMDb",
    help="Your API key for the TMDb (it can be stored in system variable under 'API_KEY' name).",
)
@click.option(
    "--query",
    "-q",
    required=True,
    type=click.STRING,
    help="Search query that should contain name of TV show.",
)
@click.option("--season", "-s", required=True, type=click.INT, help="Season number.")
@click.pass_context
def tmdb_api(ctx, api_key, query, season):
    tmdb.API_KEY = api_key
    search = tmdb.Search()
    search.tv(query=query)
    for i, s in enumerate(search.results):
        print(
            f"{i}." + " " + s["name"],
            s["original_name"],
            s["first_air_date"],
            sep=" - ",
        )

    if not search.results:
        exit(f"Cant find anything for your query: {query}")

    choice = click.prompt(
        "Enter number corresponding to TV show", type=click.IntRange(min=0, max=i)
    )
    id = search.results[choice]["id"]

    tv = tmdb.TV(id=id)
    seasons = tv.info()["number_of_seasons"]
    if season > seasons:
        print(
            "You ask for a season that doesn't exist, this TV show only has",
            seasons,
            "season" if seasons == 1 else "seasons",
        )
        exit()

    tv_season = tmdb.TV_Seasons(tv_id=id, season_number=season)
    tv_season.info()
    for episode in tv_season.episodes:
        ctx.obj.setdefault("episodes", []).append(replace_illegal(episode["name"]))


@cli.command("renamer")
@click.option(
    "--path",
    "-p",
    type=click.Path(),
    default=lambda: os.getcwd(),
    show_default="current directory",
    help="Path to the directory with files for renaming.",
)
@click.option(
    "--extension",
    "-e",
    type=ExtParamType(),
    default="",
    show_default="None, all files in a directory will be matched and renamed",
    help="Extension for files that should be renamed",
)
@click.pass_context
def renamer(ctx, path, extension):
    try:
        os.chdir(path)
        path = os.getcwd()
    except OSError:
        print("Path you entered doesn't exist:", path)

    series_list = [
        f"{i:0>2}. {episode}" for i, episode in enumerate(ctx.obj["episodes"], start=1)
    ]
    files_list = [file for file in next(os.walk("."))[2] if file.endswith(extension)]

    if files_list:
        ext_lambda = lambda p: os.path.splitext(p)[1]
        print("All of your file will be renamed the following way:")
        for src, dst in zip(files_list, series_list):
            print(
                os.path.join(path, src),
                "->",
                os.path.join(
                    path, "".join([dst, extension if extension else ext_lambda(src)])
                ),
            )
        if click.confirm("Do you want to continue?"):
            for src, dst in zip(files_list, series_list):
                os.rename(
                    os.path.join(path, src),
                    os.path.join(
                        path,
                        "".join([dst, extension if extension else ext_lambda(src)]),
                    ),
                )
            print("Done!")
        else:
            exit("Aborted")
    else:
        exit(f"Can't find any files in this path: {path}")
