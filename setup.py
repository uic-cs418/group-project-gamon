import os
import requests
import zipfile

current_dir = os.getcwd()


filenames = [
        "CoreTrends2018.zip",
        "CoreTrends2021.zip",
        "CoreTrends2019.zip",
        "NSDUH2018.zip",
        "NSDUH2019.zip",
        "NSDUH2021.zip",
        "NSDUH2022.zip",
        ]

dirs = {
        'datasets/January 3-10, 2018 - Core Trends Survey' : "https://www.pewresearch.org/wp-content/uploads/sites/20/2018/05/January-3-10-2018-Core-Trends-Survey.zip",
        'datasets/January-8-February-7-2019-Core-Trends-Survey-SPS' : "https://www.pewresearch.org/wp-content/uploads/sites/20/2019/10/January-8-February-7-2019-Core-Trends-Survey-SPSS.zip",
        'datasets/Jan-25-Feb-8-2021-Core-Trends-Survey' : "https://www.pewresearch.org/wp-content/uploads/sites/20/2022/05/Jan-25-Feb-8-2021-Core-Trends-Survey.zip",
        'datasets/National Survey on Drug Use and Health 2018' : "https://www.datafiles.samhsa.gov/sites/default/files/field-uploads-protected/studies/NSDUH-2018/NSDUH-2018-datasets/NSDUH-2018-DS0001/NSDUH-2018-DS0001-bundles-with-study-info/NSDUH-2018-DS0001-bndl-data-tsv.zip",
        'datasets/National Survey on Drug Use and Health 2019' : "https://www.datafiles.samhsa.gov/sites/default/files/field-uploads-protected/studies/NSDUH-2019/NSDUH-2019-datasets/NSDUH-2019-DS0001/NSDUH-2019-DS0001-bundles-with-study-info/NSDUH-2019-DS0001-bndl-data-tsv.zip",
        'datasets/National Survey on Drug Use and Health 2021' : "https://www.datafiles.samhsa.gov/sites/default/files/field-uploads-protected/studies/NSDUH-2021/NSDUH-2021-datasets/NSDUH-2021-DS0001/NSDUH-2021-DS0001-bundles-with-study-info/NSDUH-2021-DS0001-bndl-data-tsv_v4.zip",
        'datasets/National Survey on Drug Use and Health 2022' : "https://www.datafiles.samhsa.gov/sites/default/files/field-uploads-protected/studies/NSDUH-2022/NSDUH-2022-datasets/NSDUH-2022-DS0001/NSDUH-2022-DS0001-bundles-with-study-info/NSDUH-2022-DS0001-bndl-data-tsv_v1.zip"
        }

assert len(filenames) == len(dirs)

print("Creating directories...")
os.makedirs("tmp")
for dir in dirs.keys():
    print(f"mkdir: {dir}")
    os.makedirs(dir)

print("Completed creating directories")

print("Downloading files and unzipping")
for dir, filename in zip(dirs, filenames):
    print()
    response = requests.get(dirs[dir])
    print(f"{filename} - {response}")

    print(f"Writing {filename} to 'tmp/'")
    with open(f"tmp/{filename}", 'wb') as f:
        f.write(response.content)

    print(f"Unzipping contents to {dir}/")
    with zipfile.ZipFile(f"tmp/{filename}", "r") as zip:
        zip.extractall(f"{dir}/.")

print("Done, cleaning up now")
for filename in filenames:
    os.remove(f"tmp/{filename}")
os.removedirs("tmp")
