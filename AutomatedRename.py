import os


def rename_tool(directory):
     directory = directory
     c=0
     for filename in os.listdir(directory):
          path=os.path.join(directory, filename)
          extension = os.path.splitext(path)[1]
          new_file_name= os.path.join(directory,"image"+str(c)+extension)
          os.rename(path, new_file_name)
          c+=1

     print("File renamed!")