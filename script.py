boxVert1 = [[2008, 2026], [1998, 1474], [2056, 1473], [2065, 2025]]
boxVert2 = [[994, 1679], [911, 1670], [955, 1245], [1039, 1254]]
boxVert3 = [[126, 1572], [-28, 1140], [107, 1092], [261, 1524]]
boxVert4 = [[450, 288], [430, 181], [472, 173], [492, 280]]
boxHorz1 = [[301, 317], [281, 209], [427, 182], [447, 289]]
boxHorz2 = [[298, 321], [276, 206], [475, 169], [497, 284]]

def isHorz(arr):
    arrY = sortBy(arr, 'y')
    arrX = sortBy(arr, 'x')
    height = abs(arrY[0][1] - arrY[2][1])
    width = abs(arrX[0][0] - arrX[2][0])

    # print 'arrY', arrY
    # print 'arrX', arrX
    # print 'height', height
    # print 'width', width

    if width/height<1:
        # print 'vert'
        return False
    else:
        # print 'horz'
        return True

def sortBy(arr, i=0):
    if i == 'x':
        i = 0
    elif i == 'y':
        i = 1

    temp = arr[:]
    temp.sort(key=lambda t: t[i])
    return temp

print isHorz(boxVert1)
print isHorz(boxVert2)
print isHorz(boxVert3)
print isHorz(boxVert4)
print isHorz(boxHorz1)
print isHorz(boxHorz2)