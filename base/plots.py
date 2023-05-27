import statistics
import pickle

def load_element(file_name):
    fr = open(file_name, 'rb')
    element = pickle.load(fr)
    fr.close()
    return element

y =load_element('dists_avgs')
x= load_element('all_form_areas')


# print(x)
print(statistics.mean(x))
print()
for i in y:
    print(i)
