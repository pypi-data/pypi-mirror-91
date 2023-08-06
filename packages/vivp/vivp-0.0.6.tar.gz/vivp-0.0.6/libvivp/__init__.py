import os
import json
from .utils import is_vivp_dir, VPACKAGE_JSON, is_valid_git_url, VPACKAGE_HIDDEN, get_repos_dir, get_cache_dir, is_sub_file
from .vPackage import vPackage
from git import Git
import git
import shutil
import subprocess

def setup(vivp_dir, packageName, packageAuthors, packageURL):
    if is_vivp_dir(vivp_dir):
        raise Exception("Already VIVP directory")
    p = vPackage(filePath=os.path.join(vivp_dir, VPACKAGE_JSON), createNew=True, saveable=True)
    p.data['packageDetails']['packageName'] = packageName
    p.data['packageDetails']['packageAuthors'] = packageAuthors
    if packageURL:
        if (is_valid_git_url(packageURL)):
            p.data['packageURL'] = packageURL
        else:
            raise Exception('Invalid packageURL : ' + packageURL)
    #g = Git(vivp_dir)
    p.save()
    print(p)
    pass

def install(vivp_dir, package_list):
    if not is_vivp_dir(vivp_dir):
        raise Exception("Not VIVP directory")
    p = vPackage(filePath=os.path.join(vivp_dir, VPACKAGE_JSON), createNew=False, saveable=True)


    for dep in package_list:
        if is_valid_git_url(dep):
            if not p.has_dependency(dep):
                p.data['dependencyList'].append(dep)
            else:
                raise Exception('Dependency already added: ' + dep)
        else:
            raise Exception('Invalid dependency : ' + dep)
    
    p.save()
    print(p)
    refresh_all_dependencies(vivp_dir)
    pass

def update(vivp_dir, package_list):
    if not is_vivp_dir(vivp_dir):
        raise Exception("Not VIVP directory")
    refresh_all_dependencies(vivp_dir)

def remove(vivp_dir, package_list):
    if not is_vivp_dir(vivp_dir):
        raise Exception("Not VIVP directory")
    p = vPackage(filePath=os.path.join(vivp_dir, VPACKAGE_JSON), createNew=False, saveable=True)


    for dep in package_list:
        if is_valid_git_url(dep):
            if p.has_dependency(dep):
                p.data['dependencyList'].remove(dep)
            else:
                raise Exception('Dependency does not in list : ' + dep)
        else:
            raise Exception('Invalid dependency : ' + dep)
    
    p.save()
    print(p)
    refresh_all_dependencies(vivp_dir)
    pass

def list_vivp(vivp_dir):
    if not is_vivp_dir(vivp_dir):
        raise Exception("Not VIVP directory")
    pass

def refresh_all_dependencies(vivp_dir):
    if not is_vivp_dir(vivp_dir):
        raise Exception("Not VIVP directory")
    p = vPackage(filePath=os.path.join(vivp_dir, VPACKAGE_JSON), createNew=False, saveable=False)

    print("[vivp]", "Clearing cache")
    CACHE_DIR = get_cache_dir(vivp_dir)
    REPOS_DIR = get_repos_dir(vivp_dir)
    # Remove VPACKAGE_HIDDEN directory
    if os.path.isdir(CACHE_DIR):
        #os.rm(CACHE_DIR)
        shutil.rmtree(CACHE_DIR)

    os.makedirs(CACHE_DIR)
    os.makedirs(REPOS_DIR)

    # iterate through all packages and clone
    for dep in p.data['dependencyList']:
        print("[vivp]", "git clone ", dep)
        output = git.Git(REPOS_DIR).clone(dep)
        print(output)

    pass

def get_files_from_dependencies(vivp_dir):
    if not is_vivp_dir(vivp_dir):
        raise Exception("Not VIVP directory")
    p = vPackage(filePath=os.path.join(vivp_dir, VPACKAGE_JSON), createNew=False, saveable=False)
    dependency_files_list = []
    if os.path.isdir(get_repos_dir(vivp_dir)):
        folder_list = os.listdir(get_repos_dir(vivp_dir))
        for dep in folder_list:
            package_dep_path = os.path.join(get_repos_dir(vivp_dir), dep)
            p = vPackage(filePath=os.path.join(package_dep_path, VPACKAGE_JSON), createNew=False, saveable=False)
            for dep_file in p.data['fileList']:
                dependency_files_list.append(os.path.join(package_dep_path, dep_file))
    return dependency_files_list

