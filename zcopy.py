import os

def update_test_file():
    # Updated file paths
    cart_path = 'data/cart.txt'
    products_path = 'data/products.txt'
    output_path = 'test.py'
    
    # Files to process
    files_to_read = [cart_path, products_path]

    # Open test.py in write mode ('w') to clear any existing content first
    with open(output_path, 'w', encoding='utf-8') as outfile:
        
        for file_path in files_to_read:
            try:
                # Open and read the source file
                with open(file_path, 'r', encoding='utf-8') as infile:
                    content = infile.read()
                    
                    # Write the file title as a comment (e.g., # data/cart.txt)
                    outfile.write(f"# {file_path}\n")
                    
                    # Write the raw content without triple quotes
                    outfile.write(f"{content}\n\n")
                    
                    print(f"Successfully added content from: {file_path}")
                    
            except FileNotFoundError:
                print(f"Error: The file '{file_path}' was not found.")
            except Exception as e:
                print(f"An unexpected error occurred with '{file_path}': {e}")

if __name__ == "__main__":
    update_test_file()
    print("Finished updating test.py")