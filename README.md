# dcmagick
[![PyPI version](https://badge.fury.io/py/dcmagick.svg)](https://badge.fury.io/py/dcmagick)
[![MIT licensed](https://img.shields.io/badge/license-MIT-blue.svg)](https://raw.githubusercontent.com/amplify-education/serverless-domain-manager/master/LICENSE)
[![Build Status](https://travis-ci.org/ar90n/dcmagick.svg?branch=master)](https://travis-ci.org/ar90n/dcmagick)

dcmagick is a cli tool for finding, dumping and converting DICOM images.
This is insipired by [DCMTK](https://dicom.offis.de/dcmtk.php.en), [GDCM](https://sourceforge.net/projects/gdcm/) and [imagemagick](https://www.imagemagick.org/).

## Installation

```bash
$ pypi install dcmagick
```

## Feature

### Dump

Dump DICOM tags and images on terminal via various format.

#### Dump by PRETTYE
```bash
$ dcmagick dump --format PRETTY ~/dcms/CT_small.dcm 2> /dev/null
(0008, 0005) Specific Character Set              CS: 'ISO_IR 100'
(0008, 0008) Image Type                          CS: ['ORIGINAL', 'PRIMARY', 'AXIAL']
(0008, 0012) Instance Creation Date              DA: '20040119'
(0008, 0013) Instance Creation Time              TM: '072731'
(0008, 0014) Instance Creator UID                UI: 1.3.6.1.4.1.5962.3
(0008, 0016) SOP Class UID                       UI: CT Image Storage
(0008, 0018) SOP Instance UID                    UI: 1.3.6.1.4.1.5962.1.1.1.1.1.20040119072730.12322
(0008, 0020) Study Date                          DA: '20040119'
(0008, 0021) Series Date                         DA: '19970430'
(0008, 0022) Acquisition Date                    DA: '19970430'
(0008, 0023) Content Date                        DA: '19970430'
(0008, 0030) Study Time                          TM: '072730'
(0008, 0031) Series Time                         TM: '112749'
(0008, 0032) Acquisition Time                    TM: '112936'
(0008, 0033) Content Time                        TM: '113008'
(0008, 0050) Accession Number                    SH: ''
(0008, 0060) Modality                            CS: 'CT'
...
```

#### Dump by JSON
```bash
$ dcmagick dump --format JSON ~/dcms/CT_small.dcm 2> /dev/null | jq .
{
  "0008, 0005": {
    "vr": "CS",
    "description": "Specific Character Set",
    "value": [
      "ISO_IR 100"
    ]
  },
  "0008, 0008": {
    "vr": "CS",
    "description": "Image Type",
    "value": [
      "ORIGINAL",
      "PRIMARY",
      "AXIAL"
    ]
  },
  "0008, 0012": {
    "vr": "DA",
    "description": "Instance Creation Date",
    "value": "20040119"
  },
  "0008, 0013": {
    "vr": "TM",
    "description": "Instance Creation Time",
    "value": "072731"
  },
  "0008, 0014": {
    "vr": "UI",
    "description": "Instance Creator UID",
    "value": "1.3.6.1.4.1.5962.3"
  },
...
```

#### Dump by BRAILLE
```bash
$ dcmagick dump --format BRAILLE ~/dcms/CT_small.dcm 2> /dev/null
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠌⢆⠕⡌⡢⡑⡐⢌⠢⠑⢌⠪⡪⡪⡪⡪⡪⣪⢪⡪⡪⡪⡪⡪⡪⡪⡪⣪⢪⢪⢂⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡌⡊⢆⢕⢜⡬⣪⣎⣎⢜⢌⠢⡑⢕⢕⢝⢜⢎⢎⢎⢎⢎⢇⢏⢎⢮⢪⢣⡣⡣⡣⡣⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⢪⢨⢪⣞⡾⣫⢻⢜⡎⡟⡾⣆⢇⠪⡪⡪⡪⡪⡪⡪⡪⡪⡣⡳⡱⡣⡣⡳⡱⡕⡝⡜⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠢⡱⣸⡽⡳⡹⣜⢜⡕⡕⡝⡎⡯⣳⡕⡌⡪⡪⡪⡣⡫⡪⡣⡣⡇⣇⢗⢕⢝⡜⡜⡜⠌⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡢⡑⡵⣝⢎⢧⢫⢎⢮⢺⢸⡪⡺⡸⡪⡻⣆⠪⡘⢜⢜⢜⢼⢸⢜⢎⢎⢮⢪⢣⠣⢃⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢐⠌⡎⣞⢜⢎⡎⡮⡪⡳⡹⣜⢜⢕⢝⢜⢭⡳⡕⢌⠢⡑⡱⡑⡕⢕⢕⢕⢕⢑⠁⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⢆⢣⢳⢝⢜⢕⢕⢕⢵⢹⡪⡺⡜⣕⡳⡹⡸⡸⣽⢰⠐⢔⠢⡑⠜⠌⠂⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠢⠢⡃⣗⢝⢕⢝⢎⡇⣏⢮⡺⣪⢳⡱⣕⢽⢸⢜⠼⡕⡅⠕⡨⠨⢈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⡎⡪⡑⣕⢽⡪⡇⡗⣗⢽⡸⡱⡕⡕⣳⢹⢜⢮⢳⡹⡪⣏⢎⡂⡢⠑⠄⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡐⡕⡝⡜⡌⡎⣯⡺⣝⢞⡼⡪⣎⢮⡪⡪⣪⡫⣝⢵⡳⣝⢝⣮⢣⢃⢪⢘⢌⠪⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⡘⡜⡜⡜⡜⢔⢕⡷⣝⢮⣳⣽⢽⢹⠱⡙⢎⠞⣞⢮⡳⣝⢮⡳⣕⢇⠣⡑⠜⢔⢑⠅⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⢰⢡⢣⠱⡑⢜⢸⠨⢢⢿⣯⣿⢟⠜⡌⢆⢣⢑⢅⢕⠌⡎⡟⡷⣷⣽⠺⡘⢌⢂⠣⡑⡅⢕⢑⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⢰⠸⡘⢜⠌⡪⠨⡊⡔⡅⣗⢽⢝⡧⡣⡱⡘⡌⢆⢣⠱⡰⡑⡌⡪⡪⡺⡸⡨⢂⠕⢌⢊⢢⠡⡑⢔⠨⡠⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⡀⡆⡣⡑⢅⠕⡡⢪⢨⡪⡪⣪⣺⣪⢷⣝⣎⢆⢪⠢⡱⡑⢅⢣⠢⡃⢎⠢⡑⡕⢕⢱⢑⠜⢌⢢⢡⠱⡡⡑⢌⠢⡑⢄⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⡠⡰⣑⢑⢔⠰⡨⡢⡪⡺⡼⣕⢗⣽⣺⣾⣿⣿⣿⣿⣾⣌⢊⠆⢕⠡⡅⠕⢌⢢⢱⢼⣼⣷⣷⣷⣯⣎⢢⠡⡱⠰⡘⠄⠕⠨⡂⠥⡑⢄⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⢀⢄⢢⢗⡏⡮⡢⡣⡪⡪⡪⡪⣪⢳⢝⡾⣽⣾⢷⣷⣻⣞⡿⡽⣿⣿⣷⣿⣼⣬⣶⣽⣮⣮⣿⢿⡿⣿⢿⣿⣿⣟⢆⠕⢌⢌⢂⠣⡑⢅⠢⠡⡂⡑⢔⠰⡀⡀⠀⠀⠀⠀⠀⠀
⠢⡑⡝⡜⡪⡯⡪⡺⣝⢜⢎⢞⢜⡜⡮⡫⢣⢑⠕⡌⢝⢻⢿⣯⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣻⣽⣯⣿⢿⠫⡣⠱⡨⡊⢆⢂⢪⠨⠢⡑⢌⠪⡰⠨⡂⡢⢊⠔⡡⠠⡀⠀⠀⠀
⡑⡌⡌⢎⠪⡣⡱⡹⡜⡜⡜⣜⢜⢜⠰⡡⡑⡌⡪⡐⡅⢕⠍⡫⡞⣿⣿⣿⣯⢿⢽⢽⣽⣾⢟⡯⡻⡘⢔⢑⢌⠪⡰⡘⢔⢑⠔⡅⡃⡊⡢⢃⠎⡊⢆⠪⠢⡱⠨⡊⠔⠅⢕⠠
⢌⢆⠕⡅⡣⡱⢸⢸⢸⢸⢮⡺⠜⡔⠕⡌⡢⣑⠢⡑⢌⢢⢱⢐⠕⢜⢜⣷⣿⡽⣽⣿⢯⢏⢇⢣⢑⢌⠆⡕⢔⠱⡨⠪⡘⢌⠜⡐⡑⠌⡢⠡⡑⡑⢕⢑⠕⢜⠸⡨⠪⡑⡅⡪
⢢⠢⢣⢊⠆⢎⢊⢆⠣⡑⡕⡸⡨⡪⡘⡌⡪⡂⡣⡑⡅⢕⠌⡆⡣⡑⢕⠸⢽⡿⣿⢫⠫⡘⢔⢑⠔⢅⠕⢌⠆⢇⠎⡪⢊⢢⢑⠱⡘⡌⠆⡕⢌⢌⠢⢅⢣⢑⢕⢘⢌⢢⢑⢌
⡊⢎⠪⡢⢩⢊⢢⢑⢅⢕⢅⠎⡔⢕⠸⡨⠢⡣⡑⡕⢜⢔⢱⢨⠢⡣⡑⢕⢑⢝⢕⢑⢕⢑⢅⢣⢑⢅⢣⢑⠕⢅⠇⢎⠪⡘⡌⡪⢂⢎⠪⣘⢐⢅⢕⢡⢱⢨⠢⡑⡅⡕⢜⢐
⢜⢌⢪⢨⠢⡣⡑⢅⢣⢊⢆⢣⠱⡑⡑⢕⢑⠕⡌⡪⢢⢑⢢⢑⠕⡌⡊⣊⠢⡑⡐⡱⡘⢌⢊⢢⢑⢅⠇⡕⡱⡡⢣⢑⠅⢇⠪⡌⡆⡕⡱⡐⢕⢌⢆⢣⠱⡨⡊⢆⢊⠔⡡⡡
⡢⡱⡨⢢⠣⡒⢌⠪⡢⢱⢘⠔⡕⢅⢣⠣⡑⡕⢌⠎⡜⢌⢊⢆⢕⢌⠜⡐⢕⢨⠨⠢⡑⢅⢣⠱⡐⡢⠣⡊⢆⢣⢑⠢⡑⢅⢇⠪⡢⢱⢨⠸⡐⡅⢆⢣⢑⢕⢘⢌⠄⡕⢌⢆
⢢⢱⠸⡰⡑⡅⡣⡑⢌⠢⡡⡃⡪⡨⡂⡣⢑⠜⢌⠎⢌⠢⢑⠐⢅⢢⠡⢣⢱⢱⡹⡨⢌⠢⡑⡅⡣⡑⡕⡑⡅⡣⠡⡡⠨⠢⡡⡃⡊⡢⡑⡅⢇⢕⠱⡡⠣⡪⠸⡐⢅⠊⢆⠕
⢅⢣⠱⡸⡐⢕⢑⠌⡆⢕⠰⡨⢂⠢⡂⡊⢔⠨⠢⡡⡱⢨⢂⢇⢣⠢⡣⡑⢌⠢⡊⢔⢅⠕⡌⡢⡡⡑⡌⡌⢌⠢⢑⠌⢌⢊⠢⡪⠨⡂⢎⢌⠢⢢⢃⢎⠪⡘⢌⠢⡢⡡⡑⡌
⡊⢆⢣⠱⡸⡘⢜⠸⡨⢢⠣⡪⢪⢘⢌⢪⠢⡣⢣⠣⡪⠪⡂⢇⠪⡊⢆⢊⠢⡑⢌⢒⠢⡣⡱⢨⠪⡨⢢⢊⢢⢑⠔⢌⠢⡂⢕⠨⡌⣊⢢⠡⡣⠱⡘⢔⢕⠱⡑⡕⢜⠔⢕⠱
⢸⢨⢢⠣⡪⡨⡢⢣⠪⡢⡣⡑⡅⡣⢪⢂⢇⠕⢅⠣⡪⢊⠪⡨⠊⠌⡂⠅⢅⢊⠐⢌⢊⠢⡑⢅⠣⡊⢎⠜⡌⢆⢍⠎⡊⣊⠪⠪⡘⢔⠅⡇⡣⢍⢎⠪⡢⢣⢱⠸⡰⡩⡊⢎
⡑⡅⡣⡱⠸⡐⠕⢅⠣⣊⢢⢑⠕⢜⢔⠱⡐⠅⡃⡑⠌⡂⡑⠄⠅⠕⡨⠨⢂⠢⠡⡑⡐⡐⠄⢅⠣⡑⡑⢕⠸⡐⢕⢸⠨⡢⡹⡘⡌⢆⢣⠱⡘⡔⢅⢣⢑⢱⠨⣊⢢⠱⡘⡌
⠸⡐⢕⠸⡘⡌⡣⢃⠣⡊⢌⠢⢑⠡⢂⢑⠌⠌⠢⠨⠨⡐⠨⠨⡈⡂⠢⠡⡑⠌⡊⡐⡐⠌⠌⠢⠨⡐⠨⡠⡑⠌⡌⢆⠣⡱⢨⠢⡣⢱⠡⡣⢱⢘⠜⡔⡱⢡⠣⡢⢣⠱⡡⠣
⠡⢃⠅⠅⢅⢂⢊⠔⡁⡂⠅⢌⢂⠅⡢⢂⠊⠌⠌⢌⠌⡂⡑⡡⠨⠂⠅⠕⡐⠅⡢⢁⠊⠌⢌⠌⠢⠨⠨⠐⢄⠑⢄⠑⢌⢐⠡⠑⠌⡊⢌⠊⢆⠣⠱⡘⢌⢊⠪⡨⠢⡃⠕⡉
⢈⠢⡈⡊⠔⡐⡐⡨⢐⠨⡈⠢⡐⠨⠐⠄⠅⡃⠅⢅⢂⠢⢂⠢⠡⠡⡡⢑⠨⠨⡐⠄⠕⠡⡁⡊⠌⡊⠌⢌⢂⢑⢐⠡⢂⢂⢊⠌⢌⢂⠢⢑⢐⠡⠑⢄⢑⠄⠕⡠⠑⢄⢑⢐
⢐⢁⢂⠢⠡⢂⢂⢂⠢⠡⡈⠢⠨⠨⠨⠊⠌⢄⢑⢐⠄⠕⡐⠡⠡⡑⠄⢕⠨⢊⢐⠅⠅⠕⡐⡐⡡⠨⡨⢂⢂⠢⢂⢑⢐⠔⡐⢌⠐⢄⢑⢐⠔⠡⠡⠡⢂⠊⠔⡨⢈⠢⡁⠢
```

#### Dump by HALFBLOCK
```bash
$ dcmagick dump --format HALFBLOCK ~/dcms/CT_small.dcm 2> /dev/null
```
![Dump by HALFBLOCK](https://github.com/ar90n/dcmagick/blob/doc/images/sc_halfblock.png)

#### Dump by ITERM2
```bash
$ dcmagick dump --format ITERM2 ~/dcms/CT_small.dcm 2> /dev/null
```
![Dump by ITERM2](https://github.com/ar90n/dcmagick/blob/doc/images/sc_iterm2.png)

### Find

Find DICOM images by MongpDB like query to its tags.

```bash
$ dcmagick find --query '{"Modality": "MR"}' --name '*.dcm' ~/dcms/ 2> /dev/null
/home/argon/dcms/MR_small_bigendian.dcm
/home/argon/dcms/emri_small_jpeg_2k_lossless.dcm
/home/argon/dcms/MR_small_RLE.dcm
/home/argon/dcms/emri_small.dcm
/home/argon/dcms/emri_small_big_endian.dcm
/home/argon/dcms/MR_small_jp2klossless.dcm
/home/argon/dcms/MR_small_implicit.dcm
/home/argon/dcms/MR_small_expb.dcm
/home/argon/dcms/emri_small_jpeg_ls_lossless.dcm
/home/argon/dcms/MR_small.dcm
/home/argon/dcms/MR_truncated.dcm
/home/argon/dcms/emri_small_RLE.dcm
/home/argon/dcms/MR_small_jpeg_ls_lossless.dcm
```

### Convert

Convert DICOM images into PNG or JPEG, and vice versa.

#### DICOM to PNG.
```bash
$ dcmagick convert ~/dcms/CT_small.dcm ~/out.png 2> /dev/null
$ file out.png
/home/argon/out.png: PNG image data, 128 x 128, 8-bit grayscale, non-interlaced
```

#### PNG to DICOM.
```bash
$ dcmagick convert ~/out.png ~/out.dcm 2> /dev/null
$ file out.dcm
/home/argon/out.dcm: DICOM medical imaging data
```

## License
This software is released under the MIT License, see [LICENSE](LICENSE).
