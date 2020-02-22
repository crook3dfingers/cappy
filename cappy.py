import argparse
import cv2
import requests
import shutil
import time
from tesserocr import PyTessBaseAPI, PSM, OEM

def main():
	parser = argparse.ArgumentParser(usage='%(prog)s [options] posturl', description='Cappy, the little captcha solver.')

	parser.version = "0.1"
	parser.add_argument("posturl", metavar="posturl", type=str, help="the url to POST the captcha to")
	parser.add_argument("-i", "--imageurl", type=str, help="the url to grab the captcha (default: <posturl>/craptcha.php")
	parser.add_argument("-o", "--output", type=str, default="/tmp/captcha.png", help="where to save the temporary captcha file (default: /tmp/captcha)")
	parser.add_argument("-s", "--success", type=str, default=" more!", help="text to check response for to determine successful captcha submission (default:  more!)")
	parser.add_argument("-e", "--error", type=str, default="Wrong CAPTCHA!", help="text to check response for to determine wrong captcha post (default: Wrong CAPTCHA!)")
	parser.add_argument("-c", "--count", type=int, default=200, help="total number of captchas to try (default: 200)")
	parser.add_argument("-n", "--name", type=str, default="captcha", help="field name of captcha (default: captcha)")
	parser.add_argument("-v", action="version")

	args = parser.parse_args()
	posturl = args.posturl
	imageurl = args.imageurl
	output = args.output
	success = args.success
	wrong = args.error
	totalcount = args.count
	captchaname = args.name

	if imageurl == None:
		imageurl = posturl + "/craptcha.php"

	with PyTessBaseAPI(psm=PSM.SINGLE_WORD, oem=OEM.TESSERACT_ONLY) as api:
		api.SetVariable("tessedit_char_whitelist", "abcdefghijklmnopqrstuvwxyz")
		
		image = None
		count = 0
		successcount = 0
		wrongcount = 0
		ses = requests.Session()
		starttime = time.time()

		while count < totalcount:
			res = ses.get(imageurl, stream=True).raw
			with open(output, "wb") as out_file:
				shutil.copyfileobj(res, out_file)
			del res

			image = cv2.imread(output, cv2.IMREAD_GRAYSCALE)
			image = cv2.resize(image, None, fx=10, fy=10, interpolation=cv2.INTER_LINEAR)
			image = cv2.GaussianBlur(image, (5,5), 0)
	#		image = cv2.bilateralFilter(image, 9, 75, 75)
	#		image = cv2.blur(image, (5,5))
	#		image = cv2.medianBlur(image, 9)
			ret, image = cv2.threshold(image, 185, 255, cv2.THRESH_BINARY)
			cv2.imwrite(output, image)

			api.SetImageFile(output)
			captcha = api.GetUTF8Text().replace(" ", "").rstrip().lower()
			content = ses.post(url=posturl, data={captchaname : captcha}).content

			count += 1
			html = str(content)

			if success in html:
				successcount += 1
			elif wrong in html:
				wrongcount += 1
			else:
				print(html)

		elapsedtime = time.time() - starttime

	print("Finished")
	print("Time: " + str(round(elapsedtime)) + " seconds")
	print("Correct: " + str(successcount))
	print("Wrong: " + str(wrongcount))
	print("Percent Correct: " + str(round((successcount/(successcount + wrongcount)) * 100)) + "%")
	print("Correct solves per 30 seconds: " + str(round((successcount/elapsedtime) * 30)))

if __name__== "__main__":
	main()
