import jieba
import readTextReview as rTR

fileLength = rTR.readFilelength()

for i in range(fileLength):
    text = rTR.readTextReviews(i)
    if type(text) == float:
        print("No reviews")
    else:
        print(text)
        seg_list = []
        for t in text:
            seg = jieba.cut(t, cut_all=False)
            seg_list.append(seg)
        for seg in seg_list:
            for word in seg:
                print(word)
