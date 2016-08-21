from models import *

def add_data():

    #Add user
    user1 = Users("trunghieu", "12345")
    db.session.add(user1)
    db.session.commit()

    user2 = Users("boshieu", "123456")
    db.session.add(user2)
    db.session.commit()

    #Add cataloges
    cata1 = Catalogues("FullStack")
    db.session.add(cata1)
    db.session.commit()

    cata2 = Catalogues("English")
    db.session.add(cata2)
    db.session.commit()

    cata3 = Catalogues("Crypto")
    db.session.add(cata3)
    db.session.commit()

    #Add tag
    tag1 = Tags("Python")
    db.session.add(tag1)
    db.session.commit()

    tag2 = Tags("Flask")
    db.session.add(tag2)
    db.session.commit()

    tag3 = Tags("PostgreSQL")
    db.session.add(tag3)
    db.session.commit()

    tag4 = Tags("HTML")
    db.session.add(tag4)
    db.session.commit()

    #Add post
    user_post = Users.query.get(1)
    tag_ids = [1, 2, 3, 4]

    post1 = Posts("First post",
                  """This is first post.
                  <br>This post have four tags and two comments.""")
    post1.users = user_post
    catalogue = Catalogues.query.get(1)
    post1.cataloges = catalogue
    for id in tag_ids:
        tag = Tags.query.get(id)
        post1.tags.append(tag)
    db.session.add(post1)
    db.session.commit()

    post2 = Posts("Second post",
                  """This is second post. <br>
                  This post have two tags and one comment.""")
    post2.users = user_post
    catalogue = Catalogues.query.get(2)
    post2.cataloges = catalogue
    tag = Tags.query.get(1)
    post2.tags.append(tag)
    tag = Tags.query.get(3)
    post2.tags.append(tag)
    db.session.add(post2)
    db.session.commit()

    post3 = Posts("Third post",
                  """This is third post.
                  <br>This post have one tag and one comment.""")
    post3.users = user_post
    catalogue = Catalogues.query.get(3)
    post3.cataloges = catalogue
    tag = Tags.query.get(2)
    post3.tags.append(tag)
    db.session.add(post3)
    db.session.commit()

    #Add comment
    comment1 = Comments("Trung Hieu", "This is first comment for first post")
    post = Posts.query.get(1)
    comment1.posts = post
    db.session.add(comment1)
    db.session.commit()

    comment2 = Comments("Bos Hieu", "This is second comment for first post")
    post = Posts.query.get(1)
    comment2.posts = post
    db.session.add(comment2)
    db.session.commit()

    comment3 = Comments("Trung Hieu", "This is first comment for second post")
    post = Posts.query.get(2)
    comment3.posts = post
    db.session.add(comment3)
    db.session.commit()

    comment4 = Comments("Trung Hieu", "This is first comment for third post")
    post = Posts.query.get(3)
    comment4.posts = post
    db.session.add(comment4)
    db.session.commit()
