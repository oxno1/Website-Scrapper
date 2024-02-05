from requests import get,post
import zipfile,os
os.mkdir('result')
def Copy(URL: str):
    data = {
  "url": URL,
  "renameAssets": False,
  "saveStructure": False,
  "alternativeAlgorithm": False}
    return post("https://copier.saveweb2zip.com/api/copySite",json=data).json()['md5']

def isFinished(proccess: str):
    return get(f"https://copier.saveweb2zip.com/api/getStatus/{proccess}").json()
def DownloadSource(proccess: str):
    downloading = get(f"https://copier.saveweb2zip.com/api/downloadArchive/{proccess}")
    filename = 'result/'+downloading.headers.get('Content-Disposition').split('filename="')[1].split('"')[0]
    with open(filename,'wb') as file:
        file.write(downloading.content)
    with zipfile.ZipFile(filename, 'r') as zip_ref:
        zip_ref.extractall(filename.split('.')[0])
    os.remove(filename)

url = input("Enter site URL : ")
print("Getting files md5")
md5 = Copy(url)
print("Grapped : "+md5)
print("Starting copy files ...")
while 1:
    status = isFinished(md5)
    if status['isFinished'] and status['success']:
        break
print("Done copy files .....")
print('Downloading.......')
DownloadSource(md5)
print('Done <by @oxno1>')
