def absolute_metrics(y_hat,y_label):
    abs_value=0
    i=0
    while i<len(y_hat):
        abs_value= abs_value+(abs(y_hat[i]-y_label[i]))
        i=i+1
    abs_value = abs_value / len(y_hat)
    return abs_value

def accuracy_metrics(y_hat,y_label):
    count=0
    i=0
    while i<len(y_hat):
        if y_hat[i]==y_label[i] :
            count=count+1
        i=i+1
    accur=count/len(y_hat)
    return accur

def F1_score(y_hat,y_label):
    n = len(y_hat)
    true_positive = 0
    false_positive = 0
    false_negative = 0
    for i in range (n):
        if y_label[i]==1 and y_hat[i] ==1 :
            true_positive += 1
        if y_label[i]==0 and y_hat[i] ==1 :
            false_positive += 1
        if y_label[i]==1 and y_hat[i] ==0 :
            false_negative += 1

    if true_positive>0:
        precision=float(true_positive)/(true_positive+false_positive)
        recall=float(true_positive)/(true_positive+false_negative)

        return 2*((precision*recall)/(precision+recall))
    else:
        return 0

def confusion_matrix(y_hat, y_label):

    conf_arr = [[0, 0],
                [0, 0]]

    for i in range(len(y_hat)):
        if int(y_label[i]) == 0:
            if y_hat[i] == 0 :
                conf_arr[0][0] = conf_arr[0][0] + 1
            elif y_hat[i] == 1 :
                conf_arr[1][0] = conf_arr[1][0] + 1
        elif int(y_label[i]) == 1:
            if y_hat[i] == 0 :
                conf_arr[0][1] = conf_arr[0][1] + 1
            elif y_hat[i] == 1 :
                conf_arr[1][1] = conf_arr[1][1] + 1
    return conf_arr