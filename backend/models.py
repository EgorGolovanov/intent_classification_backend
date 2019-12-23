from django.db import models

class Categories(models.Model):
  id = models.AutoField(primary_key=True)
  name = models.TextField()

  def __str__(self):
      return self.name

class Requests(models.Model):
    id = models.AutoField(primary_key=True)
    content = models.TextField()
    is_marked_up = models.BooleanField(default=False)
    categories = models.ManyToManyField(Categories)

    def __str__(self):
        return self.content
