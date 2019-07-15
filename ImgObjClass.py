

class Item(object):
   def __init__(self, label , xmax, xmin, ymin, ymax):
      self.label = label
      self.xmax = xmax
      self.xmin = xmin
      self.ymin = ymin
      self.ymax = ymax


   def __repr__(self):
      return '{}: xmin: {}, xmax: {}, ymin: {}, ymax: {}'.format(self.label, self.xmin,self.xmax, self.ymin, self.ymax)



class Img(object):
   def __init__(self, name, objects):
      self.name  = name
      self.objects = objects

   def __repr__(self):
      return '{}: {}'.format(self.name,self.objects)
