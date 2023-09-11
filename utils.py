import synonyms


def syn_judge(s1, s2, threshold=0.707):
    return synonyms.compare(s1, s2)>=threshold


if __name__=="__main__":
    print(synonyms.compare("相当的", "相当得"))