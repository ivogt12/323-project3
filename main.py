import sys
from syntax_analyzer import Parser

def print_usage():
    """Display command-line usage instructions"""
    print()

def main():
    # Check command-line arguments
    if len(sys.argv) != 3:
        print_usage()
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    try:
        # Initialize and run parser
        #print(f"\nCompiling {input_file}...")
        parser = Parser(input_file, output_file)
        parser.parse()
        
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found")
        sys.exit(1)
    except Exception as e:
        print(f"Fatal Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()