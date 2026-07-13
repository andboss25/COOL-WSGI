
import json
import sys
import zipfile
import os
import shutil

# Yeah ik i need to organize and refactor ts

template_location = sys.argv[sys.argv.index("--template") + 1]

if sys.argv[1] == "make":
    if not os.path.isdir(template_location):
        print("Not a valid folder!")
    z = zipfile.ZipFile(f"{template_location}.tmp","w")
    for root, dirs, files in os.walk(template_location):
        arcname = os.path.relpath(root, template_location)
        if arcname != '.':
            z.write(root, arcname)
        
        for file in files:
            file_path = os.path.join(root, file)
            arcname_file = os.path.relpath(file_path, template_location)
            z.write(file_path, arcname_file)

elif sys.argv[1] == "install":
    app_location = sys.argv[sys.argv.index("--app") + 1]
    z = zipfile.ZipFile(f"{template_location}.tmp","r")
    z.extractall("__template__")

    manifest_original : dict = json.load(open(
        os.path.join(
            "__template__",
            "manifest.json"
        ),"r"
    ))

    manifest = manifest_original

    manifest.pop("name")
    manifest.pop("version")

    target_manifest = open(os.path.join(
        app_location,
        "manifest.json"
    ),"r")


    target_manifest_data = json.load(
        target_manifest
    )

    target_manifest = open(os.path.join(
        app_location,
        "manifest.json"
    ),"w")

    for key in manifest.keys():
        try:
            for key2 in manifest[key]:
                target_manifest_data[key][key2].extend(manifest[key][key2])
        except:

            target_manifest_data[key] = manifest[key]

    target_manifest.write(
        json.dumps(target_manifest_data,indent=3)
    )

    target_manifest.close()

    os.remove(os.path.join(
        "__template__",
        "manifest.json"
    ))

    shutil.copytree(
        "__template__",
        app_location,
        dirs_exist_ok= True
    )

# TODO test