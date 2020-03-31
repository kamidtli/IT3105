single_line = "\u2013"
hline = single_line*3
v_sep = "\ / "
n_sep = "/ \\ "

def print_board(state):
  size = len(state)
  width = size + 3*(size-1)
  rows = rotate(state)
  sep = n_sep
  print(single_line*width + "\n")
  for row in rows:
    row_str = ""
    for j in range(len(row)):
      row_str += str(row[j].value)
      if j < len(row)-1:
        row_str += hline

    print(row_str.center(width))
    if sep == n_sep:
      print((" " + sep*len(row)).center(width))
    else:
      print((" " + sep*(len(row)-1)).center(width))


    if len(row) == size - 1:
      sep = v_sep

  print(single_line*width)

def rotate(state):
  rotated_state = []
  for i in range(len(state)):
    row = []
    for j in range(i+1):
      cell = state[i-j][j]
      row.append(cell)
    rotated_state.append(row)

  for i in range(len(state)-1):
    row = []
    for j in range(len(state)-1-i):
      cell = state[len(state)-1-j][j+1+i]
      row.append(cell)
    rotated_state.append(row)
  return rotated_state
