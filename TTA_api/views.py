from diffusers import AudioLDM2Pipeline
#import torch
#import scipy
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import numpy as np
from pydub import AudioSegment
from io import BytesIO

def homepage(request):
    print("The server is up and running")
    return JsonResponse({"message": "Server running"})



def generate_audio(prompt, repo_id="cvssp/audioldm2", num_inference_steps=1, audio_length_in_s=10.0):
    pipe = AudioLDM2Pipeline.from_pretrained(repo_id)
    pipe = pipe.to("cpu")
    audio = pipe(prompt, num_inference_steps=num_inference_steps, audio_length_in_s=audio_length_in_s).audios[0]
    return (audio * 32767).astype(np.int16)

def write_audio(audio_waveform):
    sample_width = 2  # 16-bit
    frame_rate = 16000  # 16 kHz
    channels = 1  # Mono

    audio_bytes = audio_waveform.tobytes()
    audio_segment = AudioSegment(
        audio_bytes,
        sample_width=sample_width,
        frame_rate=frame_rate,
        channels=channels
    )

    converted_audio_stream = BytesIO()
    audio_segment.export(converted_audio_stream, format="wav")
    return converted_audio_stream

@csrf_exempt
@require_http_methods(["GET"])
def TTA(request):
    prompt = request.GET.get("prompt", "").strip()
    if prompt:
        prompt = prompt.replace("%22", "")  # Remove double quotes from the encoded string
        audio_waveform = generate_audio(prompt)
        audio_stream = write_audio(audio_waveform)

        # Create a Django HttpResponse with the audio data and appropriate MIME type
        response = HttpResponse(audio_stream.getvalue(), content_type='audio/wav')
        response['Content-Disposition'] = 'attachment; filename="generated_audio.wav"'

        return response
    else:
        return JsonResponse({"error": "prompt parameter is required"}, status=400)

TTA = csrf_exempt(require_http_methods(["GET"])(TTA))


TTA = csrf_exempt(require_http_methods(["GET"])(TTA))