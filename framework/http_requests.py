class GetReq:
    @staticmethod
    def parse_query_string(string) -> dict:
        """Парсит строку параметров на аргументы и создает из них словарь"""
        result = {}
        if string:
            split_string = string.split('&')
            for item in split_string:
                k, v = item.split('=')
                result[k] = v
        return result

    @staticmethod
    def get_requests_params(environ):
        query_string = environ['QUERY_STRING']
        request_params = GetReq.parse_query_string(query_string)
        return request_params


class PostReq(GetReq):
    @staticmethod
    def get_wcgi_input_data (environ) -> bytes:
        """Если длинна контента не пустая принимаем весь контент и кладем в дату"""
        data_len = environ.get('CONTENT_LENGTH')
        content_length = int(data_len) if data_len else 0
        data = environ['wsgi.input'].read(content_length) if content_length > 0 else b''
        return data

    @staticmethod
    def decode_wsgi_input_data(data: bytes) -> dict:
        """Декодируем байтовую строку в строку и парсим в словарь"""
        data_string = data.decode(encoding='utf-8')
        result = PostReq.parse_query_string(data_string)
        return result

    def get_requests_params(self, environ):
        byte_data = self.get_wcgi_input_data(environ)
        data = self.decode_wsgi_input_data(byte_data)
        return data
