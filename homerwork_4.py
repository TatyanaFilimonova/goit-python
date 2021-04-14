from pathlib import Path
import sys


def parse_folder(path):
    for i in path.iterdir():
      if i.is_dir(): 
          parse_folder(i)
      else: 
        suffix = i.suffix.upper()[1:]
        if suffix in image: image_list.append(i.name)
        elif suffix in video: video_list.append(i.name)
        elif suffix in docs: docs_list.append(i.name)
        elif suffix in music: music_list.append(i.name)
        elif suffix in arch: arch_list.append(i.name)
        else:
           unknown_list.append(i.name)
           if suffix not in unknown_ext: unknown_ext.append(suffix)
           continue
        if suffix not in known_ext: known_ext.append(suffix) 


def parse_args():
    print("Start function parse args")
    result = ""
    print(sys.argv)
    for arg in sys.argv[1:]:
      result=result+arg
      result=result+" "
    print (result.strip())
    return result.strip()


def print_list(lst):
   for i in lst:
      print(i)
      

def print_results():
   print("Image Files:")
   print_list(image_list)
   print ("++++++++++++++++++++++++++++++++++++++++++++++++++++++")
   print ("Video Files:")
   print_list(video_list)
   print ("++++++++++++++++++++++++++++++++++++++++++++++++++++++")
   print ("Docs Files:")
   print_list(docs_list)
   print ("++++++++++++++++++++++++++++++++++++++++++++++++++++++") 
   print("Music Files:")
   print_list(music_list)
   print ("++++++++++++++++++++++++++++++++++++++++++++++++++++++")
   print("Arch Files:")
   print_list(arch_list)
   print ("++++++++++++++++++++++++++++++++++++++++++++++++++++++")
   print ("Unknown files")
   print_list(unknown_list)
   print ("++++++++++++++++++++++++++++++++++++++++++++++++++++++")
   print ("Known extention")
   print_list(known_ext)
   print ("++++++++++++++++++++++++++++++++++++++++++++++++++++++")
   print ("Unknown extention")
   print_list(unknown_ext)

   
image =  ('JPEG', 'PNG', 'JPG', 'SVG')
video =  ('AVI', 'MP4', 'MOV', 'MKV')
docs =  ('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX')
music = ('MP3', 'OGG', 'WAV', 'AMR')
arch =  ('ZIP', 'GZ', 'TAR')

image_list = []
video_list = []
docs_list = []
music_list = []
arch_list = []
unknown_list = []
known_ext = []
unknown_ext = []

parse_folder(Path(parse_args()))
print_results()




