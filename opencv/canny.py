import cv2

def test_1():
    img_gray = cv2.imread('data/house.jpg', cv2.IMREAD_GRAYSCALE)
    cv2.imshow("Original", img_gray)

    img_canny = cv2.Canny(img_gray, 50, 150)
    cv2.imshow("Canny Edge", img_canny)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

def nothing():
    pass

def test_2():

    img_gray = cv2.imread('data/house.jpg', cv2.IMREAD_GRAYSCALE)

    cv2.namedWindow("Canny Edge")
    cv2.createTrackbar('low threshold', 'Canny Edge', 0, 1000, nothing)
    cv2.createTrackbar('high threshold', 'Canny Edge', 0, 1000, nothing)

    cv2.setTrackbarPos('low threshold', 'Canny Edge', 50)
    cv2.setTrackbarPos('high threshold', 'Canny Edge', 150)

    cv2.imshow("Original", img_gray)

    while True:

        low = cv2.getTrackbarPos('low threshold', 'Canny Edge')
        high = cv2.getTrackbarPos('high threshold', 'Canny Edge')

        img_canny = cv2.Canny(img_gray, low, high)
        cv2.imshow("Canny Edge", img_canny)

        #ESC = 27
        if cv2.waitKey(1) & 0xFF == 27:
            break

    cv2.destroyAllWindows()


def main():
    #test_1()
    test_2()


if __name__ == "__main__":
    main()