import random
import utils.storage_utils
from datetime import datetime

class id_gen:
  def __init__(self):
    self.character_range = 25
    self.alphabet = 'a b c d e f g h i j k l m n o p q r s t u v w x y z'.split()
    self.alphanumeric = '1 2 3 4 5 6 7 8 9 0'.split()
    self.upper_chance = 0.5

  def get_reverse_timestamp(self):
    f = datetime.now()
    a = 17**100 - int(datetime.timestamp(f))
    return str(a)

  def generate_id(self):
    vid_id = ''
    vid_id += self.get_reverse_timestamp()
    joined_alpha = self.alphabet + self.alphanumeric
    for h in range(self.character_range):
      chance = random.uniform(0, 1)
      random_index = random.randint(0, len(joined_alpha) - 1)
      if chance > self.upper_chance:
        vid_id += joined_alpha[random_index].upper()
      else:
        vid_id += joined_alpha[random_index]
    return vid_id

if __name__ == '__main__':
  id = id_gen()
  out = id.generate_id()
  print(out)