from flhabr import FreelanceHabrParser

if __name__ == "__main__":
    parser = FreelanceHabrParser(output="result.xlsx", query="п")
    parser.run()