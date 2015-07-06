# script om de drie analyse stappen van timewalk opnieuw te doen
# zie:
# - read_ESD.py
# - walk.py
# - fit_model_1_en_2.py
# In de losse bestanden staan de namen van de datafiles "hardcoded"
#  (het is niet anders)
import read_ESD
import walk
import fit_model_1_en_2

if __name__ == '__main__':
    read_ESD.main()
    walk.main()
    fit_model_1_en_2.main()