def execute(vivp_dir):
    if not is_vivp_dir(vivp_dir):
        raise Exception("Not VIVP directory")
    p = vPackage(filePath=os.path.join(vivp_dir, VPACKAGE_JSON), createNew=False, saveable=True)
    file_list = []
    for f in p.data['fileList']:
        file_list.append(f)
    for f in p.data['testBench']:
        file_list.append(f)
    dependency_files = get_files_from_dependencies(vivp_dir)
    for f in dependency_files:
        file_list.append(f)

    vcd_files = list(filter(lambda x: x.endswith(".vcd"), os.listdir() ))
    for vcd_file in vcd_files:
        os.remove(vcd_file)
    
    out_files = list(filter(lambda x: x.endswith(".out"), os.listdir() ))
    for out_file in out_files:
        os.remove(out_file)

    # TODO : Load files from .vpackage/repos/

    exec_str = "iverilog " + " ".join(file_list)
    print("[vivp]", exec_str)
    proc = subprocess.Popen(exec_str.split(" "))
    proc.wait()

    exec_str = "vvp a.out" # check list of .out files
    print("[vivp]", exec_str)
    proc = subprocess.Popen(exec_str.split(" "))
    proc.wait()

    vcd_files = list(filter(lambda x: x.endswith(".vcd"), os.listdir() ))
    if len(vcd_files)==0:
        Exception("Failed : no VCD Files")
    elif len(vcd_files)==1:
        exec_str = "gtkwave " + vcd_files[0]
        print("[vivp]", exec_str)
        proc = subprocess.Popen(exec_str.split(" "))
        proc.wait()
        print("[vivp]", "Done...")
    else:
        Exception("Failed : too many VCD Files")
    pass

def add_files(vivp_dir, file_list):
    if not is_vivp_dir(vivp_dir):
        raise Exception("Not VIVP directory")
    p = vPackage(filePath=os.path.join(vivp_dir, VPACKAGE_JSON), createNew=False, saveable=True)
    for f in file_list:
        if is_sub_file(vivp_dir, f):
            if not p.has_file(f):
                p.data['fileList'].append(f)
            else:
                raise Exception("File already in list : " + f)
        else:
            raise Exception("Invalid path : " + f)
    p.save()

def remove_files(vivp_dir, file_list):
    if not is_vivp_dir(vivp_dir):
        raise Exception("Not VIVP directory")
    p = vPackage(filePath=os.path.join(vivp_dir, VPACKAGE_JSON), createNew=False, saveable=True)
    for f in file_list:
        if is_sub_file(vivp_dir, f):
            if p.has_file(f):
                p.data['fileList'].remove(f)
            else:
                raise Exception("File not in list : " + f)
        else:
            raise Exception("Invalid path : " + f)
    p.save()

def add_testbench(vivp_dir, file_list):
    if not is_vivp_dir(vivp_dir):
        raise Exception("Not VIVP directory")
    p = vPackage(filePath=os.path.join(vivp_dir, VPACKAGE_JSON), createNew=False, saveable=True)
    for f in file_list:
        if is_sub_file(vivp_dir, f):
            if not p.has_testbench(f):
                p.data['testBench'].append(f)
            else:
                raise Exception("File already in list : " + f)
        else:
            raise Exception("Invalid path : " + f)
    p.save()

def remove_testbench(vivp_dir, file_list):
    if not is_vivp_dir(vivp_dir):
        raise Exception("Not VIVP directory")
    p = vPackage(filePath=os.path.join(vivp_dir, VPACKAGE_JSON), createNew=False, saveable=True)
    for f in file_list:
        if is_sub_file(vivp_dir, f):
            if p.has_testbench(f):
                p.data['testBench'].remove(f)
            else:
                raise Exception("File not in list : " + f)
        else:
            raise Exception("Invalid path : " + f)
    p.save()