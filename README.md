# Credit/Debit Card-OCR

Its an OPENCV-based project to read Account Number , Card Type , and Accont Holder Name from Credit/Debit Card . 

Usually OCR (Tesseract) is used to read text from images . but here the text written is in different font , so that will not work in this case.

So here Template matching technique is used with a different font(digits and aphabets separately) to extract the associated credit card digits/alphabets from images.

# Process : 

1. Localize the four groupings of four digits on a credit card.
2. Extract each of these four groupings followed by segmenting each of the sixteen numbers individually.
3. Recognize each of the sixteen credit card digits by using template matching and the OCR-A FONT.


# Steps :

1. Clone this Repo.
2. pip install > requirements.txt
3. Run Command :  python final_card_ocr.py -image IMAGE_PATH 

# Font-Images:
<p float="left">
  <img src="font_images/OCRA.png" width="400" height="200" />
  <img src="font_images/ocr_a_reference.png" width="500" height="100" /> 
</p>

# Results : 

<p float="center">
  <img src="Sample_images/credit_card_01.png" width="400" height="200" />
</p>

Account No. : 
Card Type   : 
Name        : 
