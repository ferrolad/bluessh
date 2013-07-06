from django.shortcuts import render_to_response

def gotoIndex(request):
    return render_to_response('index.html')
