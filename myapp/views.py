from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from pvleopard import create, LeopardActivationLimitError, LeopardError

def transcribe_audio(request):
    if request.method == 'POST' and request.FILES['audioFile']:
        try:
            # save file to server
            file = request.FILES['audioFile']
            fs = FileSystemStorage()
            filename = fs.save(file.name, file)
            
            # transcribe with Leopard Speech-to-Text
            leopard = create(access_key="TLRhZQnqZ8i9WBMKE6usdvUgfpfVlIMzypNjWsC0otltA6Jj2o5hnQ==")
            transcript, words = leopard.process_file(filename)
            
            # clean up
            leopard.delete()
            fs.delete(filename)
        except LeopardActivationLimitError:
            return JsonResponse({'error': "AccessKey has reached its processing limit."})
        except LeopardError:
            return JsonResponse({'error': "Unable to transcribe audio file."})
        else:
            for word in words:
                print(
                    "{word=\"%s\" start_sec=%.2f end_sec=%.2f confidence=%.2f}"
                    % (word.word, word.start_sec, word.end_sec, word.confidence))
            return JsonResponse({'transcript': transcript})
    return render(request,"transcribe_audi.html")
