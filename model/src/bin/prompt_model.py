
import sys
import os

src_dir = os.path.join(os.getcwd(), "..", "..")

sys.path.append(os.path.abspath(src_dir))

from src.utils.visualizer import Visualizer 

visualizer = Visualizer()

sentence = "Je veux passer par Bucy le Long. Je veux aller à Abergement le Petit depuis Viodos Abense de Bas en passant par Marseille, mais je veux éviter Chauny. Je voudrais aussi passer par Bourguignon sous Coucy."

response = visualizer.pipeline(sentence)

print(response)
