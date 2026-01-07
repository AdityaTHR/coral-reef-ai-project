import cv2
import numpy as np

class CoralImageEnhancer:
    def enhance_image(self, image_path):
        """Simple enhancement for underwater coral images"""
        print(f"Enhancing: {image_path}")
        
        # Read image
        img = cv2.imread(image_path)
        if img is None:
            print("Error: Cannot read image")
            return None
        
        # 1. Color correction (reduce blue tint)
        img_lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(img_lab)
        
        # Apply CLAHE to L channel for better contrast
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        l = clahe.apply(l)
        
        # Reduce blue channel (b channel in LAB)
        b = cv2.addWeighted(b, 0.7, np.ones_like(b)*128, 0.3, 0)
        
        # Merge back
        enhanced_lab = cv2.merge([l, a, b])
        enhanced = cv2.cvtColor(enhanced_lab, cv2.COLOR_LAB2BGR)
        
        # 2. Sharpen slightly
        kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
        enhanced = cv2.filter2D(enhanced, -1, kernel)
        
        print("✅ Image enhanced")
        return enhanced
    
    def save_image(self, image, output_path):
        """Save image to file"""
        cv2.imwrite(output_path, image)
        print(f"Saved to: {output_path}")

# Test the enhancer
if __name__ == "__main__":
    enhancer = CoralImageEnhancer()
    
    # Create a test image
    test_img = np.zeros((200, 300, 3), dtype=np.uint8)
    test_img[:, :, 0] = 150  # Blue tint (water effect)
    test_img[50:150, 100:200, 2] = 180  # Coral-like red area
    
    # Save test image
    cv2.imwrite("test_coral_input.jpg", test_img)
    print("Created test image: test_coral_input.jpg")
    
    # Enhance it
    enhanced = enhancer.enhance_image("test_coral_input.jpg")
    
    if enhanced is not None:
        enhancer.save_image(enhanced, "test_coral_enhanced.jpg")
        print("✅ Enhancer is working!")