import requests


class OCR:
    def __init__(self):
        pass

    @staticmethod
    def ocr_space_file(filename, overlay=False, api_key='602f2b87ab88957', language='eng'):
        payload = {'isOverlayRequired': overlay,
                   'apikey': api_key,
                   'language': language,
                   }
        with open(filename, 'rb') as f:
            r = requests.post('https://api.ocr.space/parse/image',
                              files={filename: f},
                              data=payload,
                              )
        return r.content.decode()


if __name__ == "__main__":
    pass
