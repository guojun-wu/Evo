import pandas as pd
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--metric', type=str, default='bert', help='metric to use')
    parser.add_argument('-f', '--file', type=str, default='en-de', help='file to view')
    args = parser.parse_args()

    df = pd.read_csv(f'result/{args.metric}/{args.file}.csv')

    # show shape
    print(df.shape)

    # show head
    print(df.head())

if __name__ == "__main__":
    main()
    