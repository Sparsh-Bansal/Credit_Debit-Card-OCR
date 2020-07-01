#Credit/Debit Card-OCR

Its an OPENCV-based project to read Account Number , Card Type , and Accont Holder Name from Credit/Debit Card . 

Usually OCR (Tesseract) is used to read text from images . but here the text written is in different font , so that will not work in this case.

So here Template matching technique is used with a different font(digits and aphabets separately) to extract the associated credit card digits/alphabets from images.

#Process : 

1. Localize the four groupings of four digits on a credit card.

2. Extract each of these four groupings followed by segmenting each of the sixteen numbers individually.

3. Recognize each of the sixteen credit card digits by using template matching and the OCR-A FONT.
