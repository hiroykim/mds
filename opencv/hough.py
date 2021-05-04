import cv2
import numpy as np

img_name="dave2.jpg"

def test_1():
    img = cv2.imread('./data/%s'%img_name)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)

    lines = cv2.HoughLines(edges, 1, np.pi / 180, 150)
    for line in lines:
        rho, theta = line[0]
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho
        x1 = int(x0 + 1000 * (-b))
        y1 = int(y0 + 1000 * (a))
        x2 = int(x0 - 1000 * (-b))
        y2 = int(y0 - 1000 * (a))

        cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 1)

    cv2.imshow('edges', edges)
    cv2.imshow('result', img)
    cv2.waitKey()
    cv2.destroyAllWindows()

def test_2():
    img = cv2.imread('./data/%s'%img_name)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    minLineLength = 50
    maxLineGap = 10

    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 100, minLineLength, maxLineGap)

    for line in lines:
        x1, y1, x2, y2 = line[0]
        cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 1)

    cv2.imshow('edges', edges)
    cv2.imshow('result', img)
    cv2.waitKey()
    cv2.destroyAllWindows()


def main():
    test_1()
    test_2()

if __name__ == "__main__":
    main()