import string
from django.db import connection
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render

from lh_project import settings

from .models import Lesson
from .forms import LessonForm, CategoryForm

import PyPDF2
from pydantic import FileUrl
import textract

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from pathlib import Path

from django.contrib import messages


# Create your views here.
def index(request):
    """The home page for Learning Hub."""
    return(render(request, 'learning_hub/base.html'))

def filtered_lesson(request):
    form = CategoryForm(request.POST, request.FILES) 
    cat = request.POST.get('category') 
    print("Category ID: ", cat)  
    lesson = Lesson.objects.all()
 
    if cat == None or cat == '':
        lesson_list = lesson
    else:    
        lesson_list = lesson.filter(category__id=cat)

       
    #lesson_list = Lesson.objects.select_related('category').order_by('category')
    paginator = Paginator(lesson_list, settings.MAX_LESSON_LIST)  # Show 25 contacts per page.
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "learning_hub/filtered_lesson.html", {"form": form, "page_obj": page_obj, "lesson": lesson})

'''def filtered_lesson(request):
    lesson = Lesson.objects.all()
    print("Lesson: ", lesson)
    return render(request, "learning_hub/filtered_lesson.html", {"lesson": lesson})'''
      
def new_lesson(request):
    #print(request)
    if request.method == 'POST':
        form = LessonForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            title = request.POST.get('title')
            id = getProblemStatementFromTitle(title)
            print("Id and Title: ", id[0][0], title)
            tokenizer(request, id[0][0])
        
            
            #return HttpResponseRedirect("/new_lesson/?submitted=true")
            return render(request, 'learning_hub/new_lesson.html', {'form': form, 'submitted': 'sumbitted'})
    else:
        form = LessonForm()
    return render(request, 'learning_hub/new_lesson.html', {'form': form})

def lesson_detail(request, pk):
    print("Request: ", request)
    lesson = Lesson.objects.get(pk=pk)
    context = {'lesson': lesson}
    return render(request, 'learning_hub/lesson_detail.html', context)

def getProblemStatementFromTitle(title):
    with connection.cursor() as cursor:
        cursor.callproc('getProblemStatementFromTitle', [title])
        results = cursor.fetchall()

    return results

def tokenizer(request, id):
    #lesson = Lesson()

    record = Lesson.objects.get(id=id)
        
    #context = {'entry': this_id, 'title': this_title, 'problem_statement': this_statement}
    #return render(request, 'base.html')
    record.problem_statement = (pdfTokenizer(id)).strip()
    record.save(update_fields=['problem_statement']) 
    
    #return HttpResponseRedirect('/lessons?submitted=True')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def pdfTokenizer(id):
    print("Id = ", id)
    lesson = Lesson.objects.get(pk=id)
    print("BASE_DIR: ", settings.BASE_DIR)
    print("MEDIA_ROOT: ", settings.MEDIA_ROOT)
    print("STATICFILES_DIRS: ", settings.STATICFILES_DIRS)
    print("PDF doc name: ", lesson.problem_document)
    filename = str(settings.MEDIA_ROOT) + "/" + str(lesson.problem_document)
    print("File name: ", filename)
    
    #open allows you to read the file.
    pdfFileObj = open(filename,'rb')
        
    #The pdfReader variable is a readable object that will be parsed.
    pdfReader = PyPDF2.PdfReader(pdfFileObj)

    print('Number of pages = ',len(pdfReader.pages))

    #Discerning the number of pages will allow us to parse through all the pages.
    num_pages = len(pdfReader.pages)
    count = 0
    text = ""

    #The while loop will read each page.
    while count < num_pages:
        pageObj = pdfReader.pages[count]
        count += 1
        text += pageObj.extract_text()

    #print("Extracted text: ", text)    

    #This if statement exists to check if the above library returned words. It's done because PyPDF2 cannot read scanned files.
    if text != "":
        text = text
    #If the above returns as False, we run the OCR library textract to #convert scanned/image based PDF files into text.
    else:
        text = textract.process(FileUrl, method='tesseract', language='eng')

    #Now we have a text variable that contains all the text derived from our PDF file. Type print(text) to see what it contains. It likely contains a lot of spaces, possibly junk such as '\n,' etc.
    #Now, we will clean our text variable and return it as a list of keywords.

    #The word_tokenize() function will break our text phrases into individual words.
    #print("Extracted text: ", text)
    tokens = word_tokenize(text.lower())

    #We'll create a new list that contains punctuation we wish to clean.
    #punctuations = ['(',')',';',':','[',']',',']
    punctuations = [';',':','[',']',',','!','.',',','[',']']
    #We initialize the stopwords variable, which is a list of words like "The," "I," "and," etc. that don't hold much value as keywords.

    stop_words = stopwords.words('english')
    stop_words = set(stop_words)-set(['a'])

    #We create a list comprehension that only returns a list of words that are NOT IN stop_words and NOT IN punctuations.
    keywords = [word for word in tokens if not word in stop_words and not word in punctuations]
    #keywords = [word for word in tokens if not word in punctuations]
    #keywords = "Hello New World!"

    #print(keywords)
    keyword_collection = ' '
    for word in keywords:
        keyword_collection += ' ' + word
    return keyword_collection

