import json
import mimetypes
import os
import re

config_file = "variables.json"

types_map = mimetypes.types_map.copy()
types_map.update({".toml": "text/toml"})
types_map.update({".md": "text/md"})


def search_and_replace(file_path, src_txt, dst_txt):
    # Read in the file
    with open(file_path, "r") as file:
        file_data = file.read()

    # Replace the target string
    file_data = file_data.replace(src_txt, dst_txt)

    # Write the file out again
    with open(file_path, "w") as file:
        file.write(file_data)


def bootstrap():
    with open(config_file) as f:
        config = json.load(f)

    for root, dirs, files in os.walk("."):
        # Rename folders
        new_root = root
        for var, value in config.items():
            new_root = re.sub(var, value, new_root)
        if new_root != root:
            os.rename(root, new_root)
            root = new_root
        # Now dirs
        for i, dir in enumerate(dirs):
            new_dir = dir
            for var, value in config.items():
                new_dir = re.sub(var, value, new_dir)
            if new_dir != dir:
                os.rename(os.path.join(root, dir), os.path.join(root, new_dir))
                dirs[i] = new_dir

        # Rename files
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext in types_map:
                if types_map[ext].split("/")[0] == "text":
                    new_file = file
                    for var, value in config.items():
                        new_file = re.sub(var, value, new_file)
                    if new_file != file:
                        os.rename(
                            os.path.join(root, file), os.path.join(root, new_file)
                        )

                    # Replace content
                    os.path.join(root, new_file)
                    for var, value in config.items():
                        search_and_replace(os.path.join(root, new_file), var, value)

    print("Search and replace complete")

    # Now we remove lines from readme that are not needed, i.e. from `## Templating` to the next `##`

    with open("README.md", "r") as f:
        lines = f.readlines()

    skip = False
    with open("README.md", "w") as f:
        for line in lines:
            if "## Templating" in line:
                skip = True
            elif skip and line.startswith("##"):
                skip = False
            if not skip:
                f.write(line)

    print("README.md cleaned")

    # Finally destroy the bootstrap.py and variables.json files
    os.remove("bootstrap.py")
    os.remove("variables.json")


if __name__ == "__main__":
    bootstrap()
