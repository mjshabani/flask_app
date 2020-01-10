from flask import g, request, url_for, jsonify
from flask_mongoengine import Pagination
from functools import wraps

def paginate(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        list = f(*args, **kwargs)

        per_page = request.args.get('per_page', 10, type=int)
        page = request.args.get('page', 1, type=int)

        per_page = min(max(per_page, 5), 40)
        page = max(min(page, (len(list)+per_page-1)//per_page), 1)

        paginated = Pagination(list, page, per_page)

        result = {
            'list' : [item.to_json() for item in paginated.items],
            'meta' : {
                'total' : paginated.total,
                'page' : page,
                'pages' : max(paginated.pages, 1),
                'per_page' : per_page,
                'next_page' : url_for(request.endpoint, page=paginated.next_num, per_page=paginated.per_page, _external=True) if paginated.has_next else None,
                'prev_page' : url_for(request.endpoint, page=paginated.prev_num, per_page=paginated.per_page, _external=True) if paginated.has_prev else None
            }
        }
        return jsonify(result), 200
    return wrapper
