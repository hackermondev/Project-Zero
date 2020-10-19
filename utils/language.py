import detectlanguage
import os
from googletrans import Translator

detectlanguage.configuration.api_key = os.getenv('detectlanguage')

def detect(content):
  return detectlanguage.simple_detect(content)

def translate(content):
  translator = Translator()

  return translator.translate(content)