#/usr/bin/env python3

import os
import requests
import argparse
import configparser
import json

CONFIG_NAME = "crio_cfg.ini"
TOKEN = ""

def parse_args():
  parser = argparse.ArgumentParser(description = \
             "Clone all repositories in organization you join already")
  
  parser.add_argument("-o", "--org", required=True, type=str, help="Organization name")
  parser.add_argument("-d", "--dir", help="The directory where repositories will be cloned")
  args = parser.parse_args()
  return args

def get_token():
  global TOKEN
  config = configparser.ConfigParser()
  config.read(CONFIG_NAME)
  
  try:
    TOKEN = config['DEFAULT']['Token']
  except KeyError:
    print("There is no config file(crio_cfg.ini) or configuration name in file")
    exit(-1)
    
def check_org_is_exist(org):
  global TOKEN
  headers = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {TOKEN}",
    "X-Github-Api-Version": "2022-11-28"
  }
  
  res = requests.get(f"https://api.github.com/orgs/{org}", headers = headers)
  return res.ok

def get_repositories_list(org):
  global TOKEN
  headers = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {TOKEN}",
    "X-Github-Api-Version": "2022-11-28"
  }
  datas = {
    "per_page" : 100,
    "page" : 1
  }
  
  res = requests.get(f"https://api.github.com/orgs/{org}/repos", headers = headers, params = datas)
  json_object = json.loads(res.text)
  
  repo_list = []
  for data in json_object:
    repo_list.append(data['ssh_url'])
    
  return repo_list

def check_directory_is_existed(dirpath):
  return os.path.exists(dirpath) and os.path.isdir(dirpath)

def check_directory_args(dirpath):
  repo_dir = os.path.dirname(os.path.realpath(__file__))
  if dirpath != None:
    is_existed = check_directory_is_existed(dirpath)
    if is_existed == False:
      print("Please check directory is existed. : " + dirpath)
      exit(-1)
    repo_dir = dirpath
  return repo_dir

def move_directory(dirpath):
  os.chdir(dirpath)
  
def clone_repositories(repo_list):
  for repo in repo_list:
    os.system("git clone " + repo)
    
def main():
  get_token()
  args = parse_args()
  repo_dir = check_directory_args(args.dir)
  move_directory(repo_dir)
  
  if check_org_is_exist(args.org) == False:
    print("Please check organization name")
    exit(-1)
    
  repo_list = get_repositories_list(args.org)
  if len(repo_list) == 0:
    print("There is no repository in organization")
    exit(-1)
    
  clone_repositories(repo_list)

if __name__ == '__main__':
  main()
