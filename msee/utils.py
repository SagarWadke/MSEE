import cv2 as cv

def show_image(image, window_name='Image', max_width=1280, max_height=720):
    # Get the image dimensions
    height, width = image.shape[:2]
    
    # Calculate the scaling factor to fit the image within the max dimensions
    scaling_factor = min(max_width / width, max_height / height)
    
    # Resize the image if it's larger than the specified max dimensions
    if scaling_factor < 1:
        resized_image = cv.resize(image, None, fx=scaling_factor, fy=scaling_factor, interpolation=cv.INTER_AREA)
    else:
        resized_image = image
    # Display the resized image
    cv.imshow(window_name, resized_image)
    cv.waitKey(1000)