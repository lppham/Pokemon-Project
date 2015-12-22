import requests, six
import lxml.html as lh
from itertools import cycle, islice
from matplotlib import colors
import pandas as pd
from pandas.tools.plotting import scatter_matrix
import matplotlib.pyplot as pyplot
#%matplotlib inline

#Getting data from online
url = 'http://pokemondb.net/pokedex/all'
page = requests.get(url)
doc = lh.fromstring(page.content)
tr_elements = doc.xpath('//tr')

stats = ['Attack', 'Defense', 'HP', 'Sp. Atk', 'Sp. Def', 'Speed', 'Total']

col = []
i=0

for t in tr_elements[0]:
	i+=1
	name = t.text_content()
	col.append((name,[]))

for i in range(1, len(tr_elements)):
	T = tr_elements[i]
	if len(T) != 10:
		break

	j = 0

	for t in T.iterchildren():
		data = t.text_content()
		if j > 0:
			try:
				data = int(data)
			except:
				pass
		col[j][1].append(data)
		j += 1

dex_dict = {title:column for (title, column) in col}
df = pd.DataFrame(dex_dict)

def break_str(name):
	#This function separates alternate names for pokemon
	#For example, VenusaurMega Venusaur becomes Venusaur (Mega Venusaur)
	letters = [letter for letter in name]
	for char in range(1, len(letters)):
		if letters[char].isupper():
			#Add space
			letters[char] = ' ' + letters[char]
	final = ''.join(letters).split(' ')
	return final

def brackets(name):
	s = break_str(name)
	length = len(s)

	if length > 1:
		s.insert(1, '(')
		s.append(')')
	return ' '.join(s)

df['Name'] = df['Name'].apply(brackets)
df['Type'] = df['Type'].apply(break_str)

df.to_json('PokeData.json')
df = pd.read_json('PokeData.json')
df = df.set_index(['#'])

def max_stats(df, ret_list):
	msg = ''
	for stat in ret_list:
		best = df[stat].max()
		name = df[ df[stat]==best ]['Name'].values[0]
		msg += 'Greatest ' + stat.ljust(7) + ':'.ljust(2) + str(best).ljust(5) + name + '\n'
	return msg

def min_stats(df, ret_list):
	msg = ''
	for stat in ret_list:
		worst = df[stat].min()
		name = df[ df[stat]==worst ]['Name'].values[0]
		msg += 'Worst ' + stat.ljust(7) + ':'.ljust(2) + str(worst).ljust(5) + name + '\n'
	return msg

scatter_matrix(df[stats[:-1]], alpha=0.2, figsize=(10,10), diagonal='kde')



type_dict = {}
stats_col = ["#", "Name", "Total", "HP", "Attack", "Defense", "Sp. Atk", "Sp. Def", "Speed"]


dex_dict['Type'] = df['Type'].values

for col in stats_col:
	type_dict[col] = []
	type_dict['Type'] = []

for row in range(len(dex_dict['#'])):
	for t in dex_dict['Type'][row]:
		for col in stats_col:
			type_dict[col].append(dex_dict[col][row])
		type_dict['Type'].append(t)

type_df = pd.DataFrame(type_dict)

unique_types = type_df['Type'].unique()

graph_colors = list(six.iteritems(colors.cnames))
graph_colors = list(islice(cycle(graph_colors), None, len(type_df)))

def bar_stats():
	i = 0
	plt.figure(figsize=(15,5))
	plt.subtitle('Selected Statistics', fontsize = 15)

	for t in unique_types:
		i += 1

		#Mean
		plt.subplot(121)
		plt.title('Mean')
		type_df[type_df['Type']==t].mean().plot(kind='bar', color = graph_colors[i])

		#SD
		plt.subplot(122)
		plt.title('Standard Dev.')
		type_df[type_df['Type']==t].std().plot(kind='bar', color = graph_colors[i])

	plt.legend(unique_types, bbox_to_anchor=(1.3,1.1))



