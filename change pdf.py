import time 
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import fitz  # import PyMuPDF
import yaml
import sys

class ExampleHandler(FileSystemEventHandler):
    #the file is created/moved in directory
    def on_created(self, event):
        file_name = event.src_path.split('.')
        print (file_name[len(file_name) - 1])

        if file_name[len(file_name) - 1] != 'pdf':

            with open(dir_name + '\error.txt', 'a') as f:
                f.write("File " +  event.src_path + " was not recognized as pdf.\n")

        else:

            try:
                #often happens that you try to access the file while it has not yet been closed so I added a timer
                time.sleep(5)
                doc = fitz.open(event.src_path)

                for page in doc:

                    for index, text in enumerate(old_text):

                        for xref in page.get_contents():
                            stream = doc.xref_stream(xref).replace(bytes(text, 'utf-8'), bytes(new_text[index], 'utf-8'))
                        
                        doc.update_stream(xref, stream)

                doc.save(event.src_path, incremental=True, encryption=fitz.PDF_ENCRYPT_KEEP)
                print("pdf saved")
            except Exception as ex:

                with open(dir_name + '\error.txt', 'a') as f:
                    f.write("Error on file " +  event.src_path + ": " + str(ex) + "\n")
                    print(ex)

#get settings that work only for exe file
dir_name = sys.executable
dir_name = dir_name.replace('replace-text-pdf.exe', '')
print(dir_name)
config = yaml.safe_load(open(dir_name + 'settings.yml'))
old_text = config['old-text']
new_text = config['new-text']
path = config['path-pdf']
observer = Observer()
#create event handler
event_handler = ExampleHandler() 
#set observer to use created handler in directory
observer.schedule(event_handler, path=path)
observer.start()

# sleep until keyboard interrupt, then stop + rejoin the observer
try:
    while True:
        time.sleep(1)
        print("WOOF")
except KeyboardInterrupt:
    observer.stop()

observer.join()