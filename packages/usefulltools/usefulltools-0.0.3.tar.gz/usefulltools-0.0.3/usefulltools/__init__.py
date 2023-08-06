import os
import requests
import linecache

class File:
  def directory(self,directory):
    os.chdir(directory)

  def ls(self,directory=''):
    os.system(f'ls {directory}')

  def run(self,file,language='python'):
    os.system(f'{language} {file}')


  def file(self,filename,content='',mode='a'):
    with open(filename,mode) as f:
      f.write(content)

  def remove(self,filename):
    os.system(f'rm {filename}')

  def download_file(self,file_url,file_name,file_exten):
    types = ['.png','.jpg','.gif']
    x = requests.get(file_url, allow_redirects=True)
    if file_exten in types:
      with open(file_name+file_exten,'wb') as f:
        f.write(x.content)
        return True
    else:
      try:
        with open(file_name+file_exten,'w') as f:
          f.write(x.text)
          return True
      except TypeError:
        os.remove(file_name+file_exten)
        return False
  def get_line(self,file,line_num):
    return linecache.getline(file,line_num)

class Foo:
  def bar(self,x):
    return x*10