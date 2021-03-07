import requests as rq
from bs4 import BeautifulSoup
import re, threading, time, certifi, datetime
from io import BytesIO


start_time = time.time()

urlPage = "http://insidelearn.com/courses/all?page="
hitPage = rq.get(urlPage+"1")
print("--- %s seconds ---" % (time.time() - start_time))
htmlPage = BeautifulSoup(hitPage.content, "html.parser")
page = htmlPage.find("ul", {"class":"pagination"}).find_all("li")[-2]
print("* ----------------- *\n[INFO] FOUND",page.text,"PAGE ")


# --- >
try:
	brp = int(input('Masukkan Berapa Page: '))
	if brp > int(page.text): brp = int(page.text)
except Exception as e:
	brp = 1
page = brp # Mau berapa Page?
# --- >


print("[INFO] PARSING",page,"PAGE\n* ----------------- *")

isi = []
th = []
def urlHit(url):
	hit = rq.get(url)
	# hit = hitURLNya(url)
	isi.append({'isi':hit, 'no':int(url.split("=")[1])})
for x in range(page-1,-1,-1):
	print("="*50)
	url = f"{urlPage}{x+1}"
	print(f"** PAGE {x+1} ** | HIT URL ", url)
	t = threading.Thread(target=urlHit, args=[url])
	th.append(t)

print("\n* ============================ *")
print("[INFO] GETTING ALL ELEMENT..!")
print("* ============================ *", "\n")

for x in th:
	x.start()
for x in th:
	x.join()
print("--- %s seconds ---" % (time.time() - start_time))
isi = sorted(isi, key=lambda i:i['no']) 

datenow = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

arr = []
for y in reversed(isi):
	txt = ""
	txt += f'\n[PAGE] {y["no"]}'
	txt += f'\n{"="*50}\n'
	print("\n[PAGE]", y["no"])
	print("="*50)
	hit = y['isi']
	html = BeautifulSoup(hit.content, "html.parser")
	cards = html.find_all("div", {'class':"single-job-post row nomargin"})
	for x in cards:
		a = x.find_all("a")
		txtnya = a[1]
		categori = a[2]
		txt += f"[INFO] {txtnya.text}\n"
		txt += f"[CATG] {categori.text}\n"
		txt += f"[LINK] {txtnya['href']} \n----------------\n"
		print(f"[INFO] {txtnya.text}")
		print(f"[CATG] {categori.text}")
		print(f"[LINK] {txtnya['href']}", "\n----------------")
	arr.append(txt)

with open(datenow+".txt", "w") as fl:
	tmp = """*****************************************
*  THANKS FOR USE                       *
*  Please Come to My Github             *
*  https://github.com/airgg             *
*                                       *
*  Don't Forget to Follow My Instagram  *
*  https://instagram.com/airgg18        *
*                                       *
*****************************************
"""
	print(tmp)
	for x in reversed(arr): tmp += x
	fl.write(tmp)
print("--- %s seconds ---" % (time.time() - start_time))
time.sleep(3600)