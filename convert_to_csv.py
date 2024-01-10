import pandas as pd
import os
def convert(file_name):
    with open(file_name, 'r') as file:
        lines = file.readlines()
        data = [line.strip().split(',') for line in lines]

    df = pd.DataFrame(data, columns=['Symbol', 'Price', 'Quantity', 'Trade time'])
    # name = 
    file_name = 'book_data/' + file_name.split("/")[1].split(".")[0] + ".csv"
    df.to_csv(file_name)


if __name__ == "__main__":
    list_file = os.listdir("data_txt")
    list_path_file = ['data_txt/' + item for item in list_file]
    print(list_path_file)
    for path_file in list_path_file:
        convert(path_file)
        print(f"sucessful {path_file}")
    # test = 'data_txt/coinTradeData_2023-12-22_17-46-57.txt'.split("/")[1].split(".")[0] + ".csv"
    # print(test)