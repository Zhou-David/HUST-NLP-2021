class Tokenizer(object):
    def __init__(self, init_words, init_max_len, init_delimiter):
        self.words = init_words
        self.max_len = init_max_len
        self.delimiter = init_delimiter

    def forward_mm_split(self, fmm_text):
        """
        正向最大匹配分词算法
        :param fmm_text: 待分词字符串
        :return: 分词结果，以list形式存放，每个元素为分出的词
        """
        # 字词列表，存放分词结果
        word_list = []

        # 用于记录分词的起始位置
        count = 0

        # 字或词当前的长度
        word_len = self.max_len

        while word_len > 0 and count < len(fmm_text):
            word = fmm_text[count:count + word_len]
            word_len = len(word)
            if (word in self.words) or (word in self.delimiter):
                word_list.append(word)
                count = count + word_len
                word_len = self.max_len
            else:
                word_len = word_len - 1
        return word_list

    def reverse_mm_split(self, rmm_text):
        """
        逆向最大匹配分词算法
        :param rmm_text: 待分词字符串
        :return: 分词结果，以list形式存放，每个元素为分出的词
        """
        # 字词列表，存放分词结果
        word_list = []

        # 用于记录分词的末尾位置
        count = len(rmm_text)

        # 字或词当前的长度
        word_len = self.max_len

        while word_len > 0 and count > 0:
            if count <= word_len:
                word = rmm_text[:count]
            else:
                word = rmm_text[(count - word_len):count]
            word_len = len(word)
            if (word in self.words) or (word in self.delimiter):
                word_list.insert(0, word)
                count = count - word_len
                word_len = self.max_len
            else:
                word_len = word_len - 1
        return word_list

    def bidirectional_mm_split(self, bi_text):
        """
        双向最大匹配分词算法
        :param bi_text: 待分词字符串
        :return: 分词结果，以list形式存放，每个元素为分出的词
        """
        # 前向最大匹配得到的分词结果
        forward = self.forward_mm_split(bi_text)
        # 后向最大匹配得到的分词结果
        reverse = self.reverse_mm_split(bi_text)
        # 总词数
        forward_total_words = len(forward)
        reverse_total_words = len(reverse)
        # 单字词个数
        forward_single_words = 0
        reverse_single_words = 0
        # 非字典词数
        forward_illegal_words = 0
        reverse_illegal_words = 0
        # 罚分，分值越低，表明结果越好
        forward_score = 0
        reverse_score = 0

        if forward == reverse:
            return forward
        else:
            # 统计前向匹配的各个词情况
            for word in forward:
                if len(word) == 1:
                    forward_single_words += 1
                if word not in self.words:
                    forward_illegal_words += 1
            # 统计后向匹配的各个词情况
            for word in reverse:
                if len(word) == 1:
                    reverse_single_words += 1
                if word not in self.words:
                    reverse_illegal_words += 1
            # 计算罚分
            if forward_total_words < reverse_total_words:
                reverse_score += 1
            else:
                forward_score += 1
            if forward_illegal_words < reverse_illegal_words:
                reverse_score += 1
            else:
                forward_score += 1
            if forward_single_words < reverse_single_words:
                reverse_score += 1
            else:
                forward_score += 1
            # 比较罚分情况，罚分最小的选做最终结果
            if forward_score < reverse_score:
                return forward
            else:
                return reverse


def load_dict(path):
    tmp = set()
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            word = line.strip().split(' ')[0]
            tmp.add(word)
    return tmp


if __name__ == '__main__':
    words = load_dict('dict.txt')
    max_len = max(map(len, [word for word in words]))
    delimiter = ',./;\'<>?:\"-=_+!@#$%^&*(){}，。？、；‘“’”·~[]'

    # test
    tokenizer = Tokenizer(words, max_len, delimiter)
    texts = [
        '研究生命的起源',
        '无线电法国别研究',
        '人要是行，干一行行一行，一行行行行行，行行行干哪行都行。'
    ]
    for text in texts:
        # 前向最大匹配
        print('前向最大匹配:', '/'.join(tokenizer.forward_mm_split(text)))
        # 后向最大匹配
        print('后向最大匹配:', '/'.join(tokenizer.reverse_mm_split(text)))
        # 双向最大匹配
        print('双向最大匹配:', '/'.join(tokenizer.bidirectional_mm_split(text)))
        print('')
