from django.shortcuts import render
from django.http import HttpResponseRedirect
from django import forms
from django.contrib import messages
from re import search
from . import util
import random
import markdown2



class NewEntryForm(forms.Form):
	entry_title = forms.CharField(label='Title', max_length=200)
	entry_content = forms.CharField(label='Content for entry', widget=forms.Textarea)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

"""
	View to display the entry's content and title in a separate page  
	ex : wiki/HTML displays HTML's page content from entries/HTML.md
"""
def entry(request, title):
	if util.get_entry(title):
	    return render(request, "encyclopedia/entry.html", {
	        "content": markdown2.markdown(util.get_entry(title)),
	        "title": title
	    })
	elif title == "search_entry": 
		return search_entry(request)
	elif title == "add_entry":
		return add_entry(request)
	elif title == "randomized_entry":
		return randomized_entry(request)
	elif title == "edit_entry":
		return edit_entry(request)
	else: 
		return render(request, "encyclopedia/error404.html")

"""
	View to display the query search result in a separate page  
	ex : user search for "PHP" it should redirect in wiki/PHP
	if it exists or search something with first letter PH -> PHP
"""
def search_entry(request):
	query = request.GET.get('q', '')
	result_entries = util.list_entries()
	result_queries = []

	if util.get_entry(query):
		return entry(request, query)
	else:
		for i in range(len(result_entries)):
			if search(query.casefold(), result_entries[i].casefold()):
				result_queries.append(result_entries[i])
		if not result_queries:
			return render(request, "encyclopedia/error404.html")

		return render(request, "encyclopedia/search_entry.html", {
			"result_title" : query,
			"result_queries" : result_queries
		})

"""
	View to add a new entry in the encyclopedia
	If an entry already exists we put a message for the user
"""
def add_entry(request):
    if request.method == "POST":
    	form = NewEntryForm(request.POST)
    	if form.is_valid():
    		title = form.cleaned_data["entry_title"]
    		content = form.cleaned_data["entry_content"]
    		if util.get_entry(title):
    			messages.add_message(request, messages.INFO, 'This entry already exists ! Please try again with a new entry !!')
    			return render(request, "encyclopedia/add_entry.html", {
    				"form" : form
    			})
    		else:
    			return HttpResponseRedirect(title, util.save_entry(title, content))
    	else:
    		return render(request, "encyclopedia/add_entry.html", {
    			"form" : form
    			})
    else:
    	return render(request, "encyclopedia/add_entry.html", {
    			"form" : NewEntryForm()
    	})

"""
	Randomly displays an entry
"""
def randomized_entry(request):
	random_entry = util.list_entries()
	n = random.randint(0, len(random_entry)-1)
	return HttpResponseRedirect(random_entry[n])

"""
	View to displays the page to edit an entry
	We need to use again the form to display entry datas to edit
"""
def edit_entry(request):
	title = request.GET.get('title', '')
	if request.method == "POST":
		form = NewEntryForm(request.POST)
		if form.is_valid():
			content = form.cleaned_data["entry_content"]
			title = form.cleaned_data["entry_title"]
			return HttpResponseRedirect(title, util.save_entry(title, content))
	else:
		return render(request, "encyclopedia/edit_entry.html", {
			"title" : title,
			"content" : util.get_entry(title),
			"form" 	: NewEntryForm(initial={'entry_title': title,'entry_content': util.get_entry(title)})
		})