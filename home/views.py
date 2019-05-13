from django.shortcuts import render
from core.ResearcherLinks import ResearcherLinks

# Create your views here.


def index(request):

    lConsult = False

    if request.method == 'POST':
        lConsult = True

        url = request.POST['url']
        depthLayers = request.POST['depthLayers']

        objRl = ResearcherLinks(url, depthLayers)

        objReturn = objRl.searchLinks()
        qtdFound = len(objReturn)

        context = {
            'lConsult': lConsult,
            'objReturn': objReturn,
            'url': url,
            'qtdFound': qtdFound
        }
        return render(request, 'home/index.html', context)

    elif request.method == 'GET':
        context = {
            'lConsult': lConsult,
        }
        return render(request, 'home/index.html', context)
