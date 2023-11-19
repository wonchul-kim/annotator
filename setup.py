from setuptools import setup, find_packages 

def get_version():
    try:
        import subprocess
        version = subprocess.check_output(["git", "describe", "--tags", "--abbrev=0"]).decode().strip()
        return version[1:]
    except Exception as err:
        print("Error:", err)
        return "3.0.1"  # Default version if git tag retrieval fails
    

with open('README.md', encoding='utf-8') as f: # README.md 내용 읽어오기
        long_description = f.read()

setup(
        name                    = 'annotator',
        version                 = get_version(),
        long_description        = long_description,
        long_description_content_type = 'text/markdown', 
        description             = 'Annotator',
        author                  = 'wonchul',
        author_email            = 'onedang22@gmail.com',
        # url                     = 'http://192.168.0.27:88/kim.wonchul/aivdata', 
        # download_url        = 'https://github.com/TooTouch/tootorch/archive/v0.1.tar.gz', 
        # install_requires    =  ["torch","torchvision","h5py","tqdm","pillow","opencv-python"], # requirements will do this
        packages                = find_packages(exclude = []),
        keywords                = ['Annotator'], 
        python_requires         = '>=3.8',
        package_data            = {"": ['*.yaml', "*.txt", "*.md", "*.yml"]},
        include_package_data    = True,
        # zip_safe                = False,
    )