from django.db import models


# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=30)
    email = models.EmailField()
    name = models.CharField(max_length=15)
    surname = models.CharField(max_length=15)
    profile_pic = models.ImageField(upload_to='Bilqram/Images/Profile_Pictures')
    contributionScore = models.IntegerField(default=0)

    def __str__(self):
        return self.username


class Content(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    pub_date = models.DateTimeField()
    editable = models.BooleanField(default=False)

    def edit(self, content: str):
        if not self.editable:
            return False
        self.content = content.strip()
        self.save()
        return True

    def __str__(self):
        return self.title


class Blog(Content):
    pass


class Comment(Content):
    par_blog = models.ForeignKey(Blog, on_delete=models.CASCADE)


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    date = models.DateTimeField()
