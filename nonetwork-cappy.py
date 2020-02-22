import argparse
import cv2
import requests
import shutil
import time
from tesserocr import PyTessBaseAPI, PSM, OEM

def main():
	parser = argparse.ArgumentParser(usage='%(prog)s [options] imageurl', description='Cappy, the little captcha solver.')

	parser.version = "0.1"
	parser.add_argument("imageurl", metavar="imageurl", type=str, help="the url to POST the captcha to")
	parser.add_argument("-o", "--output", type=str, default="/tmp/captcha.png", help="where to save the temporary captcha file (default: /tmp/captcha.png)")
	parser.add_argument("-oe", "--outputedited", type=str, default="/tmp/captcha-edited.png", help="where to save the temporary captcha file (default: /tmp/captcha-edited.png)")
	parser.add_argument("-c", "--count", type=int, default=200, help="total number of captchas to try (default: 200)")
	parser.add_argument("-v", action="version")

	args = parser.parse_args()
	imageurl = args.imageurl
	output = args.output
	outputedited = args.outputedited
	totalcount = args.count

	with PyTessBaseAPI(psm=PSM.SINGLE_WORD, oem=OEM.TESSERACT_ONLY) as api:
		api.SetVariable("tessedit_char_whitelist", "abcdefghijklmnopqrstuvwxyz")
		
		res = requests.get(imageurl, stream=True).raw
		with open(output, "wb") as out_file:
			shutil.copyfileobj(res, out_file)
		del res

		image = None
		count = 0
		starttime = time.time()

		while count < totalcount:
			image = cv2.imread(output, cv2.IMREAD_GRAYSCALE)
			image = cv2.resize(image, None, fx=10, fy=10, interpolation=cv2.INTER_LINEAR)
			image = cv2.GaussianBlur(image, (5,5), 0)
	#		image = cv2.bilateralFilter(image, 9, 75, 75)
	#		image = cv2.blur(image, (5,5))
	#		image = cv2.medianBlur(image, 9)
			ret, image = cv2.threshold(image, 185, 255, cv2.THRESH_BINARY)
			cv2.imwrite(outputedited, image)

			api.SetImageFile(outputedited)
			captcha = api.GetUTF8Text().replace(" ", "").rstrip().lower()

			count += 1

		elapsedtime = time.time() - starttime

	print("Finished")
	print("Time: " + str(round(elapsedtime)) + " seconds")
	print("Total solves per 30 seconds: " + str(round((count/elapsedtime) * 30)))

if __name__== "__main__":
	main()
