#!/usr/bin/env python3

from flask import request, session, jsonify, make_response
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

import os
from config import create_app, db, api
from models import Book, BookSchema

env = os.getenv("FLASK_ENV", "dev")
app = create_app(env)

class Books(Resource):
    def get(self):
        # 1. Extract query parameters with type-casting and default fallbacks
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=5, type=int)
        
        # 2. Execute paginated query using error_out=False to handle out-of-bounds pages
        pagination = Book.query.paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        
        # 3. Serialize only the current page's matching items
        items_json = [BookSchema().dump(b) for b in pagination.items]
        
        # 4. Construct response dictionary matching test requirements precisely
        response_data = {
            "page": page,
            "per_page": per_page,
            "items": items_json,
            "total": pagination.total,
            "total_pages": pagination.pages
        }
        
        return make_response(jsonify(response_data), 200)


api.add_resource(Books, '/books', endpoint='books')


if __name__ == '__main__':
    app.run(port=5555, debug=True)
