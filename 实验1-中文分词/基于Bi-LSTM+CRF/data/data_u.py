import pickle

from sklearn.model_selection import train_test_split

INPUT_DATA = "train.txt"
SAVE_PATH = "./data_save.pkl"
id2tag = ['B', 'M', 'E', 'S']  # B：分词头部 M：分词词中 E：分词词尾 S：独立成词
tag2id = {'B': 0, 'M': 1, 'E': 2, 'S': 3}
word2id = {}
id2word = []


def getlist(input_str):
    """
    单个分词转换为tag序列
    :param input_str: 单个分词
    :return: tag序列
    """
    out_str = []
    if len(input_str) == 1:
        out_str.append(tag2id['S'])
    elif len(input_str) == 2:
        out_str = [tag2id['B'], tag2id['E']]
    else:
        m_num = len(input_str) - 2
        m_list = [tag2id['M']] * m_num
        out_str.append(tag2id['B'])
        out_str.extend(m_list)
        out_str.append(tag2id['E'])
    return out_str


def handle_data():
    """
    处理数据，并保存至save_path
    :return:
    """
    x_data = []
    y_data = []
    word_num = 0
    line_num = 0
    with open(INPUT_DATA, 'r', encoding="utf-8") as ifp:
        for line in ifp:
            line_num = line_num + 1
            line = line.strip()
            if not line:
                continue
            line_x = []
            for i in range(len(line)):
                if line[i] == " ":
                    continue
                if line[i] in id2word:
                    line_x.append(word2id[line[i]])
                else:
                    id2word.append(line[i])
                    word2id[line[i]] = word_num
                    line_x.append(word_num)
                    word_num = word_num + 1
            x_data.append(line_x)

            line_arr = line.split()
            line_y = []
            for item in line_arr:
                line_y.extend(getlist(item))
            y_data.append(line_y)

    print(x_data[0])
    print([id2word[i] for i in x_data[0]])
    print(y_data[0])
    print([id2tag[i] for i in y_data[0]])
    x_train, x_test, y_train, y_test = train_test_split(x_data, y_data, test_size=0.1, random_state=43)
    with open(SAVE_PATH, 'wb') as output:
        pickle.dump(word2id, output)
        pickle.dump(id2word, output)
        pickle.dump(tag2id, output)
        pickle.dump(id2tag, output)
        pickle.dump(x_train, output)
        pickle.dump(y_train, output)
        pickle.dump(x_test, output)
        pickle.dump(y_test, output)


if __name__ == "__main__":
    handle_data()
