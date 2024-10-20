
import sys
import os

src_dir = os.path.join(os.getcwd(), "..", "..")

sys.path.append(os.path.abspath(src_dir))

from model_2.utils.visualizer import Visualizer 

visualizer = Visualizer()

sentence = "Je souhaite partir de Bosmont sur Serre pour arriver à Brancourt en Laonnois en passant par Chatillon sur Oise."

response = visualizer.pipeline(sentence)

print(response)
