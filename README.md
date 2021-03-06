# Installation Instructions

## Install dependencies
```bash
$ sudo apt update
$ sudo apt install libgl1-mesa-glx libegl1-mesa libxrandr2 libxrandr2 libxss1 libxcursor1 libxcomposite1 libasound2 libxi6 libxtst6 automake ca-certificates g++ git libtool libleptonica-dev make pkg-config
```

## Install tesseract
```bash
$ git clone https://github.com/tesseract-ocr/tesseract.git --branch 4.1 --single-branch
$ cd tesseract/
$ ./autogen.sh
$ ./configure
$ make
$ sudo make install
$ sudo ldconfig
$ cd /usr/local/share/tessdata/
$ sudo wget https://github.com/tesseract-ocr/tessdata/raw/master/eng.traineddata
$ sudo wget https://github.com/tesseract-ocr/tessdata/raw/master/osd.traineddata
```

## Install and activate Anaconda
```bash
$ cd <path-to-cappy-directory>
$ wget https://repo.anaconda.com/archive/Anaconda3-2019.10-Linux-x86_64.sh
$ bash Anaconda3-2019.10-Linux-x86_64.sh
$ source ~/.bashrc
(base) $ conda create --name cappy python=3.7
(base) $ conda activate cappy
(cappy) $
```

## Install python packages
```bash
(cappy) $ pip install --user --requirement requirements.txt
```

## Run cappy
```bash
(cappy) $ python ./cappy.py
```

## Test cappy without including network calls in time
```bash
(cappy) $ python ./nonetwork-cappy.py
```

## Deactivate Anaconda
```bash
(cappy) $ conda deactivate
(base) $ conda deactivate
$ 
```
