from tool.runners.python import SubmissionPy

class Number:
  def __init__(self, left, right):
      self.left: Number or int = left
      self.right: Number or int = right
  
  def update(self, deep, parent, side):
    self.deep = deep
    self.parent = parent
    self.side = side
    if not type(self.left) == int:
      self.left.update(deep + 1, self, "left")
    if not type(self.right) == int:
      self.right.update(deep + 1, self, "right")

  def copy(self):
    if type(self.left) == int:
      left = self.left
    else:
      left = self.left.copy()
    if type(self.right) == int:
      right = self.right
    else:
      right = self.right.copy()
    return Number(left, right)
    

  def split(self):
    if type(self.left) == int and self.left > 9:
      left = self.left // 2
      self.left = Number(left, self.left - left)
      self.left.update(self.deep + 1, self, "left")
      return True
    if type(self.right) == int and self.right > 9:
      left = self.right // 2
      self.right = Number(left, self.right - left)
      self.right.update(self.deep + 1, self, "right")
      return True
    
    if not type(self.left) == int:
      if self.left.split():
        return True
    if not type(self.right) == int:
      return self.right.split()
    return False
    

  def chain_right_child_down(self, value):
    if type(self.right) == int:
      self.right += value
    else:
      self.right.chain_right_child_down(value)

  def chain_left_child_down(self, value):
    if type(self.left) == int:
      self.left += value
    else:
      self.left.chain_left_child_down(value)

  def chain_left_child_up(self, value, side):
    if side == "right":
      if type(self.left) == int:
        self.left += value
      else:
        self.left.chain_right_child_down(value)
    elif self.parent:
      self.parent.chain_left_child_up(value, self.side)

  def chain_right_child_up(self, value, side):
    if side == "left":
      if type(self.right) == int:
        self.right += value
      else:
        self.right.chain_left_child_down(value)
    elif self.parent:
      self.parent.chain_right_child_up(value, self.side)

  def explode_left_child(self, left, right):
    self.left = 0
    if type(self.right) == int:
      self.right += right
    else:
      self.right.chain_left_child_down(right)
    if self.parent:
      self.parent.chain_left_child_up(left, self.side)

  def explode_right_child(self, left, right):
    self.right = 0
    if type(self.left) == int:
      self.left += left
    else:
      self.left.chain_right_child_down(left)
    if self.parent:
      self.parent.chain_right_child_up(right, self.side)

  def explode(self):
    if self.deep >= 4 and type(self.left) == int and type(self.right) == int:
      if self.side == "left":
        self.parent.explode_left_child(self.left, self.right)
      else:
        self.parent.explode_right_child(self.left, self.right)
      return True
    else:
      if not type(self.left) == int:
        if self.left.explode():
          return True
      if not type(self.right) == int:
        return self.right.explode()
    return False

  def compute(self):
    if type(self.left) == int:
      left = self.left
    else:
      left = self.left.compute()
    if type(self.right) == int:
      right = self.right
    else:
      right = self.right.compute()
    return 3 * left + 2 * right

def buildNumbers(s):
  v = []
  for i in s:
    if i == "[" or i == ",":
      continue
    if i == "]":
      if type(v[-2]) == str:
        v[-2] = int(v[-2])
      if type(v[-1]) == str:
        v[-1] = int(v[-1])
      n = Number(v[-2], v[-1])
      v = v[:-2]
      v.append(n)
      continue
    v.append(i)
  r = v[0]
  return r

class FrenkiSubmission(SubmissionPy):
  def run(self, s):
    L = []
    for i in s.splitlines():
      L.append(buildNumbers(i))
    
    r = 0
    for i in L:
      for j in L:
        if i == j:
          continue
        a = i.copy()
        b = j.copy()
        p = Number(a, b)
        p.update(0, None, None)
        while p.explode():
          continue
        while p.split():
          while p.explode():
            continue
        r = max(r, p.compute())
    return r
