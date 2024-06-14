import sys
import uvicorn
from fastapi import FastAPI, HTTPException
import logging
from pydantic import BaseModel


app = FastAPI(docs_url="/api/docs")

blog_posts = []


logging.basicConfig(filename='logs/app.log', level=logging.WARNING, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)

class BlogPost:
    def __init__(self, id, title, content):
        self.id = id
        self.title = title
        self.content = content
    def __str__(self) -> str:
        return f'{self.id} - {self.title} - {self.content}'
    
    def toJson(self):
        return {'id': self.id, 'title': self.title, 'content': self.content}

class PostCreated(BaseModel):
    id: int
    title: str
    content: str

@app.post('/blog', status_code=201)
def create_blog_post(request:PostCreated):
    try:
        data = request
        blog_posts.append(BlogPost(data.id, data.title, data.content))
        logger.info("created new post")
        return {'status':'sucess'}
    except KeyError:
        logger.error("Invalid request")
        raise HTTPException(status_code=400, detail={'error': 'Invalid request'})
    except Exception as e:
        logger.warning(str(e))
        raise HTTPException(status_code=500, detail={'error': str(e)})
        


@app.get('/blog', status_code=200)
def get_blog_posts():
    logger.info("get all posts")
    return {'posts': [blog.toJson() for blog in blog_posts]}


@app.get('/blog/{id}', status_code=200)
def get_blog_post(id:int):
    for post in blog_posts:
        if post.id == id:
            logger.info(f"get post {id}")
            return {'post': post.__dict__}
    logger.error(f"post {id} not found")
    raise HTTPException(status_code=404, detail={'error': 'Post not found'})
    

@app.delete('/blog/{id}', status_code=200)
def delete_blog_post(id:int):
    for post in blog_posts:
        if post.id == id:
            blog_posts.remove(post)
            logger.info(f"delete post {id}")
            return {'status':'sucess'}
    logger.error(f"post {id} not found")
    raise HTTPException(status_code=404, detail={'error': 'Post not found'})
    

@app.put('/blog/{id}', status_code=200)
def update_blog_post(id:int, request:PostCreated):
    try:
        data = request
        for post in blog_posts:
            if post.id == id:
                post.title = data.title
                post.content = data.content
                logger.info(f"update post {id}")
                return {'status':'sucess'}
        logger.error(f"post {id} not found")
        raise HTTPException(status_code=404, detail={'error': 'Post not found'})
    except KeyError:
        logger.error("Invalid request")
        raise HTTPException(status_code=400, detail={'error': 'Invalid request'})
    except Exception as e:
        logger.warning(str(e))
        raise HTTPException(status_code=500, detail={'error': str(e)})
        

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8001)