def getProblemStatementFromTitle(title):
    with connection.cursor() as cursor:
        cursor.callproc('getProblemStatementFromTitle', [title])
        results = cursor.fetchall()

    return results

def getProblemStatement(id):
    with connection.cursor() as cursor:
        cursor.callproc('getProblemStatement', [id])
        results = cursor.fetchall()

    return results
    
def getLessonCount():
    with connection.cursor() as cursor:
        cursor.callproc('getLessonCount')
        results = cursor.fetchall()
        if results:  # Check if there are any results
            return results[0][0]  # Extract the number from the fetched results
        else:
            return None  # Return None if no results found

    print("Lesson count = ", results)
    return results

def getIdList():
    with connection.cursor() as cursor:
        cursor.callproc('getAllIds')
        results = cursor.fetchall()

    return results

def getCategory(id):
    with connection.cursor() as cursor:
        cursor.callproc('getCategory', [id])
        results = cursor.fetchall()

    return results


def search(request):
    # Check if the request is a POST request (i.e., button click)
    if request.method == 'POST':
        dict_id = {}
        count = getLessonCount()
        print("Lesson count ", count)
        search_text = request.POST['search_text']  # Access the value of the "search_text" field from the submitted form
        print("Search text: ", search_text)
        if search_text is not "":
            dict_id = similarity(request, search_text)
            #dict_id = {0:87,1:76} #for testing with multiple ids
            print("Dict: ", dict_id)
        else:
            messages.add_message(request, messages.INFO, "Search box cannot be empty.")
            return render(request, 'error.html')

        if dict_id != {}:
            id_list = list(dict_id.values())

            lessons =  Lesson.objects.filter(id__in = id_list)
            context = {'lessons': lessons}
            return render(request, 'learning_hub/result.html', context)   
        else:
            messages.add_message(request, messages.INFO, "No matching questions found in LMS.")
            return render(request, 'learning_hub/error.html')
            #messages.error(request, "This is a custom message")
    #else:
         # Render the initial template if there was no button click
        #return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
        #form = SearchForm()
        
    return render(request, 'learning_hub/search.html')

def calculateTermFrequency(tokens):
    # Calculate word frequency
    termFreq = {}
    # Iterate through the tokens and count the frequency of each token
    for token in tokens:
        if token in termFreq:
            termFreq[token] += 1
        else:
            termFreq[token] = 1
    return termFreq

def jaccard_similarity(set1, set2):
    # Calculate Jaccard similarity, which is a measure used to compare the similarity and diversity of sets
    intersection = set(set1).intersection(set2)
    union = set(set1).union(set2)
    similarity = len(intersection) / len(union)
    return similarity

def normalizeSimilarity(similarity):
    maxPossibleSimilarity = 1
    # Normalize the similarity score to a scale of 100 using a linear transformation
    confidence = (similarity * 100) / maxPossibleSimilarity
    return confidence

def similarity(request, search_text):
    context = {}
    kount = 0
    count = getLessonCount()
    idList = getIdList()

    for id in idList:
        conf = confidence(int(id[0]), search_text)
        print("MAX_CONFIDENCE: ", settings.MAX_CONFIDENCE)
        if conf > settings.MAX_CONFIDENCE:
            context[kount] = int(id[0])
            kount = kount + 1
        
    return context 
    
def confidence(id, search_text):
    problem_statement = str(getProblemStatement(id))
    if len(problem_statement) != 0:
        clean_problem_statement = removePunctuation(str(problem_statement))
        #print("Problem statement: ", clean_problem_statement)                        
        problem_statement_tokens = tokenize(clean_problem_statement)

        cleanText = removePunctuation(str(search_text))
        #print('Cleaned string test:', cleanText)

        search_tokens = tokenize(cleanText)

        set1 = calculateTermFrequency(problem_statement_tokens)
        #print(set1)
        set2 = calculateTermFrequency(search_tokens)
        #print(set2)

        jsimilarty = jaccard_similarity(set1, set2)
        print('jaccard Similarity',jsimilarty)  
    
        confidence = normalizeSimilarity(jsimilarty)
        print('Confidence', confidence, '%')
    else:
        confidence = 0.0

    return confidence

def removePunctuation(textBlock):
    # Remove all punctuation marks from text block and replace them with blancks
    #textBlock = re.sub(r'\n', " ", textBlock)
    preprocessedTextBlock = textBlock.translate(textBlock.maketrans('', '', string.punctuation))
    return preprocessedTextBlock.lower()

def tokenize(block):
    # Split the text block into individual words or tokens
    tokens = block.split(" ")
    # using filter() to perform removal
    tokens = list(filter(None, tokens))

    return tokens

def lesson_delete(request, id = None):
    instance = get_object_or_404(Lesson, id=id)
    
    questionsDir = str(instance.problem_document) # Question dir path (relative) from database
    answersDir = str(instance.answer_document) # Answer dir path (relative) from database
    filepathQ = str(settings.MEDIA_ROOT) + "/" + questionsDir # Question dir full path 
    filepathA = str(settings.MEDIA_ROOT) + "/" + answersDir # Answer dir full path 

    file_pathQ = Path(filepathQ)
    file_pathA = Path(filepathA)
    print("File names: ", file_pathQ, file_pathA)
    file_pathQ.unlink() # Delete Question file
    file_pathA.unlink() # Delete Answer file

    instance.delete() # Delete database records
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))