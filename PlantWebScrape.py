import requests
import csv
from bs4 import BeautifulSoup

grasses_link = "https://www.eastcoastgardencenter.com/plant-index/grasses.html"
perennials_link = "https://www.eastcoastgardencenter.com/plant-index/perennials.html"
trees_link = "https://www.eastcoastgardencenter.com/plant-index/trees.html"
shrubs_link = "https://www.eastcoastgardencenter.com/plant-index/shrubs.html"

master_list = [[grasses_link, 'grasses'], [perennials_link, 'perennials'], [trees_link, 'trees'], [shrubs_link, 'shrubs']]

def list_of_type_pages(link, type_name, page_counter=2, type_page_links=set([])):
	page_request = requests.get(link)
	soup = BeautifulSoup(page_request.content, 'html.parser')
	type_page_links.add(link)
	for link in soup.find_all('a', href=True):
		if type_name in link['href']:
			if "https://www.eastcoastgardencenter.com" + "/plant-index/" + type_name + "/" + str(page_counter) + ".html" in type_page_links:
				return type_page_links
			if link['href'] == "/plant-index/" + type_name + "/" + str(page_counter) + ".html":
				list_of_type_pages("https://www.eastcoastgardencenter.com" + link['href'], type_name, page_counter + 1)
	return type_page_links

def list_of_plant_pages(link):
	page_request = requests.get(link)
	soup = BeautifulSoup(page_request.content, 'html.parser')
	plant_pages = set([])
	for element in soup.find_all('a', href=True):
		if 'item' in element['href']:
			plant_pages.add("https://www.eastcoastgardencenter.com" + element['href'])
	return plant_pages
	
def collect_specifications(link, type_name):
	fields = ['Type','Botanical Name', 'Common Name', 'Flower Color', 'Height', 'Width', 'Season of Bloom', 'Light Preference', 'Hardiness Zone']
	page_request = requests.get(link)
	list_of_specifications = [type_name]

	soup = BeautifulSoup(page_request.content, 'html.parser')
	for a in soup.find_all("li", {"class": ["element element-text first", "element element-text", "element element-text last"]}):
		for b in a.find_all("strong"):
			list_of_specifications.append(b.next_sibling)
	return list_of_specifications

fields = ['Type', 'Botanical Name', 'Common Name', 'Flower Color', 'Height', 'Width', 'Season of Bloom', 'Light Preference', 'Hardiness Zone']
filename = '*csv file path*'
	
list_of_rows = []

for element in master_list:
	for type_page in list_of_type_pages(element[0], element[1]):
		for plant_page in list_of_plant_pages(type_page):
			list_of_rows.append(collect_specifications(plant_page, element[1]))
			
with open(filename, 'w', newline='') as csvfile:
	csvwriter = csv.writer(csvfile) 
	csvwriter.writerow(fields)
	for element in list_of_rows:
		csvwriter.writerow(element)
		

