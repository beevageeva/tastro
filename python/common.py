import os

def createFolder(dirname_base="out"):
  dirExists = True
  i = 0
  dirname = "%s_%i" % (dirname_base, i)
  while os.path.exists(dirname):
    i +=1
    dirname = "%s_%i" % (dirname_base, i)
  os.mkdir(dirname)
  return dirname